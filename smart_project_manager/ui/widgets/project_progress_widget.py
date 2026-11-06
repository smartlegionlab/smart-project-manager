# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
)


class ProjectProgressWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("projectCard")
        self.setStyleSheet("""
            QFrame#projectCard {
                background-color: #1c1f24;
                border: none;
                border-radius: 6px;
            }
        """)
        self.setup_ui()
        self.show_empty()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(18, 16, 18, 16)

        top_line = QHBoxLayout()
        top_line.setSpacing(16)

        title_column = QVBoxLayout()
        title_column.setSpacing(4)

        self.project_name_label = QLabel("--")
        self.project_name_label.setStyleSheet(
            "QLabel { font-size: 20px; font-weight: bold; color: #ffffff; background: transparent; }"
        )
        self.project_name_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.project_name_label.setMinimumWidth(0)
        self.project_name_label.setWordWrap(True)
        title_column.addWidget(self.project_name_label)

        self.project_description_label = QLabel("--")
        self.project_description_label.setStyleSheet(
            "QLabel { font-size: 12px; color: #8b94a3; background: transparent; }"
        )
        self.project_description_label.setWordWrap(True)
        self.project_description_label.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Preferred
        )
        self.project_description_label.setMinimumWidth(0)
        title_column.addWidget(self.project_description_label)

        self.project_link_label = QLabel("")
        self.project_link_label.setStyleSheet(
            "QLabel { font-size: 11px; background: transparent; }"
        )
        self.project_link_label.setOpenExternalLinks(True)
        self.project_link_label.setTextFormat(Qt.RichText)
        self.project_link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.project_link_label.setWordWrap(True)
        self.project_link_label.setSizePolicy(
            QSizePolicy.Ignored, QSizePolicy.Preferred
        )
        self.project_link_label.setMinimumWidth(0)
        self.project_link_label.setVisible(False)
        title_column.addWidget(self.project_link_label)

        top_line.addLayout(title_column, 1)

        right_column = QVBoxLayout()
        right_column.setSpacing(8)
        right_column.setAlignment(Qt.AlignRight | Qt.AlignTop)

        self.project_status_badge = QLabel("--")
        self.project_status_badge.setStyleSheet("""
            QLabel {
                background-color: #3a3f48;
                color: #ffffff;
                padding: 4px 12px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 10px;
                min-width: 90px;
                max-width: 90px;
            }
        """)
        self.project_status_badge.setAlignment(Qt.AlignCenter)
        right_column.addWidget(self.project_status_badge, 0, Qt.AlignRight)

        buttons_line = QHBoxLayout()
        buttons_line.setSpacing(6)
        buttons_line.setAlignment(Qt.AlignRight)

        self.btn_edit_project = self._make_button("Edit")
        buttons_line.addWidget(self.btn_edit_project)

        self.btn_delete_project = self._make_button("Delete")
        buttons_line.addWidget(self.btn_delete_project)

        right_column.addLayout(buttons_line)

        top_line.addLayout(right_column)
        layout.addLayout(top_line)

        tiles_line = QHBoxLayout()
        tiles_line.setSpacing(8)

        self.project_tasks_total = self._make_tile(
            tiles_line, "Tasks", "#4ea1ff", "0/0"
        )
        self.project_subtasks_total = self._make_tile(
            tiles_line, "Subtasks", "#b07ce8", "0/0"
        )
        self.project_updated_label = self._make_tile(
            tiles_line, "Updated", "#ff8a80", "--"
        )
        self.project_progress_text = self._make_tile(
            tiles_line, "Progress", "#4ee09c", "0%"
        )

        layout.addLayout(tiles_line)

    def _make_button(self, text):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFlat(True)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #3a3f48;
                color: #e6e9ee;
                font-weight: bold;
                font-size: 11px;
                padding: 5px 14px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4a505b;
            }
            QPushButton:pressed {
                background-color: #2f333a;
            }
            QPushButton:disabled {
                background-color: #2a2d33;
                color: #5a606b;
            }
        """)
        return btn

    def _make_tile(self, parent_layout, title, accent, initial_value):
        tile = QFrame()
        tile.setObjectName("statTile")
        tile.setStyleSheet("""
            QFrame#statTile {
                background-color: #23262c;
                border: none;
                border-radius: 6px;
            }
        """)
        tile.setMinimumHeight(70)
        tile.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        tile_layout = QVBoxLayout(tile)
        tile_layout.setContentsMargins(12, 10, 12, 10)
        tile_layout.setSpacing(2)

        title_label = QLabel(title.upper())
        title_label.setStyleSheet(
            f"QLabel {{ color: {accent}; font-size: 9px; font-weight: bold; "
            f"letter-spacing: 1px; background: transparent; }}"
        )
        tile_layout.addWidget(title_label)

        value_label = QLabel(initial_value)
        value_label.setStyleSheet(
            "QLabel { color: #ffffff; font-size: 20px; font-weight: bold; background: transparent; }"
        )
        value_label.setWordWrap(False)
        tile_layout.addWidget(value_label)

        parent_layout.addWidget(tile, 1)
        return value_label

    def _format_link_html(self, link: str) -> str:
        display = link
        if len(display) > 60:
            display = display[:57] + "..."
        return (
            f"<a href='{link}' style='color: #4ea1ff; text-decoration: none;'>"
            f"{display}</a>"
        )

    def show_empty(self):
        self.project_name_label.setText("No project selected")
        self.project_name_label.setStyleSheet(
            "QLabel { font-size: 20px; font-weight: bold; color: #6a7280; "
            "background: transparent; }"
        )
        self.project_description_label.setText(
            "Pick a project from the list on the left, or create a new one."
        )
        self.project_description_label.setStyleSheet(
            "QLabel { font-size: 12px; color: #5a606b; background: transparent; }"
        )
        self.project_link_label.setText("")
        self.project_link_label.setVisible(False)
        self.project_status_badge.setText("")
        self.project_status_badge.setStyleSheet("""
            QLabel {
                background-color: transparent;
                color: transparent;
                padding: 0px;
                min-width: 90px;
                max-width: 90px;
            }
        """)
        self.project_tasks_total.setText("0/0")
        self.project_subtasks_total.setText("0/0")
        self.project_updated_label.setText("--")
        self.project_progress_text.setText("0%")
        self.btn_edit_project.setEnabled(False)
        self.btn_delete_project.setEnabled(False)

    def update_progress(self, project, manager):
        if not project:
            self.show_empty()
            return

        self.btn_edit_project.setEnabled(True)
        self.btn_delete_project.setEnabled(True)

        self.project_name_label.setText(project.name)
        self.project_name_label.setStyleSheet(
            "QLabel { font-size: 20px; font-weight: bold; color: #ffffff; "
            "background: transparent; }"
        )

        if project.description:
            self.project_description_label.setText(project.description)
            self.project_description_label.setStyleSheet(
                "QLabel { font-size: 12px; color: #8b94a3; background: transparent; }"
            )
        else:
            self.project_description_label.setText("No description")
            self.project_description_label.setStyleSheet(
                "QLabel { font-size: 12px; color: #5a606b; font-style: italic; "
                "background: transparent; }"
            )

        if project.link:
            self.project_link_label.setText(
                f"Link: {self._format_link_html(project.link)}"
            )
            self.project_link_label.setVisible(True)
            self.project_link_label.setToolTip(project.link)
        else:
            self.project_link_label.setText("")
            self.project_link_label.setVisible(False)

        tasks = manager.get_tasks_by_project(project.id)
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.completed)

        total_subtasks = 0
        completed_subtasks = 0

        for task in tasks:
            subtasks = manager.get_subtasks_by_task(task.id)
            total_subtasks += len(subtasks)
            completed_subtasks += sum(1 for subtask in subtasks if subtask.completed)

        progress = manager.get_project_progress(project.id)
        self.project_progress_text.setText(f"{progress:.0f}%")

        if progress == 100:
            status_text = "Completed"
            status_color = "#2e7d32"
        elif progress > 70:
            status_text = "In Progress"
            status_color = "#2a8f5e"
        elif progress > 30:
            status_text = "Active"
            status_color = "#2a6fb0"
        elif progress > 0:
            status_text = "Started"
            status_color = "#b07a1e"
        else:
            status_text = "Not Started"
            status_color = "#3a3f48"

        self.project_status_badge.setText(status_text)
        self.project_status_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {status_color};
                color: #ffffff;
                padding: 4px 12px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 10px;
                min-width: 90px;
                max-width: 90px;
            }}
        """)

        self.project_tasks_total.setText(f"{completed_tasks}/{total_tasks}")
        self.project_subtasks_total.setText(f"{completed_subtasks}/{total_subtasks}")

        if project.updated_at:
            try:
                updated_date = datetime.fromisoformat(project.updated_at.replace('Z', '+00:00'))
                self.project_updated_label.setText(updated_date.strftime("%d %b"))
            except Exception:
                self.project_updated_label.setText(project.updated_at[:5])
        else:
            self.project_updated_label.setText("--")
