from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from ..domain.entities import ProjectStatus

Base = declarative_base()


class ProjectModel(Base):
    """SQLAlchemy model for Project"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(String(1000), nullable=True)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    github_url = Column(String(500), nullable=False)
    color = Column(String(7), default="#00d4aa", nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.ACTIVE, nullable=False)
    spent_seconds = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_entity(self):
        """Convert model to domain entity"""
        from ..domain.entities import Project
        return Project(
            id=self.id,
            name=self.name,
            description=self.description,
            start_date=self.start_date,
            github_url=self.github_url,
            color=self.color,
            status=self.status,
            spent_seconds=self.spent_seconds,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_entity(project):
        """Create model from domain entity"""
        return ProjectModel(
            id=project.id,
            name=project.name,
            description=project.description,
            start_date=project.start_date,
            github_url=project.github_url,
            color=project.color,
            status=project.status,
            spent_seconds=project.spent_seconds,
            created_at=project.created_at,
            updated_at=project.updated_at
        )
