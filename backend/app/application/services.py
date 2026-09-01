from typing import List, Optional
from ..domain.entities import Project, ProjectStatus
from ..domain.repositories import ProjectRepository


class ProjectService:
    """Application service for Project operations"""

    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    async def create_project(
        self,
        name: str,
        description: str,
        github_url: str,
        color: str
    ) -> Project:
        """Create new project"""
        if not name or len(name.strip()) == 0:
            raise ValueError("Project name is required")
        
        if not github_url.startswith("https://github.com/"):
            raise ValueError("Invalid GitHub URL")
        
        project = Project(
            name=name,
            description=description,
            github_url=github_url,
            color=color
        )
        return await self.repository.add(project)

    async def get_all_projects(self) -> List[Project]:
        """Get all projects with elapsed time"""
        projects = await self.repository.get_all()
        return projects

    async def get_project(self, project_id: int) -> Optional[Project]:
        """Get project by ID"""
        return await self.repository.get_by_id(project_id)

    async def update_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        github_url: Optional[str] = None,
        color: Optional[str] = None,
        status: Optional[str] = None
    ) -> Project:
        """Update project"""
        project = await self.repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        if name:
            project.name = name
        if description:
            project.update_description(description)
        if github_url:
            project.update_github_url(github_url)
        if color:
            project.update_color(color)
        if status:
            project.change_status(ProjectStatus(status))

        return await self.repository.update(project)

    async def delete_project(self, project_id: int) -> bool:
        """Delete project"""
        return await self.repository.delete(project_id)

    async def add_spent_time(self, project_id: int, seconds: int) -> Project:
        """Add spent time to project"""
        project = await self.repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")
        project.add_spent_time(seconds)
        return await self.repository.update(project)

    async def change_status(self, project_id: int, new_status: str) -> Project:
        """Change project status"""
        project = await self.repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        project.change_status(ProjectStatus(new_status))
        return await self.repository.update(project)

    async def get_project_with_elapsed_time(self, project_id: int) -> dict:
        """Get project with calculated elapsed time"""
        project = await self.repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")
        
        elapsed = project.get_elapsed_time()
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "start_date": project.start_date,
            "github_url": project.github_url,
            "color": project.color,
            "status": project.status.value,
            "elapsed_time": elapsed,
            "spent_time": project.get_spent_time()
        }
