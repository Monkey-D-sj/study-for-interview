import operator
from typing import List, TypedDict, Optional, Annotated


class BaseResult(TypedDict):
	question: str # 问题
	answer: str # 回答
	score: Optional[int] # 分数

class BaseInspectState(TypedDict):
	position: str # 岗位
	results: Annotated[List[BaseResult], operator.add] # 结果
	passed_question_count: int # 通过问题数量

	is_passed: bool # 最终是否通过
