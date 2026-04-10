from typing import Optional, List
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage

from packages.infra.models.model import get_light_model


class ProjectExperience(BaseModel):
    """项目经验"""
    project_name: str = Field(description="项目名称")
    project_description: str = Field(description="项目描述")
    role_in_project: str = Field(description="在项目中的角色")
    technologies: List[str] = Field(description="项目中使用的技术栈")
    achievements: Optional[str] = Field(description="项目成果", default="")


class ResumeAnalysis(BaseModel):
    """简历解析结果"""
    name: str = Field(description="姓名")
    position: str = Field(description="应聘岗位")
    level: str = Field(description="职级，如 junior/mid/senior")
    tech_stack: List[str] = Field(description="技术栈列表")
    project_experiences: List[ProjectExperience] = Field(description="项目经验列表")


RESUME_SYSTEM_PROMPT = """
你是一个专业的简历解析助手。请从给定的简历文本中提取关键信息，并以结构化格式输出。

需要提取的信息：
1. 姓名：简历中提供的姓名
2. 应聘岗位：简历中提到的应聘职位
3. 职级：根据经验判断，如 junior（初级）、mid（中级）、senior（高级）
4. 技术栈：候选人的技术能力列表
5. 项目经验：候选人参与的项目列表，每个项目包含：
   - 项目名称
   - 项目描述
   - 在项目中的角色
   - 项目中使用的技术栈
   - 项目成果

注意：
- 如果某项信息无法从简历中提取，请使用合理的默认值或空字符串
- 技术栈应该是一个清晰的列表
- 项目经验应该完整且结构化
"""


def parse_resume(resume_content: str) -> ResumeAnalysis:
    """
    解析简历内容，提取结构化信息

    Args:
        resume_content: 简历的文本内容

    Returns:
        ResumeAnalysis: 解析后的简历信息
    """
    messages = [
        SystemMessage(content=RESUME_SYSTEM_PROMPT),
        HumanMessage(content=f"请解析以下简历内容：\n\n{resume_content}")
    ]

    model = get_light_model()
    structured_model = model.with_structured_output(ResumeAnalysis)

    result = structured_model.invoke(messages)
    return result


# 导出函数供外部使用
__all__ = ["parse_resume", "ResumeAnalysis", "ProjectExperience"]
