# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QFrame
)
from PyQt5.QtCore import Qt

from smart_project_manager import __version__ as ver


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Smart Project Manager")
        self.setMinimumWidth(620)
        self.setMinimumHeight(560)
        self.setModal(True)

        self.setup_ui()
        self.center_dialog()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #1e2026;
            }
        """)
        header.setFixedHeight(110)

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 20, 20, 20)
        header_layout.setSpacing(4)

        title_label = QLabel("Smart Project Manager")
        title_label.setStyleSheet("""
            QLabel {
                color: #007acc;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)

        version_label = QLabel(f"Version {ver}")
        version_label.setStyleSheet("""
            QLabel {
                color: #5a5d65;
                font-size: 12px;
            }
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(version_label)

        subtitle_label = QLabel("Project and task management for developers and researchers")
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #aaa;
                font-size: 11px;
                font-style: italic;
            }
        """)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle_label)

        layout.addWidget(header)

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
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(14)

        content_layout.addWidget(self._make_section(
            "TAB-BASED WORKFLOW",
            """<ul style='color: #ddd; margin: 0; padding-left: 18px;'>
            <li>Each opened project gets its own tab on the right</li>
            <li>Double-click a task to open its subtasks in a nested tab</li>
            <li>Close tabs without deleting projects or tasks</li>
            <li>Multiple projects and multiple tasks open at once</li>
            </ul>"""
        ))

        content_layout.addWidget(self._make_section(
            "CORE FEATURES",
            """<ul style='color: #ddd; margin: 0; padding-left: 18px;'>
            <li>Projects with name and description</li>
            <li>Tasks with priority, due date and labels</li>
            <li>Subtasks with the same fields nested inside tasks</li>
            <li>Automatic progress tracking</li>
            <li>Search and filters by priority, label, status</li>
            <li>Drag and drop to reorder tasks</li>
            <li>Custom color labels</li>
            <li>Backups and JSON export/import</li>
            <li>Dark theme optimized for extended use</li>
            </ul>"""
        ))

        content_layout.addWidget(self._make_section(
            "DATA AND PRIVACY",
            """<p style='color: #ddd; margin: 0;'>
            All data stays on your machine. No cloud, no telemetry, no network access at runtime.
            Your projects are stored in <code style='color: #2ecc71; background-color: #23262d; padding: 2px 6px; border-radius: 3px;'>~/.smart_project_manager/projects.json</code>.
            Backups are managed automatically and never leave your device.
            </p>"""
        ))

        content_layout.addWidget(self._make_section(
            "LINKS",
            """<ul style='list-style: none; padding-left: 0; margin: 0;'>
            <li><a href="https://github.com/smartlegionlab/smart-project-manager" style="color: #007acc; text-decoration: none;">GitHub Repository</a></li>
            <li><a href="https://github.com/smartlegionlab/smart-project-manager/releases" style="color: #007acc; text-decoration: none;">Releases</a></li>
            <li><a href="https://github.com/smartlegionlab/smart-project-manager/blob/master/LICENSE" style="color: #007acc; text-decoration: none;">License (BSD 3-Clause)</a></li>
            <li><a href="https://github.com/smartlegionlab/smart-project-manager/blob/master/DISCLAIMER.md" style="color: #007acc; text-decoration: none;">Disclaimer</a></li>
            <li><a href="https://smartlegionlab.github.io/" style="color: #007acc; text-decoration: none;">Smart Legion Lab</a></li>
            </ul>"""
        ))

        content_layout.addStretch()

        copyright_label = QLabel("Copyright (c) 2026, Alexander Suvorov. All rights reserved.")
        copyright_label.setStyleSheet("""
            QLabel {
                color: #5a5d65;
                font-size: 10px;
            }
        """)
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(copyright_label)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        button_panel = QFrame()
        button_panel.setStyleSheet("""
            QFrame {
                background-color: #1e2026;
            }
        """)
        button_panel.setFixedHeight(60)

        button_layout = QHBoxLayout(button_panel)
        button_layout.setContentsMargins(20, 12, 20, 12)
        button_layout.addStretch()

        ok_button = QPushButton("Close")
        ok_button.setFixedSize(110, 36)
        ok_button.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0066b3;
            }
            QPushButton:pressed {
                background-color: #005a99;
            }
        """)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        layout.addWidget(button_panel)

    def _make_section(self, title, html_content):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
            }
        """)

        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: #007acc;
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 1px;
            }
        """)
        frame_layout.addWidget(title_label)

        content_label = QLabel(html_content)
        content_label.setTextFormat(Qt.TextFormat.RichText)
        content_label.setWordWrap(True)
        content_label.setOpenExternalLinks(True)
        content_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        content_label.setStyleSheet("""
            QLabel {
                color: #ddd;
                font-size: 12px;
            }
            code {
                font-family: Consolas, monospace;
            }
            a:hover {
                text-decoration: underline;
            }
        """)
        frame_layout.addWidget(content_label)

        return frame

    def center_dialog(self):
        if self.parent():
            x = self.parent().x() + (self.parent().width() - self.width()) // 2
            y = self.parent().y() + (self.parent().height() - self.height()) // 2
            self.move(x, y)
