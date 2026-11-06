from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QFrame, QGridLayout, QComboBox
)
from PyQt5.QtCore import Qt

from smart_project_manager.core.models.subtask import SubTask


SUBTASK_TITLE_MAX_LENGTH = 100


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
        self.setMinimumWidth(460)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(14, 14, 14, 14)

        title_group = QFrame()
        title_group.setFrameStyle(QFrame.StyledPanel)
        title_layout = QVBoxLayout(title_group)
        title_layout.setContentsMargins(10, 10, 10, 10)
        title_layout.setSpacing(4)

        self.title_label = QLabel('Title:')
        title_layout.addWidget(self.title_label)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter subtask title")
        self.title_input.setMaxLength(SUBTASK_TITLE_MAX_LENGTH)
        if subtask:
            self.title_input.setText(subtask.title)
        self.title_input.textChanged.connect(self.update_title_counter)
        title_layout.addWidget(self.title_input)

        self.title_counter = QLabel()
        self.title_counter.setAlignment(Qt.AlignRight)
        title_layout.addWidget(self.title_counter)

        self.layout.addWidget(title_group)

        settings_group = QFrame()
        settings_group.setFrameStyle(QFrame.StyledPanel)
        settings_layout = QGridLayout(settings_group)
        settings_layout.setContentsMargins(10, 10, 10, 10)

        self.priority_label = QLabel('Priority:')
        settings_layout.addWidget(self.priority_label, 0, 0)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["High", "Medium", "Low"])
        if subtask:
            self.priority_combo.setCurrentIndex(subtask.priority - 1)
        else:
            self.priority_combo.setCurrentIndex(2)
        settings_layout.addWidget(self.priority_combo, 0, 1)

        settings_layout.setColumnStretch(2, 1)
        self.layout.addWidget(settings_group)

        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        button_layout.addStretch()

        button_text = 'Update' if self.is_edit_mode else 'Create'
        self.submit_button = QPushButton(button_text)
        self.submit_button.setDefault(True)
        self.submit_button.setStyleSheet(
            "background-color: #007acc; color: white; padding: 6px 18px; border-radius: 4px;"
        )
        self.submit_button.clicked.connect(self.accept)
        button_layout.addWidget(self.submit_button)

        self.layout.addLayout(button_layout)

        self.title_input.setFocus()

        self.update_title_counter()

    def update_title_counter(self):
        current_length = len(self.title_input.text())
        remaining = SUBTASK_TITLE_MAX_LENGTH - current_length
        self.title_counter.setText(
            f"{current_length}/{SUBTASK_TITLE_MAX_LENGTH} characters"
        )

        if remaining <= 10:
            self.title_counter.setStyleSheet("color: #ff6b6b; font-size: 10px; font-weight: bold;")
        elif remaining <= 30:
            self.title_counter.setStyleSheet("color: #ffa726; font-size: 10px;")
        else:
            self.title_counter.setStyleSheet("color: #888; font-size: 10px;")

    def get_subtask_data(self) -> dict:
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        return {
            'title': self.title_input.text().strip(),
            'priority': priority_map[self.priority_combo.currentText()],
            'task_id': self.task_id,
            'project_id': self.project_id
        }

    def accept(self):
        data = self.get_subtask_data()

        if not data['title']:
            QMessageBox.warning(self, 'Error', 'Subtask title is required')
            return

        if len(data['title']) > SUBTASK_TITLE_MAX_LENGTH:
            QMessageBox.warning(
                self, 'Title Too Long',
                f'Subtask title cannot exceed {SUBTASK_TITLE_MAX_LENGTH} characters.\n'
                f'Current length: {len(data["title"])} characters.'
            )
            return

        super().accept()
