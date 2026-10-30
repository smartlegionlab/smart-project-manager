# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QGroupBox, QProgressBar,
    QSizePolicy, QPushButton, QGridLayout
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
        self.layout.setSpacing(12)
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
        right_column.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

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
                text-align: center;
            }
        """)
        badge_line.addWidget(self.project_status_badge)

        right_column.addLayout(badge_line)

        buttons_line = QHBoxLayout()
        buttons_line.setSpacing(6)
        buttons_line.addStretch()

        self.btn_edit_project = QPushButton('Edit')
        self.btn_edit_project.setCursor(Qt.CursorShape.PointingHandCursor)
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
        self.btn_delete_project.setCursor(Qt.CursorShape.PointingHandCursor)
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

        tiles_grid = QGridLayout()
        tiles_grid.setHorizontalSpacing(8)
        tiles_grid.setVerticalSpacing(8)

        self.tasks_box, self.project_tasks_total = self._create_stat_box(
            "Tasks", "#2ecc71", "0"
        )
        tiles_grid.addWidget(self.tasks_box, 0, 0)

        self.subtasks_box, self.project_subtasks_total = self._create_stat_box(
            "Subtasks", "#9b59b6", "0"
        )
        tiles_grid.addWidget(self.subtasks_box, 0, 1)

        self.updated_box, self.project_updated_label = self._create_stat_box(
            "Updated", "#e74c3c", "--"
        )
        tiles_grid.addWidget(self.updated_box, 0, 2)

        tiles_grid.setColumnStretch(0, 1)
        tiles_grid.setColumnStretch(1, 1)
        tiles_grid.setColumnStretch(2, 1)
        self.layout.addLayout(tiles_grid)

        progress_group = QGroupBox()
        progress_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #3a3d45;
                border-radius: 6px;
                background-color: #1e2026;
                margin-top: 0px;
                padding: 8px;
                min-height: 60px;
            }
        """)
        progress_layout = QVBoxLayout(progress_group)
        progress_layout.setSpacing(6)
        progress_layout.setContentsMargins(10, 8, 10, 8)

        progress_header = QHBoxLayout()
        progress_title = QLabel("Progress")
        progress_title.setStyleSheet(
            "QLabel { font-weight: bold; color: #007acc; font-size: 11px; }"
        )
        progress_header.addWidget(progress_title)

        progress_header.addStretch()

        self.project_progress_text = QLabel("0%")
        self.project_progress_text.setStyleSheet(
            "QLabel { font-weight: bold; color: #2ecc71; font-size: 12px; }"
        )
        progress_header.addWidget(self.project_progress_text)

        progress_layout.addLayout(progress_header)

        self.project_progress_bar = QProgressBar()
        self.project_progress_bar.setTextVisible(False)
        self.project_progress_bar.setFixedHeight(14)
        self.project_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3a3d45;
                border-radius: 7px;
                background-color: #181a1e;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #007acc,
                    stop:1 #2ecc71
                );
                border-radius: 6px;
            }
        """)
        progress_layout.addWidget(self.project_progress_bar)

        self.layout.addWidget(progress_group)

    def _create_stat_box(self, title: str, color: str, initial_value: str):
        box = QGroupBox()
        box.setStyleSheet(f"""
            QGroupBox {{
                border: 1px solid #3a3d45;
                border-radius: 6px;
                background-color: #1e2026;
                min-height: 76px;
            }}
        """)

        layout = QVBoxLayout(box)
        layout.setSpacing(3)
        layout.setContentsMargins(6, 8, 6, 8)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            f"font-weight: bold; color: {color}; font-size: 11px; qproperty-alignment: 'AlignCenter';"
        )
        layout.addWidget(title_label)

        value_label = QLabel(initial_value)
        value_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: white;
                qproperty-alignment: 'AlignCenter';
            }
        """)
        layout.addWidget(value_label)

        layout.addStretch()

        subtitle = QLabel("Total")
        subtitle.setStyleSheet(
            "color: #aaa; font-size: 9px; qproperty-alignment: 'AlignCenter';"
        )
        layout.addWidget(subtitle)

        return box, value_label

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
                text-align: center;
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
