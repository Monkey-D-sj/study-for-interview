import json
from typing import Optional

from langgraph.types import interrupt
from pydantic import Field, BaseModel
from langchain_core.messages import SystemMessage, \
    HumanMessage, ToolMessage, AIMessage
from langgraph.config import get_stream_writer

from packages.agents.interview.model import get_teacher_model
from packages.agents.interview.state import TeacherState

intend_system_prompt = """
你是一个专业的HR，正在引导面试者填写信息。

目标：收集以下信息：
1. 姓名（user_name）
2. 面试岗位（position）
3. 面试职级（level）

规则：
- 你可以从用户输入中“提取已有信息”
- 如果信息缺失，需要自然地向用户提问
- 语气要像真人HR，简洁自然
"""

def intend_node(state: TeacherState) -> TeacherState:
    """
    询问面试者的意图
    """
    context = f"""
当前已知消息：
- 姓名：{state.get("user_name", "")}
- 面试岗位：{state.get("position", "")}
- 面试职级：{state.get("level", "")}
"""
    messages = [
        SystemMessage(content=intend_system_prompt),
        HumanMessage(content=context)
    ]

    model = get_teacher_model()
    response = model.invoke(messages)
    question = response.content

    return {
        "hr_question": question
    }

class IntendStructuredOutput(BaseModel):
    user_name: Optional[str] = None
    position: Optional[str] = None
    level: Optional[str] = None

def intend_input_node(state: TeacherState):
    answer = interrupt("")
    prompt = f"""
    请从问题{state["hr_question"]}评估回答{answer}是否是下面三个字段：
    1. 姓名（user_name）
    2. 面试岗位（position）
    3. 面试职级（level）
    如果有返回数据，没有就不返回
    """
    response = get_teacher_model().with_structured_output(IntendStructuredOutput).invoke([
        HumanMessage(content=prompt)
    ])

    if response.user_name:
        state["user_name"] = response.user_name
    if response.position:
        state["position"] = response.position
    if response.level:
        state["level"] = response.level

    return state

def finish_intend(state: TeacherState) -> str:
    if state.get("user_name") and state.get("position") and state.get("level"):
        writer = get_stream_writer()
        writer(f"欢迎{state["user_name"]}来面试{state["position"]}，那我们进入面试流程吧")
        return "continue"
    return "loop"

