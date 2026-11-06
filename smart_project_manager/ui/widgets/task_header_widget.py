# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
)


class TaskHeaderWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.task_id = None
        self.manager = None

        self.setObjectName("taskHeader")
        self.setStyleSheet("""
            QFrame#taskHeader {
                background-color: #1c1f24;
                border: none;
                border-radius: 6px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        top_line = QHBoxLayout()
        top_line.setSpacing(10)

        title_column = QVBoxLayout()
        title_column.setSpacing(2)

        self.title_label = QLabel("No task selected")
        self.title_label.setStyleSheet(
            "QLabel { font-size: 16px; font-weight: bold; color: #ffffff; background: transparent; }"
        )
        self.title_label.setWordWrap(True)
        self.title_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.title_label.setMinimumWidth(0)
        title_column.addWidget(self.title_label)

        self.description_label = QLabel("")
        self.description_label.setStyleSheet(
            "QLabel { font-size: 11px; color: #8b94a3; background: transparent; }"
        )
        self.description_label.setWordWrap(True)
        self.description_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        self.description_label.setMinimumWidth(0)
        title_column.addWidget(self.description_label)

        top_line.addLayout(title_column, 1)

        right_column = QVBoxLayout()
        right_column.setSpacing(8)
        right_column.setAlignment(Qt.AlignRight | Qt.AlignTop)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #3a3f48;
                color: #ffffff;
                padding: 4px 12px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 10px;
                min-width: 80px;
                max-width: 80px;
            }
        """)
        right_column.addWidget(self.status_label, 0, Qt.AlignRight)

        buttons_line = QHBoxLayout()
        buttons_line.setSpacing(6)
        buttons_line.setAlignment(Qt.AlignRight)

        self.btn_toggle = self._make_button(
            "Toggle", "#2a8f5e", "#34a56e", "#ffffff"
        )
        self.btn_toggle.clicked.connect(self.on_toggle_clicked)
        buttons_line.addWidget(self.btn_toggle)

        self.btn_edit = self._make_button(
            "Edit", "#FFC107", "#FFA000", "#000000"
        )
        self.btn_edit.clicked.connect(self.on_edit_clicked)
        buttons_line.addWidget(self.btn_edit)

        self.btn_delete = self._make_button(
            "Delete", "#e74c3c", "#c0392b", "#ffffff"
        )
        self.btn_delete.clicked.connect(self.on_delete_clicked)
        buttons_line.addWidget(self.btn_delete)

        right_column.addLayout(buttons_line)

        top_line.addLayout(right_column)
        layout.addLayout(top_line)

        meta_line = QHBoxLayout()
        meta_line.setSpacing(16)

        self.priority_label = QLabel("")
        self.priority_label.setStyleSheet(
            "QLabel { font-size: 11px; color: #ffffff; font-weight: bold; background: transparent; }"
        )
        meta_line.addWidget(self.priority_label)

        self.due_label = QLabel("")
        self.due_label.setStyleSheet(
            "QLabel { font-size: 11px; color: #8b94a3; background: transparent; }"
        )
        meta_line.addWidget(self.due_label)

        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(
            "QLabel { font-size: 11px; color: #4ea1ff; font-weight: bold; background: transparent; }"
        )
        meta_line.addWidget(self.progress_label)

        meta_line.addStretch()
        layout.addLayout(meta_line)

        self.callbacks = {'toggle': None, 'edit': None, 'delete': None}

        self.update_task(None, None)

    def _make_button(self, text, bg, bg_hover, fg):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFlat(True)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {fg};
                font-weight: bold;
                font-size: 11px;
                padding: 5px 14px;
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {bg_hover};
            }}
            QPushButton:pressed {{
                background-color: #23262c;
            }}
            QPushButton:disabled {{
                background-color: #2a2d33;
                color: #5a606b;
            }}
        """)
        return btn

    def set_callbacks(self, toggle_cb, edit_cb, delete_cb):
        self.callbacks['toggle'] = toggle_cb
        self.callbacks['edit'] = edit_cb
        self.callbacks['delete'] = delete_cb

    def update_task(self, task, manager):
        self.task_id = task.id if task else None
        self.manager = manager

        if not task:
            self.title_label.setText("No task selected")
            self.description_label.setText("Pick a task from the list on the left.")
            self.priority_label.setText("")
            self.due_label.setText("")
            self.progress_label.setText("")
            self.status_label.setText("")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                    color: transparent;
                    padding: 0px;
                    min-width: 80px;
                    max-width: 80px;
                }
            """)
            self.btn_toggle.setEnabled(False)
            self.btn_edit.setEnabled(False)
            self.btn_delete.setEnabled(False)
            return

        self.btn_toggle.setEnabled(True)
        self.btn_edit.setEnabled(True)
        self.btn_delete.setEnabled(True)

        self.title_label.setText(task.title)

        if task.description:
            self.description_label.setText(task.description)
        else:
            self.description_label.setText("")

        priority_text = ["High", "Medium", "Low"][task.priority - 1]
        priority_color = ["#ff6b6b", "#ffb454", "#4ee09c"][task.priority - 1]
        self.priority_label.setText(f"Priority: {priority_text}")
        self.priority_label.setStyleSheet(
            f"QLabel {{ font-size: 11px; color: {priority_color}; font-weight: bold; "
            f"background: transparent; }}"
        )

        if task.due_date:
            try:
                due_date = datetime.fromisoformat(task.due_date).date()
                if not task.completed and due_date < datetime.now().date():
                    self.due_label.setText(f"Due: {task.due_date} (overdue)")
                    self.due_label.setStyleSheet(
                        "QLabel { font-size: 11px; color: #ff6b6b; font-weight: bold; "
                        "background: transparent; }"
                    )
                else:
                    self.due_label.setText(f"Due: {task.due_date}")
                    self.due_label.setStyleSheet(
                        "QLabel { font-size: 11px; color: #8b94a3; background: transparent; }"
                    )
            except Exception:
                self.due_label.setText(f"Due: {task.due_date}")
                self.due_label.setStyleSheet(
                    "QLabel { font-size: 11px; color: #8b94a3; background: transparent; }"
                )
        else:
            self.due_label.setText("No due date")
            self.due_label.setStyleSheet(
                "QLabel { font-size: 11px; color: #5a606b; background: transparent; }"
            )

        progress = manager.get_task_progress(task.id)
        self.progress_label.setText(f"Progress: {progress:.0f}%")

        if task.completed:
            self.status_label.setText("Completed")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #2e7d32;
                    color: #ffffff;
                    padding: 4px 12px;
                    border-radius: 10px;
                    font-weight: bold;
                    font-size: 10px;
                    min-width: 80px;
                    max-width: 80px;
                }
            """)
        else:
            self.status_label.setText("Pending")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #b07a1e;
                    color: #ffffff;
                    padding: 4px 12px;
                    border-radius: 10px;
                    font-weight: bold;
                    font-size: 10px;
                    min-width: 80px;
                    max-width: 80px;
                }
            """)

    def on_toggle_clicked(self):
        if self.callbacks['toggle'] and self.task_id:
            self.callbacks['toggle'](self.task_id)

    def on_edit_clicked(self):
        if self.callbacks['edit'] and self.task_id:
            self.callbacks['edit'](self.task_id)

    def on_delete_clicked(self):
        if self.callbacks['delete'] and self.task_id:
            self.callbacks['delete'](self.task_id)
