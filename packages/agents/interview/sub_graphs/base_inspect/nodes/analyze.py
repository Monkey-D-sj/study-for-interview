from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate
from langgraph.config import get_stream_writer
from pydantic import BaseModel, Field

from packages.agents.interview.model import get_model
from packages.agents.interview.sub_graphs.base_inspect.state import \
	BaseInspectState
from packages.agents.interview.types import InterviewState, \
	ConditionEnum

system_prompt = """
你是一个专业的{position}面试官，负责评估面试候选人的回答。0-10分进行打分
问题：{question}
标准答案：{standard_answer}
回答：{answer}
"""

class EvaluateResult(BaseModel):
	score: int = Field(description="评估分数，0-10分")

def analyze_base_node(state: BaseInspectState):
	"""
	评估用户回答
	"""
	chat_template = ChatPromptTemplate.from_messages([
		SystemMessagePromptTemplate.from_template(system_prompt)
	])
	last_result = state["results"][-1]
	messages = chat_template.format_messages(position=state["position"],
											question=last_result["question"],
											standard_answer=last_result["standard_answer"],
											answer=last_result["answer"])
	model = get_model().with_structured_output(EvaluateResult)
	response = model.invoke(messages)
	score = response.score
	passed_question_count = state["passed_question_count"] if score <= 6 else state["passed_question_count"] + 1

	writer = get_stream_writer()
	writer(f"评估分数：{score}")
	state["results"][-1]["score"] = score

	return {
		"passed_question_count": passed_question_count
	}

def is_passed(state: BaseInspectState):
	"""
	判断是否通过
	"""
	if state["passed_question_count"] >= 3:
		return ConditionEnum.PASS
	return ConditionEnum.LOOP
