from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Project


class ProjectRepository(ABC):
    """Abstract repository for Project entity"""

    @abstractmethod
    async def add(self, project: Project) -> Project:
        """Add a new project"""
        pass

    @abstractmethod
    async def get_by_id(self, project_id: int) -> Optional[Project]:
        """Get project by ID"""
        pass

    @abstractmethod
    async def get_all(self) -> List[Project]:
        """Get all projects"""
        pass

    @abstractmethod
    async def update(self, project: Project) -> Project:
        """Update existing project"""
        pass

    @abstractmethod
    async def delete(self, project_id: int) -> bool:
        """Delete project by ID"""
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Project]:
        """Get project by name"""
        pass
