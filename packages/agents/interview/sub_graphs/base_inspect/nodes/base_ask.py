from langgraph.config import get_stream_writer

from packages.agents.interview.sub_graphs.base_inspect.state import \
	BaseInspectState, BaseResult

# 岗位到题库的映射
POSITION_TO_BANK = {
	"后端": "backend",
	"backend": "backend",
	"前端": "frontend",
	"frontend": "frontend",
}

# 职级到英文的映射
LEVEL_MAP = {
	"初级": "junior",
	"初级工程师": "junior",
	"1-3年": "junior",
	"中级": "mid",
	"中级工程师": "mid",
	"3-5年": "mid",
	"高级": "senior",
	"高级工程师": "senior",
	"5-10年": "senior",
}

# 支持的主题
TOPICS = ["http", "sql", "algorithm", "database", "network"]

def base_ask_node(state: BaseInspectState):
	"""
	基础问题节点 - 从题库抽取题目
	"""
	writer = get_stream_writer()

	# 获取岗位和职级
	position = state.get("position", "")
	level = state.get("level", "junior")

	# 映射到题库和英文职级
	bank = POSITION_TO_BANK.get(position.lower(), "frontend")
	english_level = LEVEL_MAP.get(level, "junior")

	# 获取已出题ID列表
	exclude = state.get("used_question_ids", [])

	# 随机选择一个主题（后续可以根据岗位定制主题）
	topic = "http" if bank == "frontend" else "sql"

	# 导入抽取函数
	from packages.agents.interview.sub_graphs.base_inspect.question_bank.scripts.extract_question import extract_question

	try:
		questions = extract_question(
			bank=bank,
			topic=topic,
			level=english_level,
			count=1,
			exclude=exclude
		)

		if not questions:
			writer("题库中暂无题目，跳过此题")
			return {
				"results": [{
					"id": "",
					"question": "题库暂无可用题目",
					"standard_answer": "",
					"answer": "",
					"score": None
				}]
			}

		q = questions[0]
		question_text = q["question"]

		# 流式输出问题（模拟打字效果）
		for char in question_text:
			writer(char)

		# 返回结果
		result: BaseResult = {
			"id": q["id"],
			"question": q["question"],
			"standard_answer": q["standard_answer"],
			"answer": "",
			"score": None
		}

		# 更新已出题ID列表
		new_used_ids = [q["id"]]

		return {
			"results": [result],
			"used_question_ids": new_used_ids
		}

	except FileNotFoundError as e:
		writer(f"题库文件不存在: {e}")
		return {
			"results": [{
				"id": "",
				"question": "题库文件不存在",
				"standard_answer": "",
				"answer": "",
				"score": None
			}]
		}
	except Exception as e:
		writer(f"抽取题目失败: {e}")
		return {
			"results": [{
				"id": "",
				"question": f"抽题失败: {str(e)}",
				"standard_answer": "",
				"answer": "",
				"score": None
			}]
		}
