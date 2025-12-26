# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
from typing import Dict, List, Optional
from dataclasses import dataclass, field

from smart_project_manager.core.models.subtask import SubTask
from smart_project_manager.core.utils import generate_id, format_datetime, calculate_progress


@dataclass
class Task:
    id: str
    title: str
    project_id: str
    priority: int = 3
    description: Optional[str] = None
    completed: bool = False
    labels: List[str] = field(default_factory=list)
    subtasks: List[str] = field(default_factory=list)
    due_date: Optional[str] = None
    completed_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __init__(
            self, title: str,
            project_id: str,
            priority: int = 3,
            description: Optional[str] = None,
            labels: Optional[List[str]] = None,
            due_date: Optional[str] = None,
            id: Optional[str] = None
    ):
        self.id = id or generate_id()
        self.title = title
        self.project_id = project_id
        self.priority = priority
        self.description = description
        self.labels = labels or []
        self.subtasks = []
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

    def add_subtask(self, subtask_id: str):
        if subtask_id not in self.subtasks:
            self.subtasks.append(subtask_id)
            self.updated_at = format_datetime()

    def remove_subtask(self, subtask_id: str):
        if subtask_id in self.subtasks:
            self.subtasks.remove(subtask_id)
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

    def check_completion(self, all_subtasks: Dict[str, SubTask]) -> bool:
        if not self.subtasks:
            return self.completed

        for subtask_id in self.subtasks:
            subtask = all_subtasks.get(subtask_id)
            if subtask and not subtask.completed:
                return False
        return True

    def update_completion(self, all_subtasks: Dict[str, SubTask]):
        if self.subtasks:
            all_completed = True
            for subtask_id in self.subtasks:
                subtask = all_subtasks.get(subtask_id)
                if subtask and not subtask.completed:
                    all_completed = False
                    break

            if all_completed != self.completed:
                self.completed = all_completed
                self.updated_at = format_datetime()
                if self.completed:
                    self.completed_at = self.updated_at
                else:
                    self.completed_at = None

    def get_progress(self, all_subtasks: Dict[str, SubTask]) -> float:
        if not self.subtasks:
            return 100.0 if self.completed else 0.0

        completed = 0
        for subtask_id in self.subtasks:
            subtask = all_subtasks.get(subtask_id)
            if subtask and subtask.completed:
                completed += 1

        return calculate_progress(len(self.subtasks), completed)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "project_id": self.project_id,
            "labels": self.labels,
            "subtasks": self.subtasks,
            "due_date": self.due_date,
            "completed_at": self.completed_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        task = cls(
            id=data['id'],
            title=data['title'],
            project_id=data['project_id'],
            priority=data['priority'],
            description=data.get('description'),
            labels=data.get('labels', []),
            due_date=data.get('due_date')
        )
        task.completed = data['completed']
        task.subtasks = data.get('subtasks', [])
        task.created_at = data.get('created_at')
        task.updated_at = data.get('updated_at')
        task.completed_at = data.get('completed_at')
        return task
