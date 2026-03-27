from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate
from packages.agents.teacher.model import teacher_model
from packages.agents.teacher.state import TeacherState

system_prompt = """
你是一个专业的{position}面试官，负责评估面试候选人的回答。1-10分进行打分
问题：{question}
回答：{answer}
"""

def evaluate(state: TeacherState) -> TeacherState:
    """
    评估用户回答
    """
    chat_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt)
    ])
    messages = chat_template.format_messages(position=state["position"],
                                            question=state["question"],
                                            answer=state["answer"])
    state["evaluation"] = teacher_model.invoke(messages)
    return state
