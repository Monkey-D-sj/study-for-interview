from typing import Union, Dict, List
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, \
    SystemMessagePromptTemplate
from langgraph.config import get_stream_writer
from langgraph.types import interrupt
from pydantic import BaseModel, Field

from packages.agents.interview.model import get_teacher_model
from packages.agents.interview.state import TeacherState
from packages.infra.utils.stream_tag_interceptor import \
    StreamTagInterceptor
from packages.infra.utils.utils import parse_xml

QUESTION_TAG = 'QUESTION'
STANDARD_ANSWER_TAG = '<STANDARDANSWER>'

practice_system_prompt = """
你是一个资深{position}面试官，需要你根据岗位{level}等级，出一道常识题给面试者，并给出标准答案
例如：
<{QUESTION_TAG}>
http状态码304代表什么
</{QUESTION_TAG}>
<{STANDARD_ANSWER_TAG}>
资源未修改
</{STANDARD_ANSWER_TAG}>

要求
- 直接返回如例子所示**xml**格式数据
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
        level=state["level"],
        QUESTION_TAG=QUESTION_TAG,
        STANDARD_ANSWER_TAG=STANDARD_ANSWER_TAG
    ) + [
        HumanMessage(content="请出一道题")
    ]

    model = get_teacher_model()
    interceptor = StreamTagInterceptor(QUESTION_TAG)
    full_content = ''
    writer = get_stream_writer()
    for chunk in model.stream(messages):
        content = chunk.content
        full_content += content
        visible = interceptor.feed(content)
        if visible:
            print('visible', visible)
            writer(visible)

    print('fullcontent', full_content)
    question = parse_xml(full_content, QUESTION_TAG)
    standard_answer = parse_xml(full_content, STANDARD_ANSWER_TAG)

    state["question"] = question
    state["standard_answer"] = standard_answer

    return state

def collect_answer(state: TeacherState) -> TeacherState:
    """收集用户回答"""
    answer = interrupt("")
    state["answer"] = answer
    state["messages"].append(HumanMessage(content=answer))
    return state
