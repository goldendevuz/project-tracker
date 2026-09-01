from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional


class ProjectCreateRequest(BaseModel):
    """DTO for creating new project"""
    name: str
    description: str
    github_url: str
    color: str = "#00d4aa"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "OpenDB",
                "description": "Open data API for Uzbekistan",
                "github_url": "https://github.com/goldendevuz/opendb",
                "color": "#00d4aa"
            }
        }


class ProjectUpdateRequest(BaseModel):
    """DTO for updating project"""
    name: Optional[str] = None
    description: Optional[str] = None
    github_url: Optional[str] = None
    color: Optional[str] = None
    status: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "OpenDB",
                "description": "Updated description",
                "color": "#4ecdc4"
            }
        }


class ElapsedTime(BaseModel):
    """DTO for elapsed time"""
    days: int
    hours: int
    minutes: int
    seconds: int


class ProjectResponse(BaseModel):
    """DTO for project response"""
    id: int
    name: str
    description: str
    start_date: datetime
    github_url: str
    color: str
    status: str
    created_at: datetime
    updated_at: datetime
    elapsed_time: Optional[ElapsedTime] = None
    spent_time: Optional[ElapsedTime] = None

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """DTO for project list response"""
    projects: list[ProjectResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "projects": [],
                "total": 0
            }
        }


class StatusChangeRequest(BaseModel):
    """DTO for status change"""
    status: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "completed"
            }
        }

class SpentTimeAddRequest(BaseModel):
    """DTO for adding spent time"""
    seconds: int

    class Config:
        json_schema_extra = {
            "example": {
                "seconds": 1500
            }
        }
