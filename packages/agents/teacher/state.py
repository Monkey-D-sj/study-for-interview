from typing import TypedDict, Literal, List, Annotated, \
    TypeAlias, Union
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class TeacherState(TypedDict):
    user_input: str # 用户输入
    user_name: str # 用户姓名
    position: str # 用户职位
    level: Literal["beginner", "intermediate", "advanced"]
    topic: str # 话题

    question: str # 问题
    answer: str # 回答
    evaluation: str # 评估

    messages: Annotated[List[AnyMessage], add_messages]
