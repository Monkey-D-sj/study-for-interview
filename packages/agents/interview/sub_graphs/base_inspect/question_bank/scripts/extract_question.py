import random
from pathlib import Path
from typing import List, Dict, Optional
import yaml

# 题库根目录
BASE_DIR = Path(__file__).parent.parent

def extract_question(
    bank: str,
    topic: str,
    level: str = "junior",
    count: int = 1,
    exclude: Optional[List[str]] = None
) -> List[Dict]:
	"""
	随机抽取题目

	Args:
		bank: 题库，如 frontend、backend
		topic: 题目主题，如 sql: List[str] = None): 已出题的ID列表，用于去重

	Returns:
		List[Dict]: 题目列表，格式:
			[
				{
					"id": "question1",
					"question": "HTTP 默认端口？",
					"standard_answer": "80",
					"level": "junior"
				},
				...
			]
	"""
	exclude = exclude or []

	# 构建题目文件路径：bank/topic/topic_level.yaml
	# 例如：frontend/http/http_junior.yaml
	topic_dir = BASE_DIR / bank / topic
	file_name = f"{topic}_{level}.yaml"
	file_path = topic_dir / file_name

	if not file_path.exists():
		raise FileNotFoundError(f"题库文件不存在: {file_path}")

	# 加载 YAML 文件
	with open(file_path, 'r', encoding='utf-8') as f:
		data = yaml.safe_load(f)

	if not data:
		return []

	# 过滤掉已出题的题目
	available_questions = [
		(q_id, q_data)
		for q_id, q_data in data.items()
		if q_id not in exclude
	]

	if not available_questions:
		return []

	# 随机抽取
	count = min(count, len(available_questions))
	selected = random.sample(available_questions, count)

	# 格式化返回结果
	result = []
	for q_id, q_data in selected:
		# q_data 是列表格式: [问题, 标准答案]
		if isinstance(q_data, list) and len(q_data) >= 2:
			result.append({
				"id": q_id,
				"question": q_data[0],
				"standard_answer": q_data[1],
				"level": level
			})

	return result