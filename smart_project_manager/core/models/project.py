# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
from typing import Dict, List, Optional
from dataclasses import dataclass, field

from smart_project_manager.core.models.task import Task
from smart_project_manager.core.utils import generate_id, format_datetime, calculate_progress


@dataclass
class Project:
    id: str
    name: str
    github_url: str
    version: str
    description: Optional[str] = None
    tasks: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __init__(
            self,
            name: str,
            github_url: str = "",
            version: str = "1.0.0",
            description: Optional[str] = None,
            id: Optional[str] = None
    ):
        self.id = id or generate_id()
        self.name = name
        self.github_url = github_url
        self.version = version
        self.description = description
        self.tasks = []
        self.created_at = format_datetime()
        self.updated_at = self.created_at

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = format_datetime()

    def add_task(self, task_id: str):
        if task_id not in self.tasks:
            self.tasks.append(task_id)
            self.updated_at = format_datetime()

    def remove_task(self, task_id: str):
        if task_id in self.tasks:
            self.tasks.remove(task_id)
            self.updated_at = format_datetime()

    def get_progress(self, all_tasks: Dict[str, Task]) -> float:
        if not self.tasks:
            return 0.0

        completed = 0
        for task_id in self.tasks:
            task = all_tasks.get(task_id)
            if task and task.completed:
                completed += 1

        return calculate_progress(len(self.tasks), completed)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "github_url": self.github_url,
            "version": self.version,
            "description": self.description,
            "tasks": self.tasks,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Project':
        github_url = data.get('github_url', '')

        project = cls(
            id=data['id'],
            name=data['name'],
            github_url=github_url,
            version=data['version'],
            description=data.get('description')
        )
        project.tasks = data.get('tasks', [])
        project.created_at = data.get('created_at')
        project.updated_at = data.get('updated_at')
        return project
