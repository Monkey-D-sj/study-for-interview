from langchain_core.tools import tool


@tool
def ask_user(question: str) -> str:
    """
    询问用户问题
    """
    return question
