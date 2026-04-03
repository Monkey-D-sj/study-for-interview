from langchain_core.messages import SystemMessage

from packages.agents.interview.model import get_model
from packages.agents.interview.sub_graphs.project_inspect.state import \
    ProjectInspectState

project_ask_system_prompt = """
你是一个资深{position}面试官，正在进行二面。
请让候选人介绍一个他最熟悉、最有挑战性的项目。

要求：
- 必须包含：项目背景、技术架构、你的职责、核心难点
- 如果描述过于简略，请主动追问细节
- 不要评价，只收集信息

你的风格：
- 冷静、专业
- 不提供提示
- 不帮候选人组织语言

输出一句话提问
"""


def project_ask_node(state: ProjectInspectState):
    messages = [
        SystemMessage(content=project_ask_system_prompt.format(position=state["position"])),
    ]
    model = get_model()
    response = model.invoke(messages)
    question = response.content
    return {
        "question": question,
        "dialogue_loop": 0
    }

