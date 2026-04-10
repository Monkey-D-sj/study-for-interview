from sqlalchemy import Column, String, Integer, JSON, DateTime
from sqlalchemy.sql import func
from apps.api.db.pg_client import Base


class Resume(Base):
    """简历表"""
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="姓名")
    position = Column(String(100), nullable=False, comment="应聘岗位")
    level = Column(String(50), nullable=False, comment="职级")
    tech_stack = Column(JSON, nullable=False, comment="技术栈")
    project_experiences = Column(JSON, nullable=False, comment="项目经验")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
