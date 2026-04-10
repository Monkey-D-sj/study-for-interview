from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate
from langgraph.config import get_stream_writer
from pydantic import BaseModel, Field

from packages.infra.models.model import get_model
from packages.agents.interview.sub_graphs.base_inspect.state import \
	BaseInspectState
from packages.agents.interview.types import ConditionEnum

system_prompt = """
你是一个专业的{position}面试官，负责评估面试候选人的回答。0-10分进行打分
问题：{question}
标准答案：{standard_answer}
回答：{answer}
"""

class EvaluateResult(BaseModel):
	score: int = Field(description="评估分数，0-10分")

def save_exam_question(question: str, answer: str, standard_answer: str, score: int):
	"""
	保存评分低的考试问题
	Args:
		question: 问题
		answer: 回复
		standard_answer: 标准答案
		score: 评分
	"""
	with open('exam_questions.jsonl', 'a', encoding="utf-8") as f:
		f.write(f'{{question: "{question}", answer: "{answer}", standard_answer: "{standard_answer}", score: "{score}"}}\n')

def analyze_base_node(state: BaseInspectState):
	"""
	评估用户回答
	"""
	chat_template = ChatPromptTemplate.from_messages([
		SystemMessagePromptTemplate.from_template(system_prompt)
	])

	question = state["question"]
	standard_answer = state["standard_answer"]
	answer = state["answer"]

	messages = chat_template.format_messages(position=state["position"],
											question=question,
											standard_answer=standard_answer,
											answer=answer)
	model = get_model().with_structured_output(EvaluateResult)
	response = model.invoke(messages)
	score = response.score
	passed_question_count = state["passed_question_count"]

	writer = get_stream_writer()
	writer(f"评估分数：{score}")

	if score < 6:
		save_exam_question(question=question, standard_answer=standard_answer, score=score, answer=answer)
	else:
		passed_question_count += 1

	return {
		"passed_question_count": passed_question_count,
		"score": score
	}

def is_passed(state: BaseInspectState):
	"""
	判断是否通过
	"""
	if state["passed_question_count"] >= 3:
		return ConditionEnum.PASS
	return ConditionEnum.LOOP
