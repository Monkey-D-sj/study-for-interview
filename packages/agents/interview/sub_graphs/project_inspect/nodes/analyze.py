from typing import List
from pydantic import BaseModel, Field

from packages.agents.interview.model import get_model
from packages.agents.interview.sub_graphs.project_inspect.state import \
	ProjectInspectState
from packages.agents.interview.types import ConditionEnum

analyze_project_system_prompt = """
你是一个资深技术面试官，正在评估候选人的回答质量。

请基于以下信息进行分析：

【问题】
{question}

【候选人回答】
{answer}

请从以下维度分析：

1. 技术深度（0-10）
2. 真实性（0-10，是否像真实做过）
3. 表达清晰度（0-10）

并识别问题：
- 是否存在“泛泛而谈”
- 是否存在“背诵痕迹”
- 是否缺少关键细节
- 是否有明显漏洞

最后给出：
- 是否需要继续追问（true/false）
- 推荐追问方向（具体到技术点）

输出 JSON：
"""

class AnalyzeProjectResult(BaseModel):
	score: int = Field(description="技术深度、真实性、表达清晰度")
	exist_question: List[str] = Field(description="问题")
	continue_ask: bool = Field(description="是否需要继续追问")
	ask_direction: str = Field(description="追问方向")


def analyze_node(state: ProjectInspectState):
	"""
	分析项目经验
	"""
	system_prompt = analyze_project_system_prompt.format(
		question=state["question"],
		answer=state["answer"]
	)
	model = get_model().with_structured_output(AnalyzeProjectResult)
	response = model.invoke(system_prompt)

	return {
		"score": response.score,
		"exist_question": response.exist_question,
		"continue_ask": response.continue_ask,
		"ask_direction": response.ask_direction
	}

def finish_node(state: ProjectInspectState):
	if state["dialogue_loop"] < 20:
		return ConditionEnum.LOOP
	else:
		return ConditionEnum.PASS
