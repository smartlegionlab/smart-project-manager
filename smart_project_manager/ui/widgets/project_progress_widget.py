# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox, QProgressBar,
    QSizePolicy, QFrame, QPushButton
)
from datetime import datetime


class ProjectProgressWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setVisible(False)

    def setup_ui(self):
        self.setTitle("")
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #3a3d45;
                border-radius: 8px;
                background-color: #1e2026;
                margin-top: 0px;
                padding: 0px;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(14, 14, 14, 14)

        top_line = QHBoxLayout()
        top_line.setSpacing(10)

        title_column = QVBoxLayout()
        title_column.setSpacing(2)

        self.project_name_label = QLabel("--")
        self.project_name_label.setStyleSheet(
            "QLabel { font-size: 20px; font-weight: bold; color: #ffffff; }"
        )
        self.project_name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.project_name_label.setWordWrap(True)
        title_column.addWidget(self.project_name_label)

        self.project_description_label = QLabel("--")
        self.project_description_label.setStyleSheet(
            "QLabel { font-size: 12px; color: #aaa; font-style: italic; }"
        )
        self.project_description_label.setWordWrap(True)
        title_column.addWidget(self.project_description_label)

        top_line.addLayout(title_column, 1)

        right_column = QVBoxLayout()
        right_column.setSpacing(6)
        right_column.setAlignment(Qt.AlignRight | Qt.AlignTop)

        badge_line = QHBoxLayout()
        badge_line.setSpacing(6)
        badge_line.addStretch()

        self.project_status_badge = QLabel("--")
        self.project_status_badge.setStyleSheet("""
            QLabel {
                background-color: #95a5a6;
                color: white;
                padding: 3px 10px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 10px;
                min-width: 90px;
            }
        """)
        badge_line.addWidget(self.project_status_badge)

        right_column.addLayout(badge_line)

        buttons_line = QHBoxLayout()
        buttons_line.setSpacing(6)
        buttons_line.addStretch()

        self.btn_edit_project = QPushButton('Edit')
        self.btn_edit_project.setCursor(Qt.PointingHandCursor)
        self.btn_edit_project.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: black;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 5px;
                font-size: 11px;
            }
            QPushButton:hover:enabled { background-color: #FFA000; }
            QPushButton:disabled { background-color: #5a5d65; color: #999; }
        """)
        buttons_line.addWidget(self.btn_edit_project)

        self.btn_delete_project = QPushButton('Delete')
        self.btn_delete_project.setCursor(Qt.PointingHandCursor)
        self.btn_delete_project.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 5px;
                font-size: 11px;
            }
            QPushButton:hover:enabled { background-color: #c0392b; }
            QPushButton:disabled { background-color: #5a5d65; color: #999; }
        """)
        buttons_line.addWidget(self.btn_delete_project)

        right_column.addLayout(buttons_line)

        top_line.addLayout(right_column)
        self.layout.addLayout(top_line)

        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(3)

        progress_bar_line = QHBoxLayout()

        self.project_progress_bar = QProgressBar()
        self.project_progress_bar.setTextVisible(False)
        self.project_progress_bar.setFixedHeight(16)
        self.project_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3a3d45;
                border-radius: 8px;
                background-color: #181a1e;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #007acc,
                    stop:1 #2ecc71
                );
                border-radius: 7px;
            }
        """)
        progress_bar_line.addWidget(self.project_progress_bar, 3)

        self.project_progress_text = QLabel("0%")
        self.project_progress_text.setStyleSheet(
            "QLabel { font-weight: bold; color: #2ecc71; font-size: 13px; margin-left: 10px; min-width: 48px; }"
        )
        progress_bar_line.addWidget(self.project_progress_text)

        progress_layout.addLayout(progress_bar_line)
        self.layout.addLayout(progress_layout)

        stats_line = QHBoxLayout()
        stats_line.setSpacing(20)

        self.project_tasks_total = self._make_stat_block(stats_line, "tasks", "#2ecc71")
        self.project_subtasks_total = self._make_stat_block(stats_line, "subtasks", "#9b59b6")
        self.project_updated_label = self._make_stat_block(stats_line, "updated", "#e74c3c")

        stats_line.addStretch()
        self.layout.addLayout(stats_line)

    def _make_stat_block(self, parent_layout, caption, color):
        container = QWidget()
        box = QVBoxLayout(container)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(1)

        value = QLabel("0")
        value.setStyleSheet("QLabel { font-size: 14px; font-weight: bold; color: white; }")
        box.addWidget(value)

        caption_label = QLabel(caption)
        caption_label.setStyleSheet(f"QLabel {{ color: {color}; font-size: 9px; }}")
        box.addWidget(caption_label)

        parent_layout.addWidget(container)
        return value

    def update_progress(self, project, manager):
        self.setVisible(True)

        self.project_name_label.setText(project.name)

        if project.description:
            self.project_description_label.setText(project.description)
        else:
            self.project_description_label.setText("No description")

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
        self.project_progress_bar.setValue(int(progress))
        self.project_progress_text.setText(f"{progress:.1f}%")

        if progress == 100:
            status_text = "Completed"
            status_color = "#2e7d32"
        elif progress > 70:
            status_text = "In Progress"
            status_color = "#2ecc71"
        elif progress > 30:
            status_text = "Active"
            status_color = "#007acc"
        elif progress > 0:
            status_text = "Started"
            status_color = "#f39c12"
        else:
            status_text = "Not Started"
            status_color = "#95a5a6"

        self.project_status_badge.setText(status_text)
        self.project_status_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {status_color};
                color: white;
                padding: 3px 10px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 10px;
                min-width: 90px;
            }}
        """)

        self.project_tasks_total.setText(f"{completed_tasks}/{total_tasks}")
        self.project_subtasks_total.setText(f"{completed_subtasks}/{total_subtasks}")

        if project.updated_at:
            try:
                updated_date = datetime.fromisoformat(project.updated_at.replace('Z', '+00:00'))
                updated_formatted = updated_date.strftime("%d %b")
                self.project_updated_label.setText(updated_formatted)
            except Exception:
                self.project_updated_label.setText(project.updated_at[:5])
        else:
            self.project_updated_label.setText("--")
