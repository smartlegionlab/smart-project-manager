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
    QGridLayout
)

from smart_project_manager.core.models.project import Project


class ProjectDialog(QDialog):

    def __init__(self, parent=None, project: Project = None, manager=None):
        super().__init__(parent)
        self.is_edit_mode = project is not None
        self.project = project
        self.manager = manager

        self.setWindowTitle('Edit Project' if self.is_edit_mode else 'Create New Project')
        self.setMinimumWidth(500)
        self.setMinimumHeight(250)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        name_group = QFrame()
        name_group.setFrameStyle(QFrame.StyledPanel)
        name_layout = QGridLayout(name_group)
        name_layout.setContentsMargins(10, 10, 10, 10)

        self.name_label = QLabel('Project Name:')
        name_layout.addWidget(self.name_label, 0, 0)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter project name")
        self.name_input.setFocus()
        if project:
            self.name_input.setText(project.name)
        name_layout.addWidget(self.name_input, 0, 1)

        self.layout.addWidget(name_group)

        desc_group = QFrame()
        desc_group.setFrameStyle(QFrame.StyledPanel)
        desc_layout = QVBoxLayout(desc_group)
        desc_layout.setContentsMargins(10, 10, 10, 10)

        self.desc_label = QLabel('Description:')
        desc_layout.addWidget(self.desc_label)

        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(150)
        self.desc_input.setPlaceholderText("Enter project description")
        if project and project.description:
            self.desc_input.setText(project.description)
        desc_layout.addWidget(self.desc_input)

        self.layout.addWidget(desc_group)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                background-color: #4a4d55;
                color: white;
            }
            QPushButton:hover {
                background-color: #5a5d65;
            }
        """)
        button_layout.addWidget(self.cancel_button)

        button_layout.addStretch()

        button_text = 'Update Project' if self.is_edit_mode else 'Create Project'
        self.submit_button = QPushButton(button_text)
        self.submit_button.setDefault(True)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                padding: 8px 24px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0066b3;
            }
        """)
        self.submit_button.clicked.connect(self.accept)
        button_layout.addWidget(self.submit_button)

        self.layout.addLayout(button_layout)

    def get_project_data(self) -> dict:
        return {
            'name': self.name_input.text().strip(),
            'description': self.desc_input.toPlainText().strip() or None
        }

    def accept(self):
        data = self.get_project_data()

        if not data['name']:
            QMessageBox.warning(self, 'Error', 'Project name is required')
            return

        super().accept()
