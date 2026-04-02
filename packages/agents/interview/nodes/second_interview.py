from packages.agents.interview.types import InterviewState


second_interview_system_prompt = """
你是一个资深{position}面试官，需要你根据岗位{level}等级，对用户项目经验进行评估
需要询问项目经验
"""

def second_interview(state: InterviewState) -> InterviewState:
	"""
	第二次面试，询问项目经验
	"""
	return state