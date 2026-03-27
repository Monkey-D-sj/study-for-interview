from langchain_core.prompts import ChatPromptTemplate, \
    SystemMessagePromptTemplate

from packages.agents.teacher.model import teacher_model
from packages.agents.teacher.nodes.evaluate import \
    system_prompt
from packages.agents.teacher.state import TeacherState

practice_system_prompt = """
你是一个资深{position}面试官，需要你根据{topic}话题出一道题给面试者
"""

def practice(state: TeacherState) -> TeacherState:
    """出题"""
    chat_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(practice_system_prompt)
    ])
    messages = chat_template.format_messages(position=state["position"], topic=state["topic"])
    state["question"] = teacher_model.invoke(messages)
    return state
