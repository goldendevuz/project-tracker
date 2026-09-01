from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..domain.entities import Project
from ..domain.repositories import ProjectRepository
from .models import ProjectModel


class SQLAlchemyProjectRepository(ProjectRepository):
    """SQLAlchemy implementation of ProjectRepository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, project: Project) -> Project:
        """Add new project"""
        model = ProjectModel.from_entity(project)
        self.session.add(model)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(model)
        return model.to_entity()

    async def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by ID"""
        result = await self.session.execute(
            select(ProjectModel).where(ProjectModel.id == project_id)
        )
        model = result.scalars().first()
        return model.to_entity() if model else None

    async def get_all(self) -> List[Project]:
        """Get all projects"""
        result = await self.session.execute(select(ProjectModel))
        models = result.scalars().all()
        return [model.to_entity() for model in models]

    async def update(self, project: Project) -> Project:
        """Update project"""
        result = await self.session.execute(
            select(ProjectModel).where(ProjectModel.id == project.id)
        )
        model = result.scalars().first()
        
        if not model:
            raise ValueError(f"Project {project.id} not found")

        model.name = project.name
        model.description = project.description
        model.github_url = project.github_url
        model.color = project.color
        model.status = project.status
        model.spent_seconds = project.spent_seconds
        model.updated_at = project.updated_at

        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(model)
        return model.to_entity()

    async def delete(self, project_id: int) -> bool:
        """Delete project"""
        result = await self.session.execute(
            select(ProjectModel).where(ProjectModel.id == project_id)
        )
        model = result.scalars().first()
        
        if not model:
            return False

        await self.session.delete(model)
        await self.session.flush()
        await self.session.commit()
        return True

    async def get_by_name(self, name: str) -> Optional[Project]:
        """Get project by name"""
        result = await self.session.execute(
            select(ProjectModel).where(ProjectModel.name == name)
        )
        model = result.scalars().first()
        return model.to_entity() if model else None
