from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate
from langgraph.config import get_stream_writer
from pydantic import BaseModel, Field

from packages.agents.interview.model import get_teacher_model
from packages.agents.interview.state import TeacherState

system_prompt = """
你是一个专业的{position}面试官，负责评估面试候选人的回答。1-10分进行打分
问题：{question}
标准答案：{standard_answer}
回答：{answer}
"""

class EvaluateResult(BaseModel):
    score: int = Field(description="评估分数，1-10分")

def evaluate(state: TeacherState) -> TeacherState:
    """
    评估用户回答
    """
    chat_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt)
    ])
    messages = chat_template.format_messages(position=state["position"],
                                            question=state["question"],
                                            standard_answer=state["standard_answer"],
                                            answer=state["answer"])  + [ HumanMessage(content="请出一道题") ]
    model = get_teacher_model().with_structured_output(EvaluateResult)
    response = model.invoke(messages)
    print(response)
    state["messages"].append(AIMessage(content=f"""
    评估分数：{response.score}
    """))
    writer = get_stream_writer()
    writer(f"评估分数：{response.score}")
    state["score"] = response.score
    return state

def evaluate_pass(state: TeacherState) -> str:
    writer = get_stream_writer()
    if state["score"] >= 6:
        writer("面试通过")
        return "pass"
    else:
        writer("面试不通过")
        return "fail"
