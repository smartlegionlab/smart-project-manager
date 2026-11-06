# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSignal


class ProjectListWidget(QListWidget):
    project_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
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

    def load_projects(self, projects, manager):
        self.blockSignals(True)
        self.clear()

        if not projects:
            empty = QListWidgetItem()
            empty.setFlags(Qt.NoItemFlags)
            widget = QWidget()
            layout = QVBoxLayout(widget)
            layout.setContentsMargins(16, 20, 16, 20)
            empty_label = QLabel("No projects yet.\nClick + New to create one.")
            empty_label.setStyleSheet("color: #5a606b; font-size: 12px;")
            empty_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(empty_label)
            empty.setSizeHint(widget.sizeHint())
            self.addItem(empty)
            self.setItemWidget(empty, widget)
        else:
            for project in projects:
                self._add_project_row(project, manager)

        self.blockSignals(False)

    def _add_project_row(self, project, manager):
        task_count = len(project.tasks)
        completed_tasks = sum(
            1 for task_id in project.tasks
            if manager.get_task(task_id) and manager.get_task(task_id).completed
        )

        widget = QWidget()
        widget.setObjectName("projectRow")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)

        text_column = QVBoxLayout()
        text_column.setSpacing(2)

        name_label = QLabel(project.name)
        name_label.setStyleSheet(
            "QLabel { color: #ffffff; font-size: 13px; font-weight: bold; background: transparent; }"
        )
        name_label.setWordWrap(True)
        text_column.addWidget(name_label)

        info_text = f"{completed_tasks}/{task_count} tasks"
        if task_count > 0 and completed_tasks == task_count:
            info_text += " • done"
        info_label = QLabel(info_text)
        info_label.setStyleSheet(
            "QLabel { color: #7f8794; font-size: 11px; background: transparent; }"
        )
        text_column.addWidget(info_label)

        layout.addLayout(text_column, 1)

        if task_count > 0 and completed_tasks == task_count:
            dot_color = "#4ee09c"
        elif completed_tasks > 0:
            dot_color = "#ffb454"
        else:
            dot_color = "#3a3f48"

        dot = QLabel()
        dot.setFixedSize(8, 8)
        dot.setStyleSheet(
            f"QLabel {{ background-color: {dot_color}; border-radius: 4px; }}"
        )
        layout.addWidget(dot, 0, Qt.AlignVCenter)

        if project.description:
            widget.setToolTip(project.description)

        item = QListWidgetItem()
        item.setData(Qt.UserRole, project.id)
        item.setSizeHint(widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, widget)

        self._apply_row_style(widget, False)
        return item

    def _apply_row_style(self, widget, selected):
        if selected:
            widget.setStyleSheet("""
                QWidget#projectRow {
                    background-color: #2a6fb0;
                    border-radius: 4px;
                }
            """)
        else:
            widget.setStyleSheet("""
                QWidget#projectRow {
                    background-color: transparent;
                    border-radius: 4px;
                }
                QWidget#projectRow:hover {
                    background-color: #23262c;
                }
            """)

    def set_current_id(self, project_id):
        self.blockSignals(True)

        target_item = None
        for i in range(self.count()):
            item = self.item(i)
            if item.data(Qt.UserRole) == project_id:
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

    def get_current_project_id(self):
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

            project_id = current.data(Qt.UserRole)
            if project_id:
                self.project_selected.emit(project_id)