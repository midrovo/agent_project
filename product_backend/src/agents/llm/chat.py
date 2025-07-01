from langchain_openai import ChatOpenAI
from src.agents.tools import tools

llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)
