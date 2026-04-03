from langgraph.checkpoint.memory import InMemorySaver

from packages.agents.interview.sub_graphs.project_inspect.graph import \
	project_inspect_sub_graph
from langgraph.types import Command

config = {
 "configurable": {
  "thread_id": "1"
 }
}
# 导出Mermaid代码
mermaid_code = project_inspect_sub_graph.get_graph().draw_mermaid()
# 保存到文件
with open("graph.mmd", "w") as f:
	f.write(mermaid_code)
response = project_inspect_sub_graph.invoke({
	"position": "ai应用工程师"
}, config=config)

while response:
	print(response)
	if "__interrupt__" in response:
		answer = input(f"请输入：")
		response = project_inspect_sub_graph.invoke(Command(resume=answer), config=config)
	else:
		response = None