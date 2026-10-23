from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox, QProgressBar, QSizePolicy
)
from datetime import datetime


class ProjectProgressWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setVisible(False)

    def setup_ui(self):
        self.setTitle("Project Progress")
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3a3d45;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #007acc;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(10, 12, 10, 10)

        top_line = QHBoxLayout()

        self.project_name_label = QLabel("--")
        self.project_name_label.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                        color: #007acc;
                    }
                """)
        self.project_name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.project_name_label.setMinimumWidth(200)
        self.project_name_label.setWordWrap(True)
        top_line.addWidget(self.project_name_label, 1)

        top_line.addStretch()

        self.project_status_badge = QLabel("--")
        self.project_status_badge.setStyleSheet("""
            QLabel {
                background-color: #95a5a6;
                color: white;
                padding: 3px 8px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 10px;
                min-width: 90px;
                text-align: center;
            }
        """)
        top_line.addWidget(self.project_status_badge)

        self.layout.addLayout(top_line)

        self.project_description_label = QLabel("--")
        self.project_description_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #aaa;
                font-style: italic;
                margin-bottom: 5px;
            }
        """)
        self.project_description_label.setWordWrap(True)
        self.layout.addWidget(self.project_description_label)

        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(3)

        progress_line = QHBoxLayout()

        progress_label = QLabel("Progress")
        progress_label.setStyleSheet("font-weight: bold; font-size: 11px;")
        progress_line.addWidget(progress_label)

        progress_line.addStretch()

        progress_layout.addLayout(progress_line)

        progress_bar_line = QHBoxLayout()

        self.project_progress_bar = QProgressBar()
        self.project_progress_bar.setTextVisible(False)
        self.project_progress_bar.setFixedHeight(16)
        self.project_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3a3d45;
                border-radius: 8px;
                background-color: #1e2026;
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
        self.project_progress_text.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #2ecc71;
                font-size: 12px;
                margin-left: 10px;
                min-width: 40px;
            }
        """)
        progress_bar_line.addWidget(self.project_progress_text)

        progress_layout.addLayout(progress_bar_line)
        self.layout.addLayout(progress_layout)

        stats_line = QHBoxLayout()
        stats_line.setSpacing(15)

        tasks_container = QWidget()
        tasks_layout = QHBoxLayout(tasks_container)
        tasks_layout.setContentsMargins(0, 0, 0, 0)
        tasks_layout.setSpacing(5)

        tasks_stats = QVBoxLayout()
        tasks_stats.setSpacing(1)

        self.project_tasks_total = QLabel("0")
        self.project_tasks_total.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
        """)
        tasks_stats.addWidget(self.project_tasks_total)

        tasks_label = QLabel("tasks")
        tasks_label.setStyleSheet("color: #2ecc71; font-size: 9px;")
        tasks_stats.addWidget(tasks_label)

        tasks_layout.addLayout(tasks_stats)
        stats_line.addWidget(tasks_container)

        subtasks_container = QWidget()
        subtasks_layout = QHBoxLayout(subtasks_container)
        subtasks_layout.setContentsMargins(0, 0, 0, 0)
        subtasks_layout.setSpacing(5)

        subtasks_stats = QVBoxLayout()
        subtasks_stats.setSpacing(1)

        self.project_subtasks_total = QLabel("0")
        self.project_subtasks_total.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: white;
            }
        """)
        subtasks_stats.addWidget(self.project_subtasks_total)

        subtasks_label = QLabel("subtasks")
        subtasks_label.setStyleSheet("color: #9b59b6; font-size: 9px;")
        subtasks_stats.addWidget(subtasks_label)

        subtasks_layout.addLayout(subtasks_stats)
        stats_line.addWidget(subtasks_container)

        timeline_container = QWidget()
        timeline_layout = QHBoxLayout(timeline_container)
        timeline_layout.setContentsMargins(0, 0, 0, 0)
        timeline_layout.setSpacing(5)

        timeline_stats = QVBoxLayout()
        timeline_stats.setSpacing(1)

        self.project_updated_label = QLabel("--")
        self.project_updated_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                font-weight: bold;
                color: white;
            }
        """)
        timeline_stats.addWidget(self.project_updated_label)

        timeline_label = QLabel("updated")
        timeline_label.setStyleSheet("color: #e74c3c; font-size: 9px;")
        timeline_stats.addWidget(timeline_label)

        timeline_layout.addLayout(timeline_stats)
        stats_line.addWidget(timeline_container)

        stats_line.addStretch()
        self.layout.addLayout(stats_line)

    def update_progress(self, project, manager):
        self.setVisible(True)
        self.setTitle("Project Progress")

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
                padding: 3px 8px;
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
                self.project_updated_label.setText(f"{updated_formatted}")
            except:
                self.project_updated_label.setText(f"{project.updated_at[:5]}")
        else:
            self.project_updated_label.setText("--")
