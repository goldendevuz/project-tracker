from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..infrastructure.db import get_session
from ..infrastructure.repositories import SQLAlchemyProjectRepository
from ..application.services import ProjectService
from ..application.dto import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
    ProjectResponse,
    ProjectListResponse,
    StatusChangeRequest,
    ElapsedTime,
    SpentTimeAddRequest
)

router = APIRouter(prefix="/api/projects", tags=["projects"])


async def get_project_service(session: AsyncSession = Depends(get_session)) -> ProjectService:
    """Dependency to get project service"""
    repository = SQLAlchemyProjectRepository(session)
    return ProjectService(repository)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    request: ProjectCreateRequest,
    service: ProjectService = Depends(get_project_service)
):
    """Create new project"""
    try:
        project = await service.create_project(
            name=request.name,
            description=request.description,
            github_url=request.github_url,
            color=request.color
        )
        elapsed = project.get_elapsed_time()
        spent = project.get_spent_time()
        return ProjectResponse(
            **{
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "start_date": project.start_date,
                "github_url": project.github_url,
                "color": project.color,
                "status": project.status.value,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
                "elapsed_time": ElapsedTime(**elapsed),
                "spent_time": ElapsedTime(**spent)
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=ProjectListResponse)
async def get_all_projects(service: ProjectService = Depends(get_project_service)):
    """Get all projects"""
    projects = await service.get_all_projects()
    project_responses = []
    
    for project in projects:
        elapsed = project.get_elapsed_time()
        spent = project.get_spent_time()
        project_responses.append(
            ProjectResponse(
                id=project.id,
                name=project.name,
                description=project.description,
                start_date=project.start_date,
                github_url=project.github_url,
                color=project.color,
                status=project.status.value,
                created_at=project.created_at,
                updated_at=project.updated_at,
                elapsed_time=ElapsedTime(**elapsed),
                spent_time=ElapsedTime(**spent)
            )
        )
    
    return ProjectListResponse(projects=project_responses, total=len(project_responses))



@router.get("/export/all")
async def export_projects(service: ProjectService = Depends(get_project_service)):
    """Export all projects as JSON"""
    projects = await service.get_all_projects()
    project_list = []
    for project in projects:
        project_list.append({
            "name": project.name,
            "description": project.description,
            "github_url": project.github_url,
            "color": project.color,
            "status": project.status.value,
        })
    return project_list

@router.post("/import/all")
async def import_projects(
    projects: List[ProjectCreateRequest],
    service: ProjectService = Depends(get_project_service)
):
    """Import projects from JSON"""
    count = 0
    for proj in projects:
        try:
            p = await service.create_project(
                name=proj.name,
                description=proj.description,
                github_url=proj.github_url,
                color=proj.color
            )
            count += 1
        except Exception as e:
            print(f"Error importing {proj.name}: {e}")
    return {"imported": count}

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    """Get project by ID"""
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    elapsed = project.get_elapsed_time()
    spent = project.get_spent_time()
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        start_date=project.start_date,
        github_url=project.github_url,
        color=project.color,
        status=project.status.value,
        created_at=project.created_at,
        updated_at=project.updated_at,
        elapsed_time=ElapsedTime(**elapsed),
        spent_time=ElapsedTime(**spent)
    )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    request: ProjectUpdateRequest,
    service: ProjectService = Depends(get_project_service)
):
    """Update project"""
    try:
        project = await service.update_project(
            project_id,
            name=request.name,
            description=request.description,
            github_url=request.github_url,
            color=request.color,
            status=request.status
        )
        elapsed = project.get_elapsed_time()
        spent = project.get_spent_time()
        return ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            start_date=project.start_date,
            github_url=project.github_url,
            color=project.color,
            status=project.status.value,
            created_at=project.created_at,
            updated_at=project.updated_at,
            elapsed_time=ElapsedTime(**elapsed),
            spent_time=ElapsedTime(**spent)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service)
):
    """Delete project"""
    success = await service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")


@router.patch("/{project_id}/status", response_model=ProjectResponse)
async def change_status(
    project_id: int,
    request: StatusChangeRequest,
    service: ProjectService = Depends(get_project_service)
):
    """Change project status"""
    try:
        project = await service.change_status(project_id, request.status)
        elapsed = project.get_elapsed_time()
        spent = project.get_spent_time()
        return ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            start_date=project.start_date,
            github_url=project.github_url,
            color=project.color,
            status=project.status.value,
            created_at=project.created_at,
            updated_at=project.updated_at,
            elapsed_time=ElapsedTime(**elapsed),
            spent_time=ElapsedTime(**spent)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{project_id}/spent-time", response_model=ProjectResponse)
async def add_spent_time(
    project_id: int,
    request: SpentTimeAddRequest,
    service: ProjectService = Depends(get_project_service)
):
    """Add spent time to project"""
    try:
        project = await service.add_spent_time(project_id, request.seconds)
        elapsed = project.get_elapsed_time()
        spent = project.get_spent_time()
        return ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            start_date=project.start_date,
            github_url=project.github_url,
            color=project.color,
            status=project.status.value,
            created_at=project.created_at,
            updated_at=project.updated_at,
            elapsed_time=ElapsedTime(**elapsed),
            spent_time=ElapsedTime(**spent)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
