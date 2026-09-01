from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class ProjectStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


@dataclass
class Project:
    """Project entity - core business logic"""
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    start_date: Optional[datetime] = None
    github_url: str = ""
    color: str = "#00d4aa"
    status: ProjectStatus = ProjectStatus.ACTIVE
    spent_seconds: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.start_date is None:
            self.start_date = datetime.utcnow()
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    def update_description(self, description: str):
        """Domain logic: update description"""
        self.description = description
        self.updated_at = datetime.utcnow()

    def update_github_url(self, github_url: str):
        """Domain logic: validate and update GitHub URL"""
        if not github_url.startswith("https://github.com/"):
            raise ValueError("Invalid GitHub URL")
        self.github_url = github_url
        self.updated_at = datetime.utcnow()

    def update_color(self, color: str):
        """Domain logic: validate and update color"""
        if not color.startswith("#") or len(color) != 7:
            raise ValueError("Invalid color format")
        self.color = color
        self.updated_at = datetime.utcnow()

    def change_status(self, new_status: ProjectStatus):
        """Domain logic: change project status"""
        self.status = new_status
        self.updated_at = datetime.utcnow()

    def get_elapsed_time(self) -> dict:
        """Calculate elapsed time since project start"""
        if not self.start_date:
            return {"days": 0, "hours": 0, "minutes": 0, "seconds": 0}
        
        diff = datetime.utcnow() - self.start_date
        days = diff.days
        seconds = diff.seconds
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": secs
        }

    def add_spent_time(self, seconds: int):
        """Domain logic: add spent time"""
        if seconds < 0:
            raise ValueError("Seconds cannot be negative")
        self.spent_seconds += seconds
        self.updated_at = datetime.utcnow()

    def get_spent_time(self) -> dict:
        """Calculate formatted spent time"""
        seconds = self.spent_seconds
        days = seconds // 86400
        seconds %= 86400
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": secs
        }
