from fastapi import APIRouter, Request
from src.agents.main import graph
import logging
from langchain_core.messages import HumanMessage
from twilio.rest import Client
from src.core.config import settings
from src.agents.state.schema import State

_logger = logging.getLogger(__name__)
router = APIRouter(prefix="/agents", tags=["agents"])

# Twilio client
twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    try:
        form_data = await request.form()
        user_message = form_data.get("Body", "")
        user_number = form_data.get("From", "")

        state = State(
            messages=[HumanMessage(content=user_message)],
            my_var=""
        )

        # Ejecutar el graph en streaming
        config = {
            "configurable": {
                "thread_id": user_number
            }
        }

        response = await graph.ainvoke(state, config)

        final_message = response['messages'][-1].content


        # Enviar la última respuesta al usuario por WhatsApp
        twilio_client.messages.create(
            from_=settings.TWILIO_FROM_NUMBER,
            to=user_number,
            body=final_message
        )

        return {"status": "message sent"}

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        _logger.error(f"Error en WhatsApp webhook: {e}\nTraceback:\n{tb}")
        return {"error": f"{str(e)}\nTraceback:\n{tb}"}
