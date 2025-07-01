from langgraph.graph import StateGraph, START
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.messages import SystemMessage
from src.agents.llm.chat import llm_with_tools
from src.agents.tools import tools
from src.agents.state.schema import State

def assistant(state: State) -> State:
    system_message = SystemMessage(content="...")
    return { "messages": [llm_with_tools.invoke([system_message] + state["messages"])] }

def build_graph():
    builder = StateGraph(State)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")
    return builder.compile()
