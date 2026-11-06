# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import os
from typing import Dict, List, Optional

from smart_project_manager.core.models.project import Project
from smart_project_manager.core.models.subtask import SubTask
from smart_project_manager.core.models.task import Task
from smart_project_manager.core.services.import_export_service import ImportExportService
from smart_project_manager.core.services.project_markdown_service import ProjectMarkdownService
from smart_project_manager.core.utils import load_json, save_json, format_datetime


class ProjectManager:

    def __init__(self, data_dir: str = "~/.smart_project_manager"):
        self.data_dir = os.path.expanduser(data_dir)
        self.data_file = os.path.join(self.data_dir, "projects.json")

        self._ensure_data_file_exists()

        self.projects: Dict[str, Project] = {}
        self.tasks: Dict[str, Task] = {}
        self.subtasks: Dict[str, SubTask] = {}

        self.load_data()

    def _ensure_data_file_exists(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

        if not os.path.exists(self.data_file):
            empty_data = {
                'projects': {},
                'tasks': {},
                'subtasks': {}
            }
            save_json(self.data_file, empty_data)
            print(f"Created new data file: {self.data_file}")

    def load_data(self):
        data = load_json(self.data_file)

        self.projects = {}
        for project_data in data.get('projects', {}).values():
            project = Project.from_dict(project_data)
            self.projects[project.id] = project

        self.tasks = {}
        for task_data in data.get('tasks', {}).values():
            task = Task.from_dict(task_data)
            self.tasks[task.id] = task

        self.subtasks = {}
        for subtask_data in data.get('subtasks', {}).values():
            subtask = SubTask.from_dict(subtask_data)
            self.subtasks[subtask.id] = subtask

    def save_data(self):
        data = {
            'projects': {project_id: project.to_dict() for project_id, project in self.projects.items()},
            'tasks': {task_id: task.to_dict() for task_id, task in self.tasks.items()},
            'subtasks': {subtask_id: subtask.to_dict() for subtask_id, subtask in self.subtasks.items()}
        }
        save_json(self.data_file, data)

    def create_project(self, name: str,
                      description: Optional[str] = None,
                      link: Optional[str] = None) -> Project:
        project = Project(name=name, description=description, link=link)
        self.projects[project.id] = project
        self.save_data()
        return project

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.projects.get(project_id)

    def update_project(self, project_id: str, **kwargs):
        project = self.get_project(project_id)
        if project:
            for key, value in kwargs.items():
                if hasattr(project, key):
                    setattr(project, key, value)
            project.updated_at = format_datetime()
            self.save_data()

    def delete_project(self, project_id: str):
        project = self.get_project(project_id)
        if project:
            for task_id in list(project.tasks):
                self.delete_task(task_id)

            del self.projects[project_id]
            self.save_data()

    def get_all_projects(self) -> List[Project]:
        return list(self.projects.values())

    def create_task(self, title: str, project_id: str, priority: int = 3,
                    description: Optional[str] = None,
                    due_date: Optional[str] = None) -> Task:
        task = Task(title=title, project_id=project_id, priority=priority,
                    description=description, due_date=due_date)

        self.tasks[task.id] = task

        project = self.get_project(project_id)
        if project:
            project.add_task(task.id)

        self.save_data()
        return task

    def create_subtask(
            self, title: str,
            task_id: str,
            project_id: str,
            priority: int = 3
    ) -> SubTask:
        subtask = SubTask(
            title=title,
            task_id=task_id,
            project_id=project_id,
            priority=priority
        )

        self.subtasks[subtask.id] = subtask

        task = self.get_task(task_id)
        if task:
            task.add_subtask(subtask.id)

        self.save_data()
        return subtask

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def update_task(self, task_id: str, **kwargs):
        task = self.get_task(task_id)
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            task.updated_at = format_datetime()
            self.save_data()

    def delete_task(self, task_id: str):
        task = self.get_task(task_id)
        if task:
            for subtask_id in list(task.subtasks):
                self.delete_subtask(subtask_id)

            project = self.get_project(task.project_id)
            if project:
                project.remove_task(task_id)

            del self.tasks[task_id]
            self.save_data()

    def get_tasks_by_project(self, project_id: str) -> List[Task]:
        return [task for task in self.tasks.values() if task.project_id == project_id]

    def get_subtask(self, subtask_id: str) -> Optional[SubTask]:
        return self.subtasks.get(subtask_id)

    def update_subtask(self, subtask_id: str, **kwargs):
        subtask = self.get_subtask(subtask_id)
        if subtask:
            for key, value in kwargs.items():
                if hasattr(subtask, key):
                    setattr(subtask, key, value)
            subtask.updated_at = format_datetime()

            self.save_data()

    def delete_subtask(self, subtask_id: str):
        subtask = self.get_subtask(subtask_id)
        if subtask:
            task = self.get_task(subtask.task_id)
            if task:
                task.remove_subtask(subtask_id)

            del self.subtasks[subtask_id]
            self.save_data()

    def get_subtasks_by_task(self, task_id: str) -> List[SubTask]:
        return [subtask for subtask in self.subtasks.values() if subtask.task_id == task_id]

    def get_project_progress(self, project_id: str) -> float:
        project = self.get_project(project_id)
        if project:
            return project.get_progress(self.tasks)
        return 0.0

    def get_task_progress(self, task_id: str) -> float:
        task = self.get_task(task_id)
        if task:
            return task.get_progress(self.subtasks)
        return 0.0

    def get_statistics(self) -> Dict:
        total_projects = len(self.projects)
        total_tasks = len(self.tasks)
        total_subtasks = len(self.subtasks)

        completed_tasks = sum(1 for task in self.tasks.values() if task.completed)
        completed_subtasks = sum(1 for subtask in self.subtasks.values() if subtask.completed)

        return {
            'projects': total_projects,
            'tasks': total_tasks,
            'subtasks': total_subtasks,
            'completed_tasks': completed_tasks,
            'completed_subtasks': completed_subtasks,
            'task_completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            'subtask_completion_rate': (completed_subtasks / total_subtasks * 100) if total_subtasks > 0 else 0
        }

    def import_data(self, import_path: str) -> Dict:
        return ImportExportService.import_data(self.data_file, import_path)

    def export_data(self, export_path: str) -> Dict:
        return ImportExportService.export_data(self.data_file, export_path)

    def export_project_to_markdown(self, project_id: str, file_path: str) -> Dict:
        project = self.get_project(project_id)
        if not project:
            return {
                'success': False,
                'error': f'Project {project_id} not found'
            }

        try:
            tasks = self.get_tasks_by_project(project_id)
            if project.task_order:
                tasks_dict = {task.id: task for task in tasks}
                sorted_tasks = []
                for tid in project.task_order:
                    if tid in tasks_dict:
                        sorted_tasks.append(tasks_dict.pop(tid))
                sorted_tasks.extend(tasks_dict.values())
                tasks = sorted_tasks

            subtasks_by_task = {}
            for task in tasks:
                subtasks_by_task[task.id] = self.get_subtasks_by_task(task.id)

            progress = self.get_project_progress(project_id)

            ProjectMarkdownService.write_to_file(
                project, tasks, subtasks_by_task, progress, file_path
            )

            return {
                'success': True,
                'export_path': file_path,
                'export_size': os.path.getsize(file_path)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
