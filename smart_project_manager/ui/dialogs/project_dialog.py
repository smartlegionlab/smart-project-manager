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
from PyQt5.QtCore import Qt, QUrl

from smart_project_manager.core.models.project import Project


NAME_MAX_LENGTH = 100
DESCRIPTION_MAX_LENGTH = 2000

ALLOWED_WITH_HOST = ('http', 'https', 'ftp', 'ftps', 'git', 'ssh')
ALLOWED_WITH_PATH = ('file', 'mailto')


def is_valid_link(text: str) -> bool:
    if not text:
        return True

    url = QUrl(text)

    if not url.isValid() or url.isRelative():
        return False

    scheme = url.scheme()

    if scheme in ALLOWED_WITH_HOST:
        return bool(url.host())

    if scheme in ALLOWED_WITH_PATH:
        return bool(url.path())

    return False


class ProjectDialog(QDialog):

    def __init__(self, parent=None, project: Project = None, manager=None):
        super().__init__(parent)
        self.is_edit_mode = project is not None
        self.project = project
        self.manager = manager

        self.setWindowTitle('Edit Project' if self.is_edit_mode else 'Create New Project')
        self.setMinimumWidth(560)
        self.setMinimumHeight(300 if not self.is_edit_mode else 420)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(10)

        name_group = QFrame()
        name_group.setFrameStyle(QFrame.StyledPanel)
        name_layout = QGridLayout(name_group)
        name_layout.setContentsMargins(10, 10, 10, 10)
        name_layout.setVerticalSpacing(4)

        self.name_label = QLabel('Project Name:')
        name_layout.addWidget(self.name_label, 0, 0)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter project name")
        self.name_input.setMaxLength(NAME_MAX_LENGTH)
        self.name_input.setFocus()
        if project:
            self.name_input.setText(project.name)
        self.name_input.textChanged.connect(self.update_name_counter)
        name_layout.addWidget(self.name_input, 0, 1)

        self.name_counter = QLabel()
        self.name_counter.setAlignment(Qt.AlignRight)
        name_layout.addWidget(self.name_counter, 1, 1)

        if self.is_edit_mode:
            self.link_label = QLabel('Link (optional):')
            name_layout.addWidget(self.link_label, 2, 0)

            self.link_input = QLineEdit()
            self.link_input.setPlaceholderText("https://github.com/user/repo")
            if project and project.link:
                self.link_input.setText(project.link)
            self.link_input.textChanged.connect(self.validate_link)
            name_layout.addWidget(self.link_input, 2, 1)

            self.link_status = QLabel("")
            self.link_status.setAlignment(Qt.AlignRight)
            self.link_status.setStyleSheet("font-size: 10px;")
            name_layout.addWidget(self.link_status, 3, 1)

        self.layout.addWidget(name_group)

        desc_group = QFrame()
        desc_group.setFrameStyle(QFrame.StyledPanel)
        desc_layout = QVBoxLayout(desc_group)
        desc_layout.setContentsMargins(10, 10, 10, 10)
        desc_layout.setSpacing(4)

        self.desc_label = QLabel('Description:')
        desc_layout.addWidget(self.desc_label)

        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(150)
        self.desc_input.setPlaceholderText("Enter project description")
        if project and project.description:
            self.desc_input.setText(project.description)
        self.desc_input.textChanged.connect(self.update_desc_counter)
        desc_layout.addWidget(self.desc_input)

        self.desc_counter = QLabel()
        self.desc_counter.setAlignment(Qt.AlignRight)
        desc_layout.addWidget(self.desc_counter)

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

        self.update_name_counter()
        self.update_desc_counter()
        if self.is_edit_mode:
            self.validate_link()

    def update_name_counter(self):
        current_length = len(self.name_input.text())
        remaining = NAME_MAX_LENGTH - current_length
        self.name_counter.setText(f"{current_length}/{NAME_MAX_LENGTH} characters")

        if remaining <= 10:
            self.name_counter.setStyleSheet("color: #ff6b6b; font-size: 10px; font-weight: bold;")
        elif remaining <= 30:
            self.name_counter.setStyleSheet("color: #ffa726; font-size: 10px;")
        else:
            self.name_counter.setStyleSheet("color: #888; font-size: 10px;")

    def update_desc_counter(self):
        current_length = len(self.desc_input.toPlainText())
        remaining = DESCRIPTION_MAX_LENGTH - current_length
        self.desc_counter.setText(f"{current_length}/{DESCRIPTION_MAX_LENGTH} characters")

        if remaining <= 100:
            self.desc_counter.setStyleSheet("color: #ff6b6b; font-size: 10px; font-weight: bold;")
        elif remaining <= 300:
            self.desc_counter.setStyleSheet("color: #ffa726; font-size: 10px;")
        else:
            self.desc_counter.setStyleSheet("color: #888; font-size: 10px;")

    def validate_link(self):
        text = self.link_input.text().strip()

        if not text:
            self.link_status.setText("")
            self.link_status.setStyleSheet("font-size: 10px;")
            return

        if is_valid_link(text):
            self.link_status.setText("Valid link")
            self.link_status.setStyleSheet(
                "color: #2ecc71; font-size: 10px; font-weight: bold;"
            )
        else:
            self.link_status.setText("Invalid link (use a scheme, e.g. https://...)")
            self.link_status.setStyleSheet(
                "color: #e74c3c; font-size: 10px; font-weight: bold;"
            )

    def get_project_data(self) -> dict:
        data = {
            'name': self.name_input.text().strip(),
            'description': self.desc_input.toPlainText().strip() or None
        }
        if self.is_edit_mode:
            data['link'] = self.link_input.text().strip() or None
        return data

    def accept(self):
        data = self.get_project_data()

        if not data['name']:
            QMessageBox.warning(self, 'Error', 'Project name is required')
            return

        if len(data['name']) > NAME_MAX_LENGTH:
            QMessageBox.warning(
                self, 'Name Too Long',
                f'Project name cannot exceed {NAME_MAX_LENGTH} characters.\n'
                f'Current length: {len(data["name"])} characters.'
            )
            return

        if self.is_edit_mode:
            link = data.get('link')
            if link and not is_valid_link(link):
                QMessageBox.warning(
                    self, 'Invalid Link',
                    'Please enter a valid URL with scheme, for example:\n'
                    'https://github.com/user/repo\n'
                    'or leave the field empty.'
                )
                return

        super().accept()