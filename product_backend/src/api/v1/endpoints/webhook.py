from fastapi import APIRouter, Request
from src.agents.main import graph
import logging
from langchain_core.messages import HumanMessage, ToolMessage
from twilio.rest import Client
from src.core.config import settings
from src.agents.state.schema import State

from pymongo import MongoClient

_logger = logging.getLogger(__name__)
router = APIRouter(prefix="/agents", tags=["agents"])

# Twilio client
twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

# Mongo client
mongo_client = MongoClient(settings.MONGO_URI)
db = mongo_client["langgraph_db"]
collection = db["conversations"]

# Serializers
from langchain_core.messages import AIMessage

def serialize_message(msg):
    if msg.type == "tool":
        return {
            "type": msg.type,
            "tool_call_id": getattr(msg, "tool_call_id", None),
            "name": getattr(msg, "name", None),
            "content": msg.content
        }
    else:
        return {
            "type": msg.type,
            "content": msg.content
        }

def deserialize_message(data):
    if data["type"] == "human":
        return HumanMessage(content=data["content"])
    elif data["type"] == "ai":
        return AIMessage(content=data["content"])
    elif data["type"] == "tool":
        return ToolMessage(
            content=data["content"],
            tool_call_id=data.get("tool_call_id"),
            name=data.get("name")
        )
    else:
        raise ValueError(f"Unknown message type: {data['type']}")
    

def save_state(session_id: str, state_obj):
    serialized_messages = [
        serialize_message(msg) for msg in state_obj["messages"]
    ]
    doc = {
        "session_id": session_id,
        "messages": serialized_messages,
        "my_var": state_obj.get("my_var", "")
    }
    collection.update_one(
        {"session_id": session_id},
        {"$set": doc},
        upsert=True
    )

def load_state(session_id: str):
    doc = collection.find_one({"session_id": session_id})
    if not doc:
        return None

    messages = [deserialize_message(m) for m in doc["messages"]]

    return {
        "messages": messages,
        "my_var": doc.get("my_var", "")
    }

@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    try:
        form_data = await request.form()
        user_message = form_data.get("Body", "")
        user_number = form_data.get("From", "")

        session_id = user_number

        # Cargar estado previo (si existe)
        previous_state = load_state(session_id)

        if previous_state is None:
            # Si no existe, crear nuevo estado
            state = State(
                messages=[HumanMessage(content=user_message)],
                my_var=""
            )
        else:
            # FILTRAR: Solo human y ai
            filtered_messages = [
                msg for msg in previous_state["messages"]
                if msg.type in ["human", "ai"]
            ]

            # Agregar el nuevo mensaje humano
            filtered_messages.append(HumanMessage(content=user_message))

            state = State(
                messages=filtered_messages,
                my_var=previous_state["my_var"]
            )

        # Ejecutar grafo
        result = await graph.ainvoke(state)

        # Guardar nuevo estado en MongoDB
        save_state(session_id, result)

        # Buscar solo la última respuesta AI con texto
        agent_response = None
        for msg in reversed(result["messages"]):
            if msg.type == "ai" and msg.content.strip():
                agent_response = msg.content
                break

        if agent_response is None:
            agent_response = "Lo siento, no pude procesar tu solicitud."

        # Enviar respuesta a WhatsApp
        twilio_client.messages.create(
            from_=settings.TWILIO_FROM_NUMBER,
            to=user_number,
            body=agent_response
        )

        return {"status": "message sent"}

    except Exception as e:
        _logger.error(f"Error in WhatsApp webhook: {e}")
        return {"error": str(e)}

