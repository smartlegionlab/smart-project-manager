# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
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
    QListWidget,
    QWidget,
    QGridLayout,
    QComboBox,
    QDateEdit
)
from PyQt5.QtCore import Qt, QDate

from smart_project_manager.models.subtask import SubTask
from smart_project_manager.ui.dialogs.label_manager_dialog import LabelManagerDialog
from smart_project_manager.ui.widgets.label_widget import LabelWidget


class SubTaskDialog(QDialog):

    def __init__(self, parent=None, subtask: SubTask = None, manager=None,
                 task_id: str = None, project_id: str = None):
        super().__init__(parent)
        self.is_edit_mode = subtask is not None
        self.subtask = subtask
        self.manager = manager
        self.task_id = task_id if task_id else (subtask.task_id if subtask else None)
        self.project_id = project_id if project_id else (subtask.project_id if subtask else None)

        self.setWindowTitle('Edit Subtask' if self.is_edit_mode else 'Create New Subtask')
        self.setMinimumWidth(450)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        title_group = QFrame()
        title_group.setFrameStyle(QFrame.StyledPanel)
        title_layout = QVBoxLayout(title_group)

        self.title_label = QLabel('Subtask Title:')
        title_layout.addWidget(self.title_label)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter subtask title")
        if subtask:
            self.title_input.setText(subtask.title)
        title_layout.addWidget(self.title_input)

        self.layout.addWidget(title_group)

        desc_group = QFrame()
        desc_group.setFrameStyle(QFrame.StyledPanel)
        desc_layout = QVBoxLayout(desc_group)

        self.desc_label = QLabel('Description (optional):')
        desc_layout.addWidget(self.desc_label)

        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        self.desc_input.setPlaceholderText("Enter subtask description")
        if subtask and subtask.description:
            self.desc_input.setText(subtask.description)
        desc_layout.addWidget(self.desc_input)

        self.layout.addWidget(desc_group)

        settings_group = QFrame()
        settings_group.setFrameStyle(QFrame.StyledPanel)
        settings_layout = QGridLayout(settings_group)

        self.priority_label = QLabel('Priority:')
        settings_layout.addWidget(self.priority_label, 0, 0)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["High", "Medium", "Low"])
        if subtask:
            self.priority_combo.setCurrentIndex(subtask.priority - 1)
        else:
            self.priority_combo.setCurrentIndex(2)
        settings_layout.addWidget(self.priority_combo, 0, 1)

        self.due_label = QLabel('Due Date (optional):')
        settings_layout.addWidget(self.due_label, 1, 0)

        self.due_input = QDateEdit()
        self.due_input.setCalendarPopup(True)
        self.due_input.setDate(QDate.currentDate().addDays(7))
        if subtask and subtask.due_date:
            self.due_input.setDate(QDate.fromString(subtask.due_date, Qt.ISODate))
        settings_layout.addWidget(self.due_input, 1, 1)

        settings_layout.setColumnStretch(2, 1)
        self.layout.addWidget(settings_group)

        labels_group = QFrame()
        labels_group.setFrameStyle(QFrame.StyledPanel)
        labels_layout = QVBoxLayout(labels_group)

        labels_header = QHBoxLayout()
        self.labels_label = QLabel('Labels (optional):')
        labels_header.addWidget(self.labels_label)

        self.btn_add_label = QPushButton('+ Add Label')
        self.btn_add_label.clicked.connect(self.add_label)
        self.btn_add_label.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 11px;
            }
        """)
        labels_header.addWidget(self.btn_add_label)

        labels_header.addStretch()
        labels_layout.addLayout(labels_header)

        self.labels_list = QListWidget()
        self.labels_list.setMaximumHeight(80)
        self.labels_list.setStyleSheet("""
            QListWidget {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 3px;
            }
        """)
        labels_layout.addWidget(self.labels_list)

        self.layout.addWidget(labels_group)

        self.selected_labels_widget = QWidget()
        self.selected_labels_layout = QHBoxLayout(self.selected_labels_widget)
        self.selected_labels_layout.setContentsMargins(0, 0, 0, 0)
        self.selected_labels_layout.setSpacing(5)
        self.layout.addWidget(self.selected_labels_widget)

        self.selected_label_ids = []
        if subtask:
            self.selected_label_ids = subtask.labels.copy()
            self.update_selected_labels_display()

        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        button_text = 'Update Subtask' if self.is_edit_mode else 'Create Subtask'
        self.submit_button = QPushButton(button_text)
        self.submit_button.setDefault(True)
        self.submit_button.setStyleSheet("background-color: #2a82da; color: white;")
        self.submit_button.clicked.connect(self.accept)
        button_layout.addWidget(self.submit_button)

        self.layout.addLayout(button_layout)

    def add_label(self):
        dialog = LabelManagerDialog(self, self.manager)
        dialog.label_selected.connect(self.on_label_selected)
        dialog.exec_()

    def on_label_selected(self, label_id: str):
        if label_id not in self.selected_label_ids:
            self.selected_label_ids.append(label_id)
            self.update_selected_labels_display()

    def update_selected_labels_display(self):
        for i in reversed(range(self.selected_labels_layout.count())):
            widget = self.selected_labels_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for label_id in self.selected_label_ids:
            label = self.manager.get_label(label_id)
            if label:
                label_widget = LabelWidget(label.name, label.color)

                remove_btn = QPushButton('×')
                remove_btn.setFixedSize(20, 20)
                remove_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        border-radius: 10px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                """)
                remove_btn.clicked.connect(lambda checked, lid=label_id: self.remove_label(lid))

                container = QWidget()
                container_layout = QHBoxLayout(container)
                container_layout.setContentsMargins(0, 0, 0, 0)
                container_layout.setSpacing(2)
                container_layout.addWidget(label_widget)
                container_layout.addWidget(remove_btn)

                self.selected_labels_layout.addWidget(container)

        self.selected_labels_layout.addStretch()

    def remove_label(self, label_id: str):
        if label_id in self.selected_label_ids:
            self.selected_label_ids.remove(label_id)
            self.update_selected_labels_display()

    def get_subtask_data(self) -> dict:
        priority_map = {"High": 1, "Medium": 2, "Low": 3}

        return {
            'title': self.title_input.text().strip(),
            'description': self.desc_input.toPlainText().strip() or None,
            'priority': priority_map[self.priority_combo.currentText()],
            'due_date': self.due_input.date().toString(
                Qt.ISODate) if self.due_input.date() != QDate.currentDate().addDays(7) else None,
            'labels': self.selected_label_ids,
            'task_id': self.task_id,
            'project_id': self.project_id
        }

    def accept(self):
        data = self.get_subtask_data()

        if not data['title']:
            QMessageBox.warning(self, 'Error', 'Subtask title is required')
            return

        super().accept()
