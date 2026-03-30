import json
from pydantic import Field, BaseModel
from langchain_core.messages import SystemMessage, \
    HumanMessage, ToolMessage
from langgraph.config import get_stream_writer

from packages.agents.teacher.model import teacher_model
from packages.agents.teacher.state import TeacherState
from langchain_core.tools import tool
from langgraph.types import interrupt


class AskUserTool(BaseModel):
    question: str = Field(description="要询问面试者的问题")
    is_finish: bool = Field(description="是否结束对话")
    level: str = Field(description="面试职级")
    position: str = Field(description="面试岗位")
    user_name: str = Field(description="面试者姓名")

@tool(args_schema=AskUserTool)
def ask_user(question: str, is_finish: bool, level: str, position: str, user_name: str) -> str:
    """
    向面试者提出一个问题
    """
    if is_finish:
        return f"收集完毕：姓名={user_name}, 岗位={position}, 职级={level}"
    print('ask_user question:', question)
    answer = interrupt(question)
    print('ask_user answer:', answer)
    return answer

intend_system_prompt = """
你是一个HR，擅长通过语言引导面试者，了解面试者的面试信息。

你必须严格按照以下规范进行操作：
- 只能通过**ask_user** 工具，来询问面试者信息
- 每次调用 **ask_user** 时，只能询问一个信息点，不得在单次调用中询问多个信息。
- 你必须依次获取以下三项信息，顺序为：
    - 面试者姓名
    - 面试岗位
    - 面试职级（必须是["beginner", "intermediate", "advanced"]中的一个）
- 当三项信息全部获取后，调用 ask_user 并设置 is_finish=True，同时填入 user_name、position、level
- 返回信息必须是JSON格式，包含以下3个字段：
    - level: 面试职级（必须是["beginner", "intermediate", "advanced"]中的一个）
    - position: 面试岗位
    - user_name: 面试者姓名


# 禁止
- 不能在单次 **ask_user** 中询问多个信息
- 不能跳过或调整信息获取顺序。
"""

def intend_node(state: TeacherState) -> TeacherState:
    """
    询问面试者的意图
    """
    messages = state.get("messages", [])
    if not messages:
        messages = [
            SystemMessage(content=intend_system_prompt),
        ]
    if state.get("user_input") and not state.get("messages"):
        messages.append(HumanMessage(content=state["user_input"]))

    model_with_tools = teacher_model.bind_tools([ask_user])

    writer = get_stream_writer()

    # 收集完整的响应
    response = model_with_tools.invoke(messages)
    writer(response.content)
    messages.append(response)
    state["messages"] = messages
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        args = tool_call['args']
        question = tool_call['args']['question']
        writer(question)

        if args["is_finish"]:
            state["user_name"] = args["user_name"]
            state["position"] = args["position"]
            state["level"] = args["level"]

    return state

def finish_intend(state: TeacherState) -> str:
    if state.get("user_name") and state.get("position") and state.get("level"):
        return "continue"
    return "loop"

