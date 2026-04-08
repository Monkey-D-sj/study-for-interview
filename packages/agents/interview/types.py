from enum import Enum
from typing import TypedDict, Literal, List, Annotated, \
    TypeAlias, Union, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

Level: TypeAlias = Literal["beginner", "intermediate", "advanced"]

class InterviewState(TypedDict):
    user_input: Annotated[str, lambda x, y: y] # 用户输入
    hr_question: Optional[str] # hr问题
    user_name: Optional[str] # 用户姓名
    position: Optional[str] # 用户职位
    level: Level
    tech_stack: Optional[str] # 技术栈

    # 第一轮面试
    base_passed: bool # 是否通过第一轮面试

    # 第二轮面试
    second_interview_question: Optional[str] # 第二轮面试问题
    second_interview_answer: Optional[str] # 第二轮面试答案
    second_interview_score: Optional[int] # 第二轮面试分数

    # 最终评估
    final_score: Optional[int] # 最终评估分数

    messages: Annotated[List[AnyMessage], add_messages]

class ConditionEnum(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    LOOP = "LOOP"