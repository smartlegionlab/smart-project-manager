# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QColorDialog,
    QTextEdit,
    QWidget,
    QGridLayout,
    QFrame,
)
from PyQt5.QtGui import QColor

from smart_project_manager.models.label import Label
from smart_project_manager.ui.widgets.label_widget import LabelWidget


class LabelDialog(QDialog):

    def __init__(self, parent=None, label: Label = None):
        super().__init__(parent)
        self.is_edit_mode = label is not None
        self.label = label

        self.setWindowTitle('Edit Label' if self.is_edit_mode else 'Create New Label')
        self.setMinimumWidth(450)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)

        name_group = QFrame()
        name_group.setFrameStyle(QFrame.StyledPanel)
        name_layout = QVBoxLayout(name_group)
        name_layout.setContentsMargins(15, 15, 15, 15)

        self.name_label = QLabel('Label Name:')
        self.name_label.setStyleSheet("font-weight: bold;")
        name_layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter label name")
        if label:
            self.name_input.setText(label.name)
        name_layout.addWidget(self.name_input)

        self.layout.addWidget(name_group)

        color_group = QFrame()
        color_group.setFrameStyle(QFrame.StyledPanel)
        color_layout = QGridLayout(color_group)
        color_layout.setContentsMargins(15, 15, 15, 15)

        self.color_label = QLabel('Color:')
        self.color_label.setStyleSheet("font-weight: bold;")
        color_layout.addWidget(self.color_label, 0, 0)

        self.color_button = QPushButton()
        self.color_button.setFixedSize(50, 50)
        self.color_button.clicked.connect(self.choose_color)
        if label:
            self.current_color = QColor(label.color)
        else:
            self.current_color = QColor("#3498db")
        self.update_color_button()
        color_layout.addWidget(self.color_button, 0, 1)

        self.preview_label = QLabel("Preview:")
        self.preview_label.setStyleSheet("font-weight: bold;")
        color_layout.addWidget(self.preview_label, 1, 0)

        self.preview_container = QWidget()
        preview_container_layout = QHBoxLayout(self.preview_container)
        preview_container_layout.setContentsMargins(0, 0, 0, 0)

        self.preview_widget = LabelWidget(
            label.name if label else "Preview Label",
            self.current_color.name(),
            self
        )
        self.preview_widget.setMinimumHeight(35)
        preview_container_layout.addWidget(self.preview_widget)
        preview_container_layout.addStretch()

        color_layout.addWidget(self.preview_container, 1, 1)

        color_layout.setColumnStretch(2, 1)
        self.layout.addWidget(color_group)

        desc_group = QFrame()
        desc_group.setFrameStyle(QFrame.StyledPanel)
        desc_layout = QVBoxLayout(desc_group)
        desc_layout.setContentsMargins(15, 15, 15, 15)

        self.desc_label = QLabel('Description (optional):')
        self.desc_label.setStyleSheet("font-weight: bold;")
        desc_layout.addWidget(self.desc_label)

        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(80)
        self.desc_input.setPlaceholderText("Enter label description")
        if label and label.description:
            self.desc_input.setText(label.description)
        desc_layout.addWidget(self.desc_input)

        self.layout.addWidget(desc_group)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setFixedSize(100, 35)
        button_layout.addWidget(self.cancel_button)

        button_layout.addStretch()

        button_text = 'Update Label' if self.is_edit_mode else 'Create Label'
        self.submit_button = QPushButton(button_text)
        self.submit_button.setDefault(True)
        self.submit_button.setFixedSize(150, 35)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1a72ca;
            }
        """)
        self.submit_button.clicked.connect(self.accept)
        button_layout.addWidget(self.submit_button)

        self.layout.addLayout(button_layout)

        self.name_input.textChanged.connect(self.update_preview)

    def choose_color(self):
        color = QColorDialog.getColor(self.current_color, self)
        if color.isValid():
            self.current_color = color
            self.update_color_button()
            self.update_preview()

    def update_color_button(self):
        self.color_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.current_color.name()};
                border: 2px solid #444;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                border: 2px solid #666;
                background-color: {self.adjust_color_brightness(self.current_color.name(), 0.1)};
            }}
        """)

    def adjust_color_brightness(self, color_hex: str, factor: float) -> str:
        color = QColor(color_hex)
        h, s, v, a = color.getHsv()
        v = min(255, int(v * (1 + factor)))
        return QColor.fromHsv(h, s, v, a).name()

    def update_preview(self):
        name = self.name_input.text() or "Preview Label"
        self.preview_widget.set_label(name, self.current_color.name())

    def get_label_data(self) -> dict:
        return {
            'name': self.name_input.text().strip(),
            'color': self.current_color.name(),
            'description': self.desc_input.toPlainText().strip() or None
        }
