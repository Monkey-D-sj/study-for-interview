from typing import TypedDict, Literal, List, Annotated, \
    TypeAlias, Union, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class TeacherState(TypedDict):
    user_input: Annotated[str, lambda x, y: y] # 用户输入
    hr_question: Optional[str] # hr问题
    user_name: Optional[str] # 用户姓名
    position: Optional[str] # 用户职位
    level: Literal["beginner", "intermediate", "advanced"]
    topic: Optional[str] # 话题

    question: Optional[str] # 问题
    standard_answer: Optional[str] # 标准答案
    answer: Optional[str] # 用户回答
    score: Optional[int] # 评估分数

    messages: Annotated[List[AnyMessage], add_messages]
