# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from datetime import datetime
from typing import Dict, List


class ProjectMarkdownService:

    PRIORITY_NAMES = {1: "High", 2: "Medium", 3: "Low"}

    @staticmethod
    def _format_date(date_str: str) -> str:
        if not date_str:
            return "--"
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%d %b %Y, %H:%M")
        except Exception:
            return date_str

    @staticmethod
    def _format_short_date(date_str: str) -> str:
        if not date_str:
            return ""
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%d %b %Y")
        except Exception:
            return date_str

    @staticmethod
    def _escape_md(text: str) -> str:
        if not text:
            return ""
        return text.replace("\r\n", "\n").strip()

    @staticmethod
    def _status_line(completed: bool) -> str:
        return "Completed" if completed else "Pending"

    @staticmethod
    def _task_progress_str(task, subtasks_map: Dict) -> str:
        subtask_ids = task.subtasks
        if not subtask_ids:
            return "100%" if task.completed else "0%"
        completed = 0
        for sid in subtask_ids:
            st = subtasks_map.get(sid)
            if st and st.completed:
                completed += 1
        pct = (completed / len(subtask_ids)) * 100
        return f"{pct:.0f}% ({completed}/{len(subtask_ids)} subtasks)"

    @staticmethod
    def build_markdown(project, tasks: List, subtasks_by_task: Dict, project_progress: float) -> str:
        subtasks_map = {}
        for subtask_list in subtasks_by_task.values():
            for st in subtask_list:
                subtasks_map[st.id] = st

        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.completed)

        total_subtasks = 0
        completed_subtasks = 0
        for task in tasks:
            subtask_list = subtasks_by_task.get(task.id, [])
            total_subtasks += len(subtask_list)
            completed_subtasks += sum(1 for st in subtask_list if st.completed)

        lines = []

        lines.append(f"# {ProjectMarkdownService._escape_md(project.name)}")
        lines.append("")

        lines.append(f"**Created:** {ProjectMarkdownService._format_date(project.created_at)}  ")
        lines.append(f"**Updated:** {ProjectMarkdownService._format_date(project.updated_at)}  ")

        if project.author:
            lines.append(f"**Author:** {ProjectMarkdownService._escape_md(project.author)}  ")
        else:
            lines.append(f"**Author:** Not specified  ")

        if project.link:
            lines.append(f"**Link:** [{project.link}]({project.link})  ")

        lines.append(f"**Progress:** {project_progress:.0f}% ({completed_tasks}/{total_tasks} tasks, "
                     f"{completed_subtasks}/{total_subtasks} subtasks)  ")

        if project_progress == 100:
            status = "Completed"
        elif project_progress > 70:
            status = "In Progress"
        elif project_progress > 30:
            status = "Active"
        elif project_progress > 0:
            status = "Started"
        else:
            status = "Not Started"
        lines.append(f"**Status:** {status}  ")

        lines.append("")
        lines.append("---")
        lines.append("")

        if project.description:
            lines.append("## Description")
            lines.append("")
            lines.append(ProjectMarkdownService._escape_md(project.description))
            lines.append("")
            lines.append("---")
            lines.append("")

        lines.append(f"## Tasks ({completed_tasks}/{total_tasks})")
        lines.append("")

        if not tasks:
            lines.append("_No tasks yet._")
            lines.append("")
        else:
            for idx, task in enumerate(tasks, start=1):
                lines.append(f"### {idx}. {ProjectMarkdownService._escape_md(task.title)}")
                lines.append("")

                lines.append(f"- **Priority:** {ProjectMarkdownService.PRIORITY_NAMES.get(task.priority, 'Unknown')}")
                lines.append(f"- **Status:** {ProjectMarkdownService._status_line(task.completed)}")

                if task.due_date:
                    lines.append(f"- **Due:** {ProjectMarkdownService._format_short_date(task.due_date)}")

                progress_str = ProjectMarkdownService._task_progress_str(task, subtasks_map)
                lines.append(f"- **Progress:** {progress_str}")

                created = ProjectMarkdownService._format_short_date(task.created_at)
                if created:
                    lines.append(f"- **Created:** {created}")

                lines.append("")

                if task.description:
                    lines.append(ProjectMarkdownService._escape_md(task.description))
                    lines.append("")

                subtask_list = subtasks_by_task.get(task.id, [])
                if subtask_list:
                    lines.append(f"**Subtasks ({len(subtask_list)}):**")
                    lines.append("")
                    for st in subtask_list:
                        checkbox = "[x]" if st.completed else "[ ]"
                        priority_name = ProjectMarkdownService.PRIORITY_NAMES.get(st.priority, "Unknown")
                        lines.append(f"- {checkbox} {ProjectMarkdownService._escape_md(st.title)} _({priority_name})_")
                    lines.append("")

                lines.append("---")
                lines.append("")

        lines.append("")
        lines.append(f"_Exported from Smart Project Manager on "
                     f"{datetime.now().strftime('%d %b %Y, %H:%M')}_")
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def write_to_file(project, tasks: List, subtasks_by_task: Dict,
                      project_progress: float, file_path: str) -> str:
        content = ProjectMarkdownService.build_markdown(
            project, tasks, subtasks_by_task, project_progress
        )
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
