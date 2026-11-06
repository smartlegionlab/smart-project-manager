# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QListWidget, QListWidgetItem, QWidget, QHBoxLayout, QLabel, QVBoxLayout,
    QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal


class SubtaskListWidget(QListWidget):
    subtask_selected = pyqtSignal(str)
    subtask_toggled = pyqtSignal(str)

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
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        checkbox = QCheckBox()
        checkbox.setChecked(subtask.completed)
        checkbox.setCursor(Qt.PointingHandCursor)
        checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                border: 1px solid #4a505b;
                background-color: #23262c;
            }
            QCheckBox::indicator:checked {
                background-color: #2a8f5e;
                border: 1px solid #2a8f5e;
            }
        """)
        checkbox.clicked.connect(
            lambda checked, sid=subtask.id: self.subtask_toggled.emit(sid)
        )
        layout.addWidget(checkbox)

        title_label = QLabel(subtask.title)
        if subtask.completed:
            title_label.setStyleSheet(
                "QLabel { color: #6a7280; font-size: 12px; "
                "text-decoration: line-through; background: transparent; }"
            )
        else:
            title_label.setStyleSheet(
                "QLabel { color: #ffffff; font-size: 12px; background: transparent; }"
            )
        title_label.setWordWrap(True)
        layout.addWidget(title_label, 1)

        priority_text = ["High", "Medium", "Low"][subtask.priority - 1]
        priority_color = ["#ff6b6b", "#ffb454", "#4ee09c"][subtask.priority - 1]
        priority_label = QLabel(priority_text)
        priority_label.setStyleSheet(
            f"QLabel {{ color: {priority_color}; font-size: 9px; font-weight: bold; "
            f"background: transparent; }}"
        )
        layout.addWidget(priority_label)

        item = QListWidgetItem()
        item.setData(Qt.UserRole, subtask.id)
        item.setSizeHint(widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, widget)

        self._apply_row_style(widget, False)
        return item

    def _apply_row_style(self, widget, selected):
        if selected:
            widget.setStyleSheet("""
                QWidget#subtaskRow {
                    background-color: #2a6fb0;
                    border-radius: 4px;
                }
            """)
        else:
            widget.setStyleSheet("""
                QWidget#subtaskRow {
                    background-color: transparent;
                    border-radius: 4px;
                }
                QWidget#subtaskRow:hover {
                    background-color: #23262c;
                }
            """)

    def set_current_id(self, subtask_id):
        self.blockSignals(True)

        target_item = None
        for i in range(self.count()):
            item = self.item(i)
            if item.data(Qt.UserRole) == subtask_id:
                target_item = item
                break

        if target_item is not None:
            self.setCurrentItem(target_item)
            for i in range(self.count()):
                widget = self.itemWidget(self.item(i))
                if widget:
                    self._apply_row_style(widget, self.item(i) is target_item)
        else:
            self.clearSelection()

        self.blockSignals(False)

    def get_current_subtask_id(self):
        item = self.currentItem()
        if item:
            return item.data(Qt.UserRole)
        return None

    def on_current_changed(self, current, previous):
        if previous is not None:
            prev_widget = self.itemWidget(previous)
            if prev_widget:
                self._apply_row_style(prev_widget, False)

        if current is not None:
            cur_widget = self.itemWidget(current)
            if cur_widget:
                self._apply_row_style(cur_widget, True)

            subtask_id = current.data(Qt.UserRole)
            if subtask_id:
                self.subtask_selected.emit(subtask_id)
