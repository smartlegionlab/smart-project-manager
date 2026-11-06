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
    QGridLayout,
    QComboBox,
    QDateEdit,
    QProgressBar
)
from PyQt5.QtCore import Qt, QDate, pyqtSignal

from smart_project_manager.core.models.task import Task


TASK_TITLE_MAX_LENGTH = 100
TASK_DESCRIPTION_MAX_LENGTH = 2000


class TaskDialog(QDialog):
    task_updated = pyqtSignal()

    def __init__(self, parent=None, task: Task = None,
                 manager=None, project_id: str = None):
        super().__init__(parent)
        self.is_edit_mode = task is not None
        self.task = task
        self.manager = manager
        self.project_id = project_id if project_id else (task.project_id if task else None)

        self.setWindowTitle('Edit Task' if self.is_edit_mode else 'Create New Task')
        self.setMinimumSize(600, 520)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        self.setup_main()

        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        button_text = 'Update Task' if self.is_edit_mode else 'Create Task'
        self.submit_button = QPushButton(button_text)
        self.submit_button.setDefault(True)
        self.submit_button.setStyleSheet("background-color: #007acc; color: white;")
        self.submit_button.clicked.connect(self.accept)
        button_layout.addWidget(self.submit_button)

        self.title_input.setFocus()

        self.layout.addLayout(button_layout)

    def setup_main(self):
        layout = self.layout
        layout.setSpacing(10)

        title_group = QFrame()
        title_group.setFrameStyle(QFrame.StyledPanel)
        title_layout = QVBoxLayout(title_group)
        title_layout.setSpacing(4)

        self.title_label = QLabel('Task Title:')
        title_layout.addWidget(self.title_label)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter task title")
        self.title_input.setMaxLength(TASK_TITLE_MAX_LENGTH)
        if self.task:
            self.title_input.setText(self.task.title)
        self.title_input.textChanged.connect(self.update_title_counter)
        title_layout.addWidget(self.title_input)

        self.title_counter = QLabel()
        self.title_counter.setAlignment(Qt.AlignRight)
        title_layout.addWidget(self.title_counter)

        layout.addWidget(title_group)

        desc_group = QFrame()
        desc_group.setFrameStyle(QFrame.StyledPanel)
        desc_layout = QVBoxLayout(desc_group)
        desc_layout.setSpacing(4)

        self.desc_label = QLabel('Description:')
        desc_layout.addWidget(self.desc_label)

        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(150)
        self.desc_input.setPlaceholderText("Enter task description")
        if self.task and self.task.description:
            self.desc_input.setText(self.task.description)
        self.desc_input.textChanged.connect(self.update_desc_counter)
        desc_layout.addWidget(self.desc_input)

        self.desc_counter = QLabel()
        self.desc_counter.setAlignment(Qt.AlignRight)
        desc_layout.addWidget(self.desc_counter)

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
            self.due_input.setDate(QDate.fromString(self.task.due_date, Qt.DateFormat.ISODate))
        settings_layout.addWidget(self.due_input, 1, 1)

        if self.is_edit_mode:
            self.progress_label = QLabel('Progress:')
            settings_layout.addWidget(self.progress_label, 2, 0)

            self.progress_bar = QProgressBar()
            self.progress_bar.setValue(int(self.manager.get_task_progress(self.task.id)))
            settings_layout.addWidget(self.progress_bar, 2, 1)

        settings_layout.setColumnStretch(2, 1)
        layout.addWidget(settings_group)

        layout.addStretch()

        self.update_title_counter()
        self.update_desc_counter()

    def update_title_counter(self):
        current_length = len(self.title_input.text())
        remaining = TASK_TITLE_MAX_LENGTH - current_length
        self.title_counter.setText(
            f"{current_length}/{TASK_TITLE_MAX_LENGTH} characters"
        )

        if remaining <= 10:
            self.title_counter.setStyleSheet("color: #ff6b6b; font-size: 10px; font-weight: bold;")
        elif remaining <= 30:
            self.title_counter.setStyleSheet("color: #ffa726; font-size: 10px;")
        else:
            self.title_counter.setStyleSheet("color: #888; font-size: 10px;")

    def update_desc_counter(self):
        current_length = len(self.desc_input.toPlainText())
        remaining = TASK_DESCRIPTION_MAX_LENGTH - current_length
        self.desc_counter.setText(
            f"{current_length}/{TASK_DESCRIPTION_MAX_LENGTH} characters"
        )

        if remaining <= 100:
            self.desc_counter.setStyleSheet("color: #ff6b6b; font-size: 10px; font-weight: bold;")
        elif remaining <= 300:
            self.desc_counter.setStyleSheet("color: #ffa726; font-size: 10px;")
        else:
            self.desc_counter.setStyleSheet("color: #888; font-size: 10px;")

    def get_task_data(self) -> dict:
        priority_map = {"High": 1, "Medium": 2, "Low": 3}

        selected_date = self.due_input.date()

        if selected_date.isValid():
            due_date = selected_date.toString(Qt.DateFormat.ISODate)
        else:
            due_date = None

        return {
            'title': self.title_input.text().strip(),
            'description': self.desc_input.toPlainText().strip() or None,
            'priority': priority_map[self.priority_combo.currentText()],
            'due_date': due_date,
            'project_id': self.project_id
        }

    def accept(self):
        data = self.get_task_data()

        if not data['title']:
            QMessageBox.warning(self, 'Error', 'Task title is required')
            return

        if len(data['title']) > TASK_TITLE_MAX_LENGTH:
            QMessageBox.warning(
                self, 'Title Too Long',
                f'Task title cannot exceed {TASK_TITLE_MAX_LENGTH} characters.\n'
                f'Current length: {len(data["title"])} characters.'
            )
            return

        if data['description'] and len(data['description']) > TASK_DESCRIPTION_MAX_LENGTH:
            QMessageBox.warning(
                self, 'Description Too Long',
                f'Task description cannot exceed {TASK_DESCRIPTION_MAX_LENGTH} characters.\n'
                f'Current length: {len(data["description"])} characters.'
            )
            return

        super().accept()
