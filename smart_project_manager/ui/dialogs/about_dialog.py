# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from smart_project_manager import __version__ as ver


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Smart Project Manager")
        self.setMinimumWidth(550)
        self.setMinimumHeight(500)
        self.setModal(True)

        self.setup_ui()
        self.center_dialog()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        title_label = QLabel(f"<h2 style='color: #007acc;'>Smart Project Manager {ver}</h2>")
        title_label.setTextFormat(Qt.RichText)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #181a1e;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: #2a2d34;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4a4d55;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #5a5d65;
            }
        """)

        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #181a1e;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)

        about_label = QLabel(
            """<p style='text-align: center; color: #ddd;'>
            A powerful project and task management tool for developers and researchers.
            </p>

            <p style='color: #007acc; font-weight: bold;'>Features:</p>
            <ul style='color: #ddd;'>
            <li>Manage unlimited projects with versions</li>
            <li>Create tasks with priorities and due dates</li>
            <li>Add subtasks to tasks</li>
            <li>Label system</li>
            <li>Automatic progress tracking</li>
            <li>Dark theme interface</li>
            <li>Tab-based interface with project tabs</li>
            <li>Nested subtask tabs per task</li>
            <li>Linux desktop integration (Application Menu / Desktop shortcuts)</li>
            </ul>

            <p style='text-align: center; margin-top: 20px; color: #007acc; font-weight: bold;'>Links:</p>
            <ul style='list-style: none; padding-left: 0; text-align: center;'>
            <li><a href="https://github.com/smartlegionlab/smart-project-manager" style="color: #007acc;">GitHub Repository</a></li>
            <li><a href="https://github.com/smartlegionlab/smart-project-manager/blob/master/LICENSE" style="color: #007acc;">License (BSD 3-Clause)</a></li>
            <li><a href="https://github.com/smartlegionlab/smart-project-manager/blob/master/DISCLAIMER.md" style="color: #007acc;">Disclaimer</a></li>
            <li><a href="https://github.com/smartlegionlab/smart-project-manager/releases" style="color: #007acc;">Releases</a></li>
            </ul>

            <p style='text-align: center; margin-top: 20px; color: #999;'>
            <b>Copyright © 2026, <a href="https://smartlegionlab.github.io/" style="color: #007acc;">Smart Legion Lab</a>. All rights reserved.</b>
            </p>
            """
        )
        about_label.setTextFormat(Qt.RichText)
        about_label.setWordWrap(True)
        about_label.setOpenExternalLinks(True)
        about_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        about_label.setStyleSheet("""
            QLabel {
                background-color: #1e2026;
                padding: 15px;
                border-radius: 5px;
                color: #ddd;
            }
            a {
                color: #007acc;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        """)

        content_layout.addWidget(about_label)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        ok_button = QPushButton("OK")
        ok_button.setMinimumWidth(100)
        ok_button.setMinimumHeight(35)
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0066b3;
            }
        """)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

    def center_dialog(self):
        if self.parent():
            x = self.parent().x() + (self.parent().width() - self.width()) // 2
            y = self.parent().y() + (self.parent().height() - self.height()) // 2
            self.move(x, y)
