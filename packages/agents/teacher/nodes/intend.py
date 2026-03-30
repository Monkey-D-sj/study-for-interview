from pydantic import Field, BaseModel
from langchain_core.messages import SystemMessage, \
    HumanMessage, ToolMessage
from langgraph.config import get_stream_writer

from packages.agents.teacher.model import teacher_model
from packages.agents.teacher.state import TeacherState
from packages.tools.ask import ask_user

intend_system_prompt = """
你是一个HR，擅长通过语言引导面试者，了解面试者的面试信息。

你必须严格按照以下规范进行操作：
- 只能通过**ask_user** 工具，来询问面试者信息
- 每次调用 **ask_user** 时，只能询问一个信息点，不得在单次调用中询问多个信息。
- 你必须依次获取以下三项信息，顺序为：
    - 面试者姓名
    - 面试岗位
    - 面试职级（必须是["beginner", "intermediate", "advanced"]中的一个）
- 当三项信息全部获取后，你可以结束对话或进行下一步操作，但仍不得输出无关内容

# 禁止
- 不能在单次 **ask_user** 中询问多个信息
- 不能输出任何非 **ask_user** 调用的文本（包括解释、问候、总结等）
- 不能跳过或调整信息获取顺序。
"""

class IntendStructOutput(BaseModel):
    user_name: str = Field(description="用户姓名")
    level: str = Field(description="岗位职级")
    position: str = Field(description="岗位")

def intend_node(state: TeacherState) -> TeacherState:
    """
    询问面试者的意图
    """
    messages = state.get("history", [])
    if not messages:
        messages = [
            SystemMessage(content=intend_system_prompt),
        ]
    messages = messages + [
        HumanMessage(content=state["user_input"])
    ]

    model_with_tools = teacher_model.bind_tools([ask_user], response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "输出格式",
            "schema": IntendStructOutput.model_json_schema(),
        },
    })

    writer = get_stream_writer()

    # 收集完整的响应
    response = model_with_tools.invoke(messages)
    print(response)
    messages.append(response)
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        question = tool_call['args']['question']
        writer(question)
        answer = ask_user.invoke(question)
        messages.append(ToolMessage(content=answer))

    if response.user_name:
        state["user_name"] = response.user_name
    if response.position:
        state["position"] = response.position
    if response.level:
        state["level"] = response.level

    return state

def finish_intend(state: TeacherState) -> str:
    print('llll')
    if state.get("user_name") and state.get("position") and state.get("level"):
        return "continue"
    return "loop"
