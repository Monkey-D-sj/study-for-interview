from typing import Union, Dict, List

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import \
    JsonOutputToolsParser

from langchain_core.prompts import ChatPromptTemplate, \
    SystemMessagePromptTemplate
from langgraph.types import interrupt
from pydantic import BaseModel, Field

from packages.agents.interview.model import get_teacher_model
from packages.agents.interview.state import TeacherState

practice_system_prompt = """
你是一个资深{position}面试官，需要你根据岗位{level}等级，出一道常识题给面试者，并给出标准答案
例如：
question: http状态码304代表什么
standard_answer: 资源未修改
"""

class PracticeStructuredOutput(BaseModel):
    question: Union[str, Dict, List] = Field(description="面试题")
    standard_answer: Union[str, Dict, List] = Field(description="标准答案")

def examiner(state: TeacherState) -> TeacherState:
    """出题"""
    chat_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(practice_system_prompt)
    ])
    messages = chat_template.format_messages(
        position=state["position"],
        level=state["level"]
    ) + [
        HumanMessage(content="请出一道题")
    ]

    parser = JsonOutputToolsParser()
    model = get_teacher_model().with_structured_output(PracticeStructuredOutput)
    response = model.pipe(parser).invoke(messages)

    question = response.question
    standard_answer = response.standard_answer

    state["question"] = question
    state["standard_answer"] = standard_answer

    return {
        "question": question,
        "standard_answer": standard_answer,
    }

def collect_answer(state: TeacherState) -> TeacherState:
    """收集用户回答"""
    answer = interrupt(f"请回答：{state['question']}")
    state["answer"] = answer
    state["messages"].append(HumanMessage(content=answer))
    return state
