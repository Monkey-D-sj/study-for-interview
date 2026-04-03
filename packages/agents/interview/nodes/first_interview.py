from typing import Union, Dict, List
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, \
    SystemMessagePromptTemplate
from langgraph.config import get_stream_writer
from langgraph.types import interrupt

from packages.agents.interview.model import get_model
from packages.agents.interview.types import InterviewState, \
    ConditionEnum
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

def first_interview(state: InterviewState):
    """
    第一次面试，根据技术栈出八股文
    """
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

    model = get_model()
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

    question = parse_xml(full_content, QUESTION_TAG)
    standard_answer = parse_xml(full_content, STANDARD_ANSWER_TAG)

    state["question"] = question
    state["standard_answer"] = standard_answer

    return state

def collect_answer():
    """收集用户回答"""
    answer = interrupt("")
    return {
        "answer": answer,
    }

def finish_first_interview(state: InterviewState) -> str:
    if state["current_count"] < state["question_count"]:
        return ConditionEnum.LOOP
    if state["passed_question_count"] / state["question_count"] > 0.6:
        return ConditionEnum.PASS
    get_stream_writer()("回去等通知把")
    return ConditionEnum.FAIL