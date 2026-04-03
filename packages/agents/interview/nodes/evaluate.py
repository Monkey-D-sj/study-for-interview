from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate
from langgraph.config import get_stream_writer
from pydantic import BaseModel, Field

from packages.agents.interview.model import get_model
from packages.agents.interview.types import InterviewState

system_prompt = """
你是一个专业的{position}面试官，负责评估面试候选人的回答。0-10分进行打分
问题：{question}
标准答案：{standard_answer}
回答：{answer}
"""

class EvaluateResult(BaseModel):
    score: int = Field(description="评估分数，0-10分")

def evaluate(state: InterviewState):
    """
    评估用户回答
    """
    chat_template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt)
    ])
    messages = chat_template.format_messages(position=state["position"],
                                            question=state["question"],
                                            standard_answer=state["standard_answer"],
                                            answer=state["answer"])  + [ HumanMessage(content="请评分") ]
    model = get_model().with_structured_output(EvaluateResult)
    response = model.invoke(messages)
    score = response.score
    passed_question_count = state["passed_question_count"] if score <= 6 else state["passed_question_count"] + 1

    writer = get_stream_writer()
    writer(f"评估分数：{score}")

    return {
        "score": score,
        "passed_question_count": passed_question_count
    }

