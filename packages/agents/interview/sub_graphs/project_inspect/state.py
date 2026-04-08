from typing import TypedDict

class ProjectInspectState(TypedDict):
	position: str # 职位
	question: str # 问题
	answer: str # 回复

	score: int # 评估分数
	exist_question: str # 存在问题
	continue_ask: bool # 是否需要继续追问
	ask_direction: str # 追问方向

	dialogue_loop: int # 对话循环次数
