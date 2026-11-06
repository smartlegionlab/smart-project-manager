# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from datetime import datetime

from PyQt5.QtWidgets import (
    QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QLabel, QVBoxLayout
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSignal

from smart_project_manager.ui.widgets.label_widget import LabelWidget


class TaskListWidget(QListWidget):
    task_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = None
        self.setup_list()
        self.currentItemChanged.connect(self.on_current_changed)

    def setup_list(self):
        self.setStyleSheet("""
            QListWidget {
                background-color: #1c1f24;
                border: none;
                border-radius: 6px;
                padding: 4px;
                outline: 0;
            }
            QListWidget::item {
                background-color: transparent;
                border: none;
                padding: 0px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: transparent;
                border: none;
            }
            QListWidget::item:hover:!selected {
                background-color: transparent;
            }
        """)
        self.setUniformItemSizes(False)
        self.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        self.setSpacing(2)

    def load_tasks(self, tasks):
        current_id = self.get_current_task_id()

        self.blockSignals(True)
        self.clear()

        if not tasks:
            empty = QListWidgetItem()
            empty.setFlags(Qt.NoItemFlags)
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(16, 20, 16, 20)
            empty_label = QLabel("No tasks yet.\nClick + Add to create one.")
            empty_label.setStyleSheet("color: #5a606b; font-size: 12px;")
            empty_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(empty_label)
            empty.setSizeHint(widget.sizeHint())
            self.addItem(empty)
            self.setItemWidget(empty, widget)
        else:
            for task in tasks:
                self._add_task_row(task)

        self.blockSignals(False)

        if current_id:
            self.select_task(current_id)

    def _add_task_row(self, task):
        widget = QWidget()
        widget.setObjectName("taskRow")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)

        top_line = QHBoxLayout()
        top_line.setSpacing(8)

        dot = QLabel()
        dot.setFixedSize(8, 8)
        if task.completed:
            dot.setStyleSheet("QLabel { background-color: #4ee09c; border-radius: 4px; }")
        else:
            dot.setStyleSheet("QLabel { background-color: #ffb454; border-radius: 4px; }")
        top_line.addWidget(dot, 0, Qt.AlignTop)

        title_label = QLabel(task.title)
        if task.completed:
            title_label.setStyleSheet(
                "QLabel { color: #6a7280; font-size: 12px; font-weight: bold; "
                "text-decoration: line-through; background: transparent; }"
            )
        else:
            title_label.setStyleSheet(
                "QLabel { color: #ffffff; font-size: 12px; font-weight: bold; "
                "background: transparent; }"
            )
        title_label.setWordWrap(True)
        top_line.addWidget(title_label, 1)

        priority_text = ["High", "Medium", "Low"][task.priority - 1]
        priority_color = ["#ff6b6b", "#ffb454", "#4ee09c"][task.priority - 1]
        priority_label = QLabel(priority_text)
        priority_label.setStyleSheet(
            f"QLabel {{ color: {priority_color}; font-size: 9px; font-weight: bold; "
            f"background: transparent; }}"
        )
        top_line.addWidget(priority_label, 0, Qt.AlignTop)

        layout.addLayout(top_line)

        bottom_line = QHBoxLayout()
        bottom_line.setSpacing(10)

        if self.manager:
            progress = self.manager.get_task_progress(task.id)
            progress_label = QLabel(f"{progress:.0f}%")
            progress_label.setStyleSheet(
                "QLabel { color: #4ea1ff; font-size: 9px; font-weight: bold; background: transparent; }"
            )
            bottom_line.addWidget(progress_label)

        if task.due_date:
            try:
                due_date = datetime.fromisoformat(task.due_date).date()
                due_text = task.due_date
                if not task.completed and due_date < datetime.now().date():
                    due_label = QLabel(due_text)
                    due_label.setStyleSheet(
                        "QLabel { color: #ff6b6b; font-size: 9px; background: transparent; }"
                    )
                else:
                    due_label = QLabel(due_text)
                    due_label.setStyleSheet(
                        "QLabel { color: #7f8794; font-size: 9px; background: transparent; }"
                    )
                bottom_line.addWidget(due_label)
            except Exception:
                pass

        if self.manager and task.labels:
            for label_id in task.labels[:2]:
                label = self.manager.get_label(label_id)
                if label:
                    label_widget = LabelWidget(label.name, label.color, label.text_color)
                    label_widget.setFixedHeight(16)
                    label_widget.setMinimumWidth(38)
                    bottom_line.addWidget(label_widget)
            if len(task.labels) > 2:
                more = QLabel(f"+{len(task.labels) - 2}")
                more.setStyleSheet(
                    "QLabel { color: #7f8794; font-size: 9px; background: transparent; }"
                )
                bottom_line.addWidget(more)

        bottom_line.addStretch()
        layout.addLayout(bottom_line)

        widget.setStyleSheet("""
            QWidget#taskRow {
                background-color: transparent;
                border-radius: 4px;
            }
            QWidget#taskRow:hover {
                background-color: #23262c;
            }
        """)

        item = QListWidgetItem()
        item.setData(Qt.UserRole, task.id)
        item.setSizeHint(widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, widget)
        item.setBackground(QColor(0, 0, 0, 0))
        return item

    def select_task(self, task_id):
        for i in range(self.count()):
            item = self.item(i)
            if item.data(Qt.UserRole) == task_id:
                self.blockSignals(True)
                self.setCurrentItem(item)
                self.blockSignals(False)
                return
        self.blockSignals(True)
        self.clearSelection()
        self.blockSignals(False)

    def get_current_task_id(self):
        item = self.currentItem()
        if item:
            return item.data(Qt.UserRole)
        return None

    def on_current_changed(self, current, previous):
        if previous is not None:
            prev_widget = self.itemWidget(previous)
            if prev_widget:
                prev_widget.setStyleSheet("""
                    QWidget#taskRow {
                        background-color: transparent;
                        border-radius: 4px;
                    }
                """)

        if current is not None:
            cur_widget = self.itemWidget(current)
            if cur_widget:
                cur_widget.setStyleSheet("""
                    QWidget#taskRow {
                        background-color: #2a6fb0;
                        border-radius: 4px;
                    }
                """)

            task_id = current.data(Qt.UserRole)
            if task_id:
                self.task_selected.emit(task_id)