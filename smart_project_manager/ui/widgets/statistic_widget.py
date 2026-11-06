# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QProgressBar
)
from PyQt5.QtCore import Qt


class StatisticsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 2, 8, 2)
        layout.setSpacing(18)

        self.projects_label = self._make_stat(layout, "Projects", "#4ea1ff", "0")
        self.tasks_label = self._make_stat(layout, "Tasks", "#4ee09c", "0/0")
        self.subtasks_label = self._make_stat(layout, "Subtasks", "#b07ce8", "0/0")
        self.labels_label = self._make_stat(layout, "Labels", "#ff8a80", "0")

        layout.addStretch()

        self.tasks_progress_text, self.tasks_progress_bar = self._make_progress(
            layout, "#4ee09c"
        )
        self.subtasks_progress_text, self.subtasks_progress_bar = self._make_progress(
            layout, "#b07ce8"
        )

    def _make_stat(self, parent_layout, title, color, initial_value):
        container = QWidget()
        box = QHBoxLayout(container)
        box.setContentsMargins(0, 0, 0, 0)
        box.setSpacing(5)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            f"QLabel {{ color: {color}; font-size: 10px; font-weight: bold; background: transparent; }}"
        )
        box.addWidget(title_label)

        value_label = QLabel(initial_value)
        value_label.setStyleSheet(
            "QLabel { color: #ffffff; font-size: 11px; font-weight: bold; background: transparent; }"
        )
        box.addWidget(value_label)

        parent_layout.addWidget(container)
        return value_label

    def _make_progress(self, parent_layout, color):
        text_label = QLabel("0%")
        text_label.setStyleSheet(
            f"QLabel {{ color: {color}; font-size: 10px; font-weight: bold; background: transparent; }}"
        )
        parent_layout.addWidget(text_label)

        bar = QProgressBar()
        bar.setTextVisible(False)
        bar.setFixedSize(90, 8)
        bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 4px;
                background-color: #2a2d33;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 4px;
            }}
        """)
        bar.setValue(0)
        parent_layout.addWidget(bar)
        return text_label, bar

    def update_stats(self, stats):
        self.projects_label.setText(str(stats['projects']))
        self.tasks_label.setText(f"{stats['completed_tasks']}/{stats['tasks']}")
        self.subtasks_label.setText(f"{stats['completed_subtasks']}/{stats['subtasks']}")
        self.labels_label.setText(str(stats['labels']))

        tasks_pct = stats['task_completion_rate']
        self.tasks_progress_bar.setValue(int(tasks_pct))
        self.tasks_progress_text.setText(f"{tasks_pct:.0f}%")

        subtasks_pct = stats['subtask_completion_rate']
        self.subtasks_progress_bar.setValue(int(subtasks_pct))
        self.subtasks_progress_text.setText(f"{subtasks_pct:.0f}%")