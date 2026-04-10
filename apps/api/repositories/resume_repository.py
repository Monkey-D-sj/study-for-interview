from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.models.resume_model import Resume
from packages.agents.resume.resume_agent import ResumeAnalysis


class ResumeRepository:
    """简历仓储"""

    @staticmethod
    async def save_resume(session: AsyncSession, resume_data: ResumeAnalysis) -> Resume:
        """
        保存简历

        Args:
            session: 数据库会话
            resume_data: 简历解析数据

        Returns:
            Resume: 保存的简历对象
        """
        resume = Resume(
            name=resume_data.name,
            position=resume_data.position,
            level=resume_data.level,
            tech_stack=resume_data.tech_stack,
            project_experiences=[
                {
                    "project_name": exp.project_name,
                    "project_description": exp.project_description,
                    "role_in_project": exp.role_in_project,
                    "technologies": exp.technologies,
                    "achievements": exp.achievements
                }
                for exp in resume_data.project_experiences
            ]
        )

        session.add(resume)
        await session.commit()
        await session.refresh(resume)

        return resume

    @staticmethod
    async def get_resume_by_id(session: AsyncSession, resume_id: int) -> Resume | None:
        """
        根据 ID 获取简历

        Args:
            session: 数据库会话
            resume_id: 简历 ID

        Returns:
            Resume | None: 简历对象
        """
        result = await session.execute(
            select(Resume).where(Resume.id == resume_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def list_resumes(session: AsyncSession, limit: int = 100) -> list[Resume]:
        """
        获取简历列表

        Args:
            session: 数据库会话
            limit: 返回数量限制

        Returns:
            list[Resume]: 简历列表
        """
        result = await session.execute(
            select(Resume).order_by(Resume.created_at.desc()).limit(limit)
        )
        return result.scalars().all()
