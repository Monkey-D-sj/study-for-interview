from pydantic import BaseModel
from typing import Optional

from packages.agents.resume.resume_agent import ProjectExperience, ResumeAnalysis


class PDFReadResponse(BaseModel):
    """
    PDF 读取响应
    """
    success: bool
    content: str = None
    page_count: int = None
    error: str = None


class ResumeParseResponse(BaseModel):
    """
    简历解析响应
    """
    success: bool
    data: Optional[ResumeAnalysis] = None
    resume_id: Optional[int] = None
    error: str = None
