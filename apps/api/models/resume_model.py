from sqlalchemy import Column, String, Integer, JSON, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
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

    sessions = relationship("Session", back_populates="resume", cascade="all, delete-orphan")


class Session(Base):
    """对话会话表"""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, comment="关联简历ID")
    title = Column(String(255), nullable=False, comment="对话标题")
    status = Column(String(50), default="active", comment="状态: active/archived/deleted")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    resume = relationship("Resume", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")


class Message(Base):
    """对话消息表"""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, comment="关联会话ID")
    role = Column(String(20), nullable=False, comment="角色: user/assistant/system")
    content = Column(Text, nullable=False, comment="消息内容")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")

    session = relationship("Session", back_populates="messages")

    __table_args__ = (
        Index("idx_messages_session_id", "session_id"),
    )
