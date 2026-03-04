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
    QProgressBar
)
from PyQt5.QtCore import Qt, QDate, pyqtSignal

from smart_project_manager.core.models.task import Task
from smart_project_manager.ui.dialogs.label_manager_dialog import LabelManagerDialog
from smart_project_manager.ui.widgets.label_widget import LabelWidget


class TaskDialog(QDialog):
    task_updated = pyqtSignal()

    def __init__(self, parent=None, task: Task = None,
                 manager=None, project_id: str = None, sound_manager=None):
        super().__init__(parent)
        self.is_edit_mode = task is not None
        self.task = task
        self.manager = manager
        self.project_id = project_id if project_id else (task.project_id if task else None)
        self.max_labels = 3

        self.sound_manager = sound_manager

        self.setWindowTitle('Edit Task' if self.is_edit_mode else 'Create New Task')
        self.setMinimumSize(700, 600)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        self.tabs = QTabWidget()
        self.main_tab = QWidget()
        self.setup_main_tab()
        self.tabs.addTab(self.main_tab, "Task Details")

        self.layout.addWidget(self.tabs)

        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.on_click)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        button_text = 'Update Task' if self.is_edit_mode else 'Create Task'
        self.submit_button = QPushButton(button_text)
        self.submit_button.clicked.connect(self.on_click)
        self.submit_button.setDefault(True)
        self.submit_button.setStyleSheet("background-color: #2a82da; color: white;")
        self.submit_button.clicked.connect(self.accept)
        button_layout.addWidget(self.submit_button)

        self.title_input.setFocus()

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
        self.btn_add_label.clicked.connect(self.on_click)
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

    def add_label(self):
        self.on_notify()
        if len(self.selected_label_ids) >= self.max_labels:
            self.on_error()
            QMessageBox.warning(self, 'Limit Reached',
                                f'You can only select up to {self.max_labels} labels.')
            return

        dialog = LabelManagerDialog(
            self,
            self.manager,
            multi_select=True,
            max_selection=self.max_labels,
            pre_selected_ids=self.selected_label_ids,
            sound_manager=self.sound_manager
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
                                        f'Added {added_count} new label(s).'
                                        f' {not_added} label(s) not added due to limit.')

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

    def get_task_data(self) -> dict:
        priority_map = {"High": 1, "Medium": 2, "Low": 3}

        selected_date = self.due_input.date()

        if selected_date.isValid():
            due_date = selected_date.toString(Qt.ISODate)
        else:
            due_date = None

        return {
            'title': self.title_input.text().strip(),
            'description': self.desc_input.toPlainText().strip() or None,
            'priority': priority_map[self.priority_combo.currentText()],
            'due_date': due_date,
            'labels': self.selected_label_ids,
            'project_id': self.project_id
        }

    def on_click(self):
        if self.sound_manager:
            self.sound_manager.play_click()

    def on_notify(self):
        if self.sound_manager:
            self.sound_manager.play_notify()

    def on_error(self):
        if self.sound_manager:
            self.sound_manager.play_error()

    def accept(self):
        data = self.get_task_data()

        if not data['title']:
            QMessageBox.warning(self, 'Error', 'Task title is required')
            return

        super().accept()
