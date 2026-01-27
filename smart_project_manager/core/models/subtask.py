# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from typing import Dict, List, Optional
from dataclasses import dataclass, field

from smart_project_manager.core.utils import generate_id, format_datetime


@dataclass
class SubTask:
    id: str
    title: str
    completed: bool
    task_id: str
    project_id: str
    priority: int = 3
    description: Optional[str] = None
    labels: List[str] = field(default_factory=list)
    due_date: Optional[str] = None
    completed_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __init__(
            self,
            title: str,
            task_id: str,
            project_id: str,
            priority: int = 3,
            description: Optional[str] = None,
            labels: Optional[List[str]] = None,
            due_date: Optional[str] = None,
            id: Optional[str] = None
    ):
        self.id = id or generate_id()
        self.title = title
        self.task_id = task_id
        self.project_id = project_id
        self.priority = priority
        self.description = description
        self.labels = labels or []
        self.due_date = due_date
        self.completed = False
        self.created_at = format_datetime()
        self.updated_at = self.created_at
        self.completed_at = None

    def toggle_complete(self):
        self.completed = not self.completed
        self.updated_at = format_datetime()
        if self.completed:
            self.completed_at = self.updated_at
        else:
            self.completed_at = None

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = format_datetime()

    def has_label(self, label_id: str) -> bool:
        return label_id in self.labels

    def add_label(self, label_id: str):
        if label_id not in self.labels:
            self.labels.append(label_id)
            self.updated_at = format_datetime()

    def remove_label(self, label_id: str):
        if label_id in self.labels:
            self.labels.remove(label_id)
            self.updated_at = format_datetime()

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "task_id": self.task_id,
            "project_id": self.project_id,
            "labels": self.labels,
            "due_date": self.due_date,
            "completed_at": self.completed_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'SubTask':
        subtask = cls(
            id=data['id'],
            title=data['title'],
            task_id=data['task_id'],
            project_id=data['project_id'],
            priority=data['priority'],
            description=data.get('description'),
            labels=data.get('labels', []),
            due_date=data.get('due_date')
        )
        subtask.completed = data['completed']
        subtask.created_at = data.get('created_at')
        subtask.updated_at = data.get('updated_at')
        subtask.completed_at = data.get('completed_at')
        return subtask
