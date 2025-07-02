from langgraph.graph import StateGraph, START
from langgraph.checkpoint.mongodb import MongoDBSaver, AsyncMongoDBSaver
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import SystemMessage
from src.agents.llm.chat import llm_with_tools
from src.agents.tools import tools
from src.agents.state.schema import State
from src.core.config import settings
from src.agents.llm.prompts import INITIAL_PROMPT
from pymongo import AsyncMongoClient

client = AsyncMongoClient(settings.MONGO_URI)

def assistant(state: State) -> State:
    system_message = SystemMessage(content=INITIAL_PROMPT())
    return { "messages": [llm_with_tools.invoke([system_message] + state["messages"])] }

def build_graph():
    checkpointer = AsyncMongoDBSaver(client)
    builder = StateGraph(State)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")
    return builder.compile(checkpointer=checkpointer)
    
