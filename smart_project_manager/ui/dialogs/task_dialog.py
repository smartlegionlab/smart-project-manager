# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QMessageBox,
    QFrame,
    QWidget,
    QGridLayout,
    QComboBox,
    QDateEdit,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QProgressBar
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate, pyqtSignal

from smart_project_manager.core.models.task import Task
from smart_project_manager.ui.dialogs.label_manager_dialog import LabelManagerDialog
from smart_project_manager.ui.dialogs.subtask_dialog import SubTaskDialog
from smart_project_manager.ui.widgets.label_widget import LabelWidget
from smart_project_manager.ui.widgets.priority_widget import PriorityIndicatorWidget


class TaskDialog(QDialog):
    task_updated = pyqtSignal()

    def __init__(self, parent=None, task: Task = None, manager=None, project_id: str = None):
        super().__init__(parent)
        self.is_edit_mode = task is not None
        self.task = task
        self.manager = manager
        self.project_id = project_id if project_id else (task.project_id if task else None)
        self.max_labels = 3

        self.setWindowTitle('Edit Task' if self.is_edit_mode else 'Create New Task')
        self.setMinimumSize(700, 600)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        self.tabs = QTabWidget()

        self.main_tab = QWidget()
        self.setup_main_tab()
        self.tabs.addTab(self.main_tab, "Task Details")

        if self.is_edit_mode:
            self.subtasks_tab = QWidget()
            self.setup_subtasks_tab()
            self.tabs.addTab(self.subtasks_tab, f"Subtasks ({len(task.subtasks)})")

        self.layout.addWidget(self.tabs)

        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        button_text = 'Update Task' if self.is_edit_mode else 'Create Task'
        self.submit_button = QPushButton(button_text)
        self.submit_button.setDefault(True)
        self.submit_button.setStyleSheet("background-color: #2a82da; color: white;")
        self.submit_button.clicked.connect(self.accept)
        button_layout.addWidget(self.submit_button)

        self.layout.addLayout(button_layout)

    def setup_main_tab(self):
        layout = QVBoxLayout(self.main_tab)
        layout.setSpacing(10)

        title_group = QFrame()
        title_group.setFrameStyle(QFrame.StyledPanel)
        title_layout = QVBoxLayout(title_group)

        self.title_label = QLabel('Task Title:')
        title_layout.addWidget(self.title_label)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter task title")
        if self.task:
            self.title_input.setText(self.task.title)
        title_layout.addWidget(self.title_input)

        layout.addWidget(title_group)

        desc_group = QFrame()
        desc_group.setFrameStyle(QFrame.StyledPanel)
        desc_layout = QVBoxLayout(desc_group)

        self.desc_label = QLabel('Description:')
        desc_layout.addWidget(self.desc_label)

        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(150)
        self.desc_input.setPlaceholderText("Enter task description")
        if self.task and self.task.description:
            self.desc_input.setText(self.task.description)
        desc_layout.addWidget(self.desc_input)

        layout.addWidget(desc_group)

        settings_group = QFrame()
        settings_group.setFrameStyle(QFrame.StyledPanel)
        settings_layout = QGridLayout(settings_group)

        self.priority_label = QLabel('Priority:')
        settings_layout.addWidget(self.priority_label, 0, 0)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["High", "Medium", "Low"])
        if self.task:
            self.priority_combo.setCurrentIndex(self.task.priority - 1)
        else:
            self.priority_combo.setCurrentIndex(2)
        settings_layout.addWidget(self.priority_combo, 0, 1)

        self.due_label = QLabel('Due Date (optional):')
        settings_layout.addWidget(self.due_label, 1, 0)

        self.due_input = QDateEdit()
        self.due_input.setCalendarPopup(True)
        self.due_input.setDate(QDate.currentDate().addDays(7))
        if self.task and self.task.due_date:
            self.due_input.setDate(QDate.fromString(self.task.due_date, Qt.ISODate))
        settings_layout.addWidget(self.due_input, 1, 1)

        if self.is_edit_mode:
            self.progress_label = QLabel('Progress:')
            settings_layout.addWidget(self.progress_label, 2, 0)

            self.progress_bar = QProgressBar()
            self.progress_bar.setValue(int(self.manager.get_task_progress(self.task.id)))
            settings_layout.addWidget(self.progress_bar, 2, 1)

        settings_layout.setColumnStretch(2, 1)
        layout.addWidget(settings_group)

        labels_group = QFrame()
        labels_group.setFrameStyle(QFrame.StyledPanel)
        labels_layout = QVBoxLayout(labels_group)

        labels_header = QHBoxLayout()
        self.labels_label = QLabel('Labels (optional):')
        labels_header.addWidget(self.labels_label)

        self.labels_counter = QLabel(f'0/{self.max_labels}')
        self.labels_counter.setStyleSheet("color: #888; font-size: 12px;")
        labels_header.addWidget(self.labels_counter)

        self.btn_add_label = QPushButton('+ Add Labels')
        self.btn_add_label.clicked.connect(self.add_label)
        self.btn_add_label.setStyleSheet("""
                    QPushButton {
                        background-color: #27ae60;
                        color: white;
                        padding: 5px 10px;
                        border-radius: 3px;
                        font-size: 11px;
                    }
                    QPushButton:disabled {
                        background-color: #666;
                        color: #999;
                    }
                """)
        labels_header.addWidget(self.btn_add_label)

        labels_header.addStretch()
        labels_layout.addLayout(labels_header)

        self.selected_labels_container = QWidget()
        self.selected_labels_container.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 3px;
            }
        """)
        self.selected_labels_container.setMinimumHeight(50)
        self.selected_labels_layout = QHBoxLayout(self.selected_labels_container)
        self.selected_labels_layout.setContentsMargins(8, 8, 8, 8)
        self.selected_labels_layout.setSpacing(5)

        labels_layout.addWidget(self.selected_labels_container)

        layout.addWidget(labels_group)

        self.selected_label_ids = []
        if self.task:
            self.selected_label_ids = self.task.labels.copy()
            self.update_selected_labels_display()

        layout.addStretch()

    def setup_subtasks_tab(self):
        layout = QVBoxLayout(self.subtasks_tab)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()

        header_label = QLabel(f'Subtasks for "{self.task.title}"')
        header_label.setFont(QFont("Arial", 12, QFont.Bold))
        header_layout.addWidget(header_label)

        header_layout.addStretch()

        self.btn_add_subtask = QPushButton('+ Add Subtask')
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
        """)
        header_layout.addWidget(self.btn_add_subtask)

        layout.addLayout(header_layout)

        self.subtasks_table = QTableWidget()
        self.subtasks_table.setColumnCount(6)
        self.subtasks_table.setHorizontalHeaderLabels(['Title', 'Priority', 'Status', 'Due Date', 'Edit', 'Delete'])
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

        layout.addWidget(self.subtasks_table)

        self.load_subtasks()

    def add_label(self):
        if len(self.selected_label_ids) >= self.max_labels:
            QMessageBox.warning(self, 'Limit Reached',
                                f'You can only select up to {self.max_labels} labels.')
            return

        dialog = LabelManagerDialog(
            self,
            self.manager,
            multi_select=True,
            max_selection=self.max_labels,
            pre_selected_ids=self.selected_label_ids
        )
        dialog.multiple_labels_selected.connect(self.on_labels_selected)

        dialog.exec_()

    def on_labels_selected(self, label_ids: list):
        new_label_ids = [lid for lid in label_ids if lid not in self.selected_label_ids]

        remaining_slots = self.max_labels - len(self.selected_label_ids)

        if remaining_slots <= 0:
            QMessageBox.warning(self, 'Limit Reached',
                                f'You can only select up to {self.max_labels} labels.')
            return

        if not new_label_ids:
            QMessageBox.information(self, 'No New Labels',
                                    'All selected labels are already added.')
            return

        added_count = 0
        for label_id in new_label_ids:
            if len(self.selected_label_ids) < self.max_labels:
                self.selected_label_ids.append(label_id)
                added_count += 1
            else:
                break

        if added_count > 0:
            self.update_selected_labels_display()

            if added_count < len(new_label_ids):
                not_added = len(new_label_ids) - added_count
                QMessageBox.information(self, 'Partial Selection',
                                        f'Added {added_count} new label(s). {not_added} label(s) not added due to limit.')
            else:
                QMessageBox.information(self, 'Labels Added',
                                        f'Successfully added {added_count} label(s).')

    def on_label_selected(self, label_id: str):
        if len(self.selected_label_ids) >= self.max_labels:
            QMessageBox.warning(self, 'Limit Reached',
                                f'You can only select up to {self.max_labels} labels.')
            return

        if label_id not in self.selected_label_ids:
            self.selected_label_ids.append(label_id)
            self.update_selected_labels_display()
        else:
            QMessageBox.information(self, 'Already Added',
                                    'This label is already selected.')

    def update_selected_labels_display(self):
        for i in reversed(range(self.selected_labels_layout.count())):
            item = self.selected_labels_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            elif item.spacerItem():
                self.selected_labels_layout.removeItem(item)

        current_count = len(self.selected_label_ids)
        self.labels_counter.setText(f'{current_count}/{self.max_labels}')

        self.btn_add_label.setEnabled(current_count < self.max_labels)

        if current_count > 0:
            for label_id in self.selected_label_ids:
                label = self.manager.get_label(label_id)
                if label:
                    label_widget = LabelWidget(label.name, label.color, label.text_color)

                    remove_btn = QPushButton('×')
                    remove_btn.setFixedSize(20, 20)
                    remove_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #e74c3c;
                            color: white;
                            border-radius: 10px;
                            font-weight: bold;
                            font-size: 12px;
                        }
                        QPushButton:hover {
                            background-color: #c0392b;
                        }
                    """)
                    remove_btn.clicked.connect(lambda checked, lid=label_id: self.remove_label(lid))

                    container = QWidget()
                    container.setStyleSheet("background-color: #353535; border-radius: 3px;")
                    container_layout = QHBoxLayout(container)
                    container_layout.setContentsMargins(5, 2, 5, 2)
                    container_layout.setSpacing(5)
                    container_layout.addWidget(label_widget)
                    container_layout.addWidget(remove_btn)

                    self.selected_labels_layout.addWidget(container)

            if current_count > self.max_labels:
                limit_label = QLabel(f'✓ Maximum {self.max_labels} labels selected')
                limit_label.setStyleSheet("color: #27ae60; font-size: 11px;")
                self.selected_labels_layout.addWidget(limit_label)

            self.selected_labels_layout.addStretch()
        else:
            no_labels_label = QLabel('No labels selected. Click "+ Add Labels" to add.')
            no_labels_label.setStyleSheet("color: #888; font-style: italic; font-size: 11px;")
            no_labels_label.setAlignment(Qt.AlignCenter)
            self.selected_labels_layout.addWidget(no_labels_label, alignment=Qt.AlignCenter)
            self.selected_labels_layout.addStretch()

    def remove_label(self, label_id: str):
        if label_id in self.selected_label_ids:
            self.selected_label_ids.remove(label_id)
            self.update_selected_labels_display()

    def add_subtask(self):
        dialog = SubTaskDialog(self, manager=self.manager, task_id=self.task.id, project_id=self.task.project_id)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_subtask_data()

            if not data['title']:
                QMessageBox.warning(self, 'Error', 'Subtask title is required')
                return

            self.manager.create_subtask(**data)
            self.load_subtasks()
            self.task_updated.emit()

    def load_subtasks(self):
        self.subtasks_table.setRowCount(0)

        subtasks = self.manager.get_subtasks_by_task(self.task.id)

        for row, subtask in enumerate(subtasks):
            self.subtasks_table.insertRow(row)

            title_item = QTableWidgetItem(subtask.title)
            if subtask.description:
                title_item.setToolTip(subtask.description)
            if subtask.completed:
                title_item.setForeground(QColor(100, 100, 100))
                font = title_item.font()
                font.setStrikeOut(True)
                title_item.setFont(font)
            self.subtasks_table.setItem(row, 0, title_item)

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

            due_text = subtask.due_date if subtask.due_date else "No due date"
            due_item = QTableWidgetItem(due_text)
            due_item.setTextAlignment(Qt.AlignCenter)
            self.subtasks_table.setItem(row, 3, due_item)

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
            self.subtasks_table.setCellWidget(row, 4, edit_button)

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
            self.subtasks_table.setCellWidget(row, 5, delete_button)

    def toggle_subtask_status(self, subtask_id: str):
        subtask = self.manager.get_subtask(subtask_id)
        if subtask:
            subtask.toggle_complete()
            self.manager.update_subtask(subtask_id, completed=subtask.completed)
            self.load_subtasks()
            self.task_updated.emit()

    def edit_subtask(self, subtask_id: str):
        subtask = self.manager.get_subtask(subtask_id)
        if not subtask:
            return

        dialog = SubTaskDialog(self, subtask=subtask, manager=self.manager)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_subtask_data()

            if not data['title']:
                QMessageBox.warning(self, 'Error', 'Subtask title is required')
                return

            self.manager.update_subtask(subtask_id, **data)
            self.load_subtasks()
            self.task_updated.emit()

    def delete_subtask(self, subtask_id: str):
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
            self.task_updated.emit()

    def get_task_data(self) -> dict:
        priority_map = {"High": 1, "Medium": 2, "Low": 3}

        return {
            'title': self.title_input.text().strip(),
            'description': self.desc_input.toPlainText().strip() or None,
            'priority': priority_map[self.priority_combo.currentText()],
            'due_date': self.due_input.date().toString(
                Qt.ISODate) if self.due_input.date() != QDate.currentDate().addDays(7) else None,
            'labels': self.selected_label_ids,
            'project_id': self.project_id
        }

    def accept(self):
        data = self.get_task_data()

        if not data['title']:
            QMessageBox.warning(self, 'Error', 'Task title is required')
            return

        super().accept()
