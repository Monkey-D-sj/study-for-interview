import operator
from typing import List, TypedDict, Optional, Annotated
from packages.agents.interview.types import Level

class BaseInspectState(TypedDict):
	position: str # 岗位
	level: Level # 职级 (junior, mid, senior)

	id: str  # 题目ID
	question: str  # 问题
	standard_answer: str  # 标准答案
	answer: str  # 回答
	score: Optional[int]  # 分数

	total_question_count: int # 总问题数量
	passed_question_count: int # 通过问题数量
	used_question_ids: Annotated[List[str], operator.add] # 已出题的题目ID，用于去重

	is_passed: bool # 最终是否通过
