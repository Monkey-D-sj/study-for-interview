from langchain_core.tools import tool
from langgraph.types import interrupt
from pydantic import Field, BaseModel

class AskUserTool(BaseModel):
    question: str = Field(description="要询问面试者的问题")

@tool(args_schema=AskUserTool)
def ask_user(question: str) -> str:
    """
    向面试者提出一个问题
    """
    answer = interrupt(question)
    return answer
