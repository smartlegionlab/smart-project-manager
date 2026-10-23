# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ShortcutsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Keyboard Shortcuts - Smart Project Manager")
        self.setMinimumWidth(600)
        self.setMinimumHeight(620)
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
        header.setFixedHeight(70)

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)

        title_label = QLabel("Keyboard Shortcuts")
        title_label.setStyleSheet("""
            QLabel {
                color: #007acc;
                font-size: 20px;
                font-weight: bold;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)

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
            "PROJECTS",
            [
                ("Ctrl+N", "New project"),
                ("Ctrl+E", "Edit current project (from tab)"),
                ("Ctrl+D", "Delete current project (from tab)"),
                ("Ctrl+B", "Create backup"),
                ("Ctrl+I", "Import data"),
                ("Ctrl+Shift+E", "Export data"),
                ("Ctrl+L", "Manage labels"),
            ]
        ))

        content_layout.addWidget(self._make_section(
            "TASKS",
            [
                ("Ctrl+T", "New task in current project"),
            ]
        ))

        content_layout.addWidget(self._make_section(
            "VIEW",
            [
                ("F5", "Refresh view"),
                ("Ctrl+F", "Focus search box"),
                ("Ctrl+/", "Show this dialog"),
            ]
        ))

        content_layout.addWidget(self._make_section(
            "HELP",
            [
                ("F1", "Open help"),
                ("Ctrl+A", "Open about"),
            ]
        ))

        content_layout.addWidget(self._make_section(
            "APPLICATION",
            [
                ("Ctrl+Q", "Exit application"),
            ]
        ))

        content_layout.addStretch()

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
        ok_button.setCursor(Qt.PointingHandCursor)
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

    def _make_section(self, title, items):
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

        for key, description in items:
            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 2, 0, 2)
            row_layout.setSpacing(20)

            key_label = QLabel(key)
            key_label.setFixedWidth(140)
            key_label.setStyleSheet("""
                QLabel {
                    color: #2ecc71;
                    font-family: Consolas, monospace;
                    font-size: 12px;
                    font-weight: bold;
                }
            """)
            row_layout.addWidget(key_label)

            desc_label = QLabel(description)
            desc_label.setStyleSheet("""
                QLabel {
                    color: #ddd;
                    font-size: 12px;
                }
            """)
            row_layout.addWidget(desc_label, 1)

            frame_layout.addWidget(row)

        return frame

    def center_dialog(self):
        if self.parent():
            x = self.parent().x() + (self.parent().width() - self.width()) // 2
            y = self.parent().y() + (self.parent().height() - self.height()) // 2
            self.move(x, y)
