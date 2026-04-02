from enum import Enum
from typing import TypedDict, Literal, List, Annotated, \
    TypeAlias, Union, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class InterviewState(TypedDict):
    user_input: Annotated[str, lambda x, y: y] # 用户输入
    hr_question: Optional[str] # hr问题
    user_name: Optional[str] # 用户姓名
    position: Optional[str] # 用户职位
    level: Literal["beginner", "intermediate", "advanced"]
    tech_stack: Optional[str] # 技术栈

    # 第一轮面试
    question_count: int # 轮数
    current_count: int # 当前轮数
    passed_question_count: int # 通过数


    question: Optional[str] # 问题
    standard_answer: Optional[str] # 标准答案
    answer: Optional[str] # 用户回答
    score: Optional[int] # 评估分数

    messages: Annotated[List[AnyMessage], add_messages]

class ConditionEnum(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    LOOP = "LOOP"