# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from datetime import datetime

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QHeaderView,
    QMessageBox,
    QFrame,
    QDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

from smart_project_manager.ui.dialogs.subtask_dialog import SubTaskDialog
from smart_project_manager.ui.widgets.priority_widget import PriorityIndicatorWidget
from smart_project_manager.ui.widgets.label_widget import LabelWidget


class SubtaskPanelWidget(QWidget):
    panel_closed = pyqtSignal()
    subtask_updated = pyqtSignal()

    def __init__(self, parent=None, manager=None, sound_manager=None):
        super().__init__(parent)
        self.manager = manager
        self.sound_manager = sound_manager
        self.current_task = None
        self.current_project_id = None

        self.setup_ui()
        self.hide()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()

        self.title_label = QLabel('Subtasks')
        self.title_label.setFont(QFont("Arial", 12, QFont.Bold))
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        self.btn_close = QPushButton('×')
        self.btn_close.setFixedSize(30, 30)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.btn_close.clicked.connect(self.on_close_clicked)
        header_layout.addWidget(self.btn_close)

        layout.addLayout(header_layout)

        button_layout = QHBoxLayout()

        self.btn_add_subtask = QPushButton('+ Add Subtask')
        self.btn_add_subtask.clicked.connect(self.on_click)
        self.btn_add_subtask.clicked.connect(self.add_subtask)
        self.btn_add_subtask.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1a72ca;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        button_layout.addWidget(self.btn_add_subtask)

        button_layout.addStretch()

        layout.addLayout(button_layout)

        self.subtasks_table = QTableWidget()
        self.subtasks_table.setColumnCount(7)
        self.subtasks_table.setHorizontalHeaderLabels(
            ['Title', 'Priority', 'Status', 'Due Date', 'Labels', 'Edit', 'Delete'])
        self.subtasks_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.subtasks_table.setAlternatingRowColors(True)
        self.subtasks_table.setStyleSheet("""
            QTableWidget {
                background-color: #2a2a2a;
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #353535;
                padding: 8px;
                border: 1px solid #444;
                font-weight: bold;
            }
        """)

        self.subtasks_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.subtasks_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.subtasks_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.subtasks_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.subtasks_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.subtasks_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.subtasks_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)

        layout.addWidget(self.subtasks_table)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #444; max-height: 1px;")
        layout.addWidget(separator)

    def show_for_task(self, task, project_id):
        self.current_task = task
        self.current_project_id = project_id
        self.title_label.setText(f'Subtasks for "{task.title}"')
        self.load_subtasks()
        self.show()

    def hide_panel(self):
        self.current_task = None
        self.current_project_id = None
        self.subtasks_table.setRowCount(0)
        self.hide()
        self.panel_closed.emit()

    def on_close_clicked(self):
        self.on_click()
        self.hide_panel()

    def load_subtasks(self):
        if not self.current_task:
            return

        self.subtasks_table.setRowCount(0)
        subtasks = self.manager.get_subtasks_by_task(self.current_task.id)

        for row, subtask in enumerate(subtasks):
            self.subtasks_table.insertRow(row)
            self.subtasks_table.setRowHeight(row, 40)

            title_widget = QWidget()
            title_layout = QVBoxLayout(title_widget)
            title_layout.setContentsMargins(5, 2, 5, 2)
            title_layout.setSpacing(2)

            title_label = QLabel(subtask.title)
            if subtask.completed:
                title_label.setStyleSheet("color: #888; text-decoration: line-through;")
            else:
                title_label.setStyleSheet("color: #fff;")

            title_layout.addWidget(title_label)

            if subtask.description:
                desc_label = QLabel(
                    subtask.description[:50] + "..." if len(subtask.description) > 50 else subtask.description)
                desc_label.setStyleSheet("color: #888; font-size: 10px;")
                title_layout.addWidget(desc_label)

            self.subtasks_table.setCellWidget(row, 0, title_widget)

            priority_widget = PriorityIndicatorWidget(subtask.priority)
            self.subtasks_table.setCellWidget(row, 1, priority_widget)

            status_button = QPushButton("✅ Completed" if subtask.completed else "⏳ Pending")
            status_button.setCheckable(True)
            status_button.setChecked(subtask.completed)
            status_button.setStyleSheet("""
                QPushButton {
                    border-radius: 3px;
                    padding: 5px 10px;
                    min-width: 100px;
                }
                QPushButton:checked {
                    background-color: #2e7d32;
                    color: white;
                }
                QPushButton:!checked {
                    background-color: #ff9800;
                    color: white;
                }
            """)
            status_button.clicked.connect(lambda checked, sid=subtask.id: self.toggle_subtask_status(sid))
            self.subtasks_table.setCellWidget(row, 2, status_button)

            due_widget = QWidget()
            due_layout = QHBoxLayout(due_widget)
            due_layout.setContentsMargins(5, 0, 5, 0)
            due_layout.setAlignment(Qt.AlignCenter)

            if subtask.due_date:
                due_label = QLabel(subtask.due_date)
                try:
                    due_date = datetime.fromisoformat(subtask.due_date).date()
                    today = datetime.now().date()
                    if due_date < today and not subtask.completed:
                        due_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
                    elif due_date == today and not subtask.completed:
                        due_label.setStyleSheet("color: #f39c12; font-weight: bold;")
                    else:
                        due_label.setStyleSheet("color: #888;")
                except:
                    due_label.setStyleSheet("color: #888;")
            else:
                due_label = QLabel("—")
                due_label.setStyleSheet("color: #666; font-style: italic;")

            due_layout.addWidget(due_label)
            self.subtasks_table.setCellWidget(row, 3, due_widget)

            labels_widget = QWidget()
            labels_layout = QHBoxLayout(labels_widget)
            labels_layout.setContentsMargins(5, 2, 5, 2)
            labels_layout.setSpacing(3)

            if subtask.labels:
                for label_id in subtask.labels[:3]:
                    label = self.manager.get_label(label_id)
                    if label:
                        label_widget = LabelWidget(label.name, label.color, label.text_color)
                        label_widget.setFixedHeight(24)
                        labels_layout.addWidget(label_widget)

                if len(subtask.labels) > 3:
                    more_label = QLabel(f"+{len(subtask.labels) - 3}")
                    more_label.setStyleSheet("""
                        color: #888;
                        font-size: 10px;
                        padding: 2px 4px;
                        background-color: #3a3a3a;
                        border-radius: 3px;
                    """)
                    labels_layout.addWidget(more_label)
            else:
                no_labels = QLabel("—")
                no_labels.setStyleSheet("color: #666; font-style: italic; font-size: 10px;")
                labels_layout.addWidget(no_labels)

            labels_layout.addStretch()
            self.subtasks_table.setCellWidget(row, 4, labels_widget)

            edit_button = QPushButton("✏️ Edit")
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #ff9800;
                    color: white;
                    border-radius: 3px;
                    padding: 5px 10px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #e68900;
                }
            """)
            edit_button.clicked.connect(lambda checked, sid=subtask.id: self.edit_subtask(sid))
            self.subtasks_table.setCellWidget(row, 5, edit_button)

            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #da2a2a;
                    color: white;
                    border-radius: 3px;
                    padding: 5px 10px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #ca1a1a;
                }
            """)
            delete_button.clicked.connect(lambda checked, sid=subtask.id: self.delete_subtask(sid))
            self.subtasks_table.setCellWidget(row, 6, delete_button)

    def add_subtask(self):
        self.on_notify()
        if not self.current_task:
            return

        dialog = SubTaskDialog(
            self,
            manager=self.manager,
            task_id=self.current_task.id,
            project_id=self.current_project_id,
            sound_manager=self.sound_manager
        )

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_subtask_data()

            if not data['title']:
                self.on_error()
                QMessageBox.warning(self, 'Error', 'Subtask title is required')
                return

            self.manager.create_subtask(**data)
            self.load_subtasks()
            self.subtask_updated.emit()

    def toggle_subtask_status(self, subtask_id: str):
        self.on_notify()
        subtask = self.manager.get_subtask(subtask_id)
        if subtask:
            subtask.toggle_complete()
            self.manager.update_subtask(subtask_id, completed=subtask.completed)
            self.load_subtasks()
            self.subtask_updated.emit()

            main_window = self.get_main_window()
            if main_window and main_window.current_project_id:
                main_window.update_clear_completed_button()

    def edit_subtask(self, subtask_id: str):
        self.on_notify()
        subtask = self.manager.get_subtask(subtask_id)
        if not subtask:
            return

        dialog = SubTaskDialog(self, subtask=subtask, manager=self.manager, sound_manager=self.sound_manager)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_subtask_data()

            if not data['title']:
                QMessageBox.warning(self, 'Error', 'Subtask title is required')
                return

            self.manager.update_subtask(subtask_id, **data)
            self.load_subtasks()
            self.subtask_updated.emit()

    def delete_subtask(self, subtask_id: str):
        self.on_notify()
        subtask = self.manager.get_subtask(subtask_id)
        if not subtask:
            return

        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            f'Delete subtask "{subtask.title}"?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.manager.delete_subtask(subtask_id)
            self.load_subtasks()
            self.subtask_updated.emit()

    def on_click(self):
        if self.sound_manager:
            self.sound_manager.play_click()

    def on_notify(self):
        if self.sound_manager:
            self.sound_manager.play_notify()

    def on_error(self):
        if self.sound_manager:
            self.sound_manager.play_error()

    def get_main_window(self):
        parent = self.parent()
        while parent:
            if hasattr(parent, 'update_clear_completed_button'):
                return parent
            parent = parent.parent()
        return None
