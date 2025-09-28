from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from src.agents.llm.prompts import DESCRIBE_PROMPT

def describe_product(name: str) -> dict:
    """
    Genera una breve descripción comercial y amigable de un producto, 
    basada únicamente en su nombre, usando el LLM.

    Args:
        name (str): Nombre del producto

    Returns:
        dict: Diccionario con la descripción generada
    """

    llm_local = ChatOpenAI(model="gpt-4o", temperature=0.7)
    description = llm_local.invoke(DESCRIBE_PROMPT(name)).content

    print(description)

    return {
        "name": name,
        "description": description
    }