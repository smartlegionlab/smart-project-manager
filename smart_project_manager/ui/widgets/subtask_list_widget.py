# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from datetime import datetime

from PyQt5.QtWidgets import (
    QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QLabel, QVBoxLayout
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSignal

from smart_project_manager.ui.widgets.label_widget import LabelWidget


class SubtaskListWidget(QListWidget):
    subtask_selected = pyqtSignal(str)

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

    def load_subtasks(self, subtasks):
        self.blockSignals(True)
        self.clear()

        if not subtasks:
            empty = QListWidgetItem()
            empty.setFlags(Qt.NoItemFlags)
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(16, 20, 16, 20)
            empty_label = QLabel("No subtasks yet.\nClick + Add to create one.")
            empty_label.setStyleSheet("color: #5a606b; font-size: 12px;")
            empty_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(empty_label)
            empty.setSizeHint(widget.sizeHint())
            self.addItem(empty)
            self.setItemWidget(empty, widget)
        else:
            for subtask in subtasks:
                self._add_subtask_row(subtask)

        self.blockSignals(False)

    def _add_subtask_row(self, subtask):
        widget = QWidget()
        widget.setObjectName("subtaskRow")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(3)

        top_line = QHBoxLayout()
        top_line.setSpacing(8)

        dot = QLabel()
        dot.setFixedSize(6, 6)
        if subtask.completed:
            dot.setStyleSheet("QLabel { background-color: #4ee09c; border-radius: 3px; }")
        else:
            dot.setStyleSheet("QLabel { background-color: #ffb454; border-radius: 3px; }")
        top_line.addWidget(dot, 0, Qt.AlignTop)

        title_label = QLabel(subtask.title)
        if subtask.completed:
            title_label.setStyleSheet(
                "QLabel { color: #6a7280; font-size: 11px; font-weight: bold; "
                "text-decoration: line-through; background: transparent; }"
            )
        else:
            title_label.setStyleSheet(
                "QLabel { color: #ffffff; font-size: 11px; font-weight: bold; "
                "background: transparent; }"
            )
        title_label.setWordWrap(True)
        top_line.addWidget(title_label, 1)

        priority_text = ["High", "Medium", "Low"][subtask.priority - 1]
        priority_color = ["#ff6b6b", "#ffb454", "#4ee09c"][subtask.priority - 1]
        priority_label = QLabel(priority_text)
        priority_label.setStyleSheet(
            f"QLabel {{ color: {priority_color}; font-size: 9px; font-weight: bold; "
            f"background: transparent; }}"
        )
        top_line.addWidget(priority_label, 0, Qt.AlignTop)

        layout.addLayout(top_line)

        bottom_line = QHBoxLayout()
        bottom_line.setSpacing(10)

        if subtask.due_date:
            try:
                due_date = datetime.fromisoformat(subtask.due_date).date()
                due_text = subtask.due_date
                if not subtask.completed and due_date < datetime.now().date():
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

        if self.manager and subtask.labels:
            for label_id in subtask.labels[:2]:
                label = self.manager.get_label(label_id)
                if label:
                    label_widget = LabelWidget(label.name, label.color, label.text_color)
                    label_widget.setFixedHeight(14)
                    label_widget.setMinimumWidth(34)
                    bottom_line.addWidget(label_widget)

        bottom_line.addStretch()
        layout.addLayout(bottom_line)

        widget.setStyleSheet("""
            QWidget#subtaskRow {
                background-color: transparent;
                border-radius: 4px;
            }
            QWidget#subtaskRow:hover {
                background-color: #23262c;
            }
        """)

        item = QListWidgetItem()
        item.setData(Qt.UserRole, subtask.id)
        item.setSizeHint(widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, widget)
        item.setBackground(QColor(0, 0, 0, 0))
        return item

    def select_subtask(self, subtask_id):
        for i in range(self.count()):
            item = self.item(i)
            if item.data(Qt.UserRole) == subtask_id:
                self.blockSignals(True)
                self.setCurrentItem(item)
                self.blockSignals(False)
                return

    def get_current_subtask_id(self):
        item = self.currentItem()
        if item:
            return item.data(Qt.UserRole)
        return None

    def on_current_changed(self, current, previous):
        if current is not None:
            subtask_id = current.data(Qt.UserRole)
            if subtask_id:
                self.subtask_selected.emit(subtask_id)