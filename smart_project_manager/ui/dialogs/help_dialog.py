# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help - Smart Project Manager")
        self.setMinimumWidth(650)
        self.setMinimumHeight(600)
        self.setModal(True)

        self.setup_ui()
        self.center_dialog()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        title_label = QLabel("<h2 style='color: #007acc;'>Smart Project Manager Help</h2>")
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

        help_label = QLabel(
            """<p style='color: #007acc; font-weight: bold;'>Getting Started:</p>
            <ol style='color: #ddd;'>
            <li>Create a project using <b>File → New Project</b> or the <b>+ New Project</b> button</li>
            <li>Click a project in the left panel to open it in a tab</li>
            <li>Add tasks to the project using <b>File → New Task</b> or the <b>+ Add Task</b> button</li>
            <li>Double-click a task to open its subtasks in a new tab below the task list</li>
            <li>Use labels to categorize tasks and subtasks</li>
            </ol>

            <p style='color: #007acc; font-weight: bold;'>Tab-Based Interface:</p>
            <ul style='color: #ddd;'>
            <li><b>Project tabs</b> (top right): each opened project gets its own tab</li>
            <li><b>Subtask tabs</b> (bottom right): each opened task gets its own subtask tab</li>
            <li>Close a project tab with the X button — the project stays in the left tree</li>
            <li>Close a subtask tab with the X button — the task stays in the task list</li>
            <li>Switch between multiple projects and multiple tasks freely</li>
            </ul>

            <p style='color: #007acc; font-weight: bold;'>Desktop Integration (Linux):</p>
            <ul style='color: #ddd;'>
            <li><b>File → Create Desktop Entry</b> — create an application shortcut in your system menu</li>
            <li>Choose between Application Menu (~/.local/share/applications/) and/or Desktop (~/Desktop/)</li>
            <li>After creation, you may need to log out and back in for the entry to appear</li>
            <li>Desktop shortcuts may show "Unsecured Application Launcher" — right-click → "Allow Launching" (one-time only)</li>
            </ul>

            <p style='color: #007acc; font-weight: bold;'>Keyboard Shortcuts:</p>
            <ul style='color: #ddd;'>
            <li>Ctrl+N: New Project</li>
            <li>Ctrl+T: New Task (in current project)</li>
            <li>Ctrl+B: Create Backup</li>
            <li>Ctrl+I: Import</li>
            <li>Ctrl+Shift+E: Export</li>
            <li>Ctrl+L: Manage Labels</li>
            <li>F5: Refresh View</li>
            <li>F1: Help</li>
            <li>Ctrl+Q: Exit</li>
            </ul>

            <p style='color: #007acc; font-weight: bold;'>Features:</p>
            <ul style='color: #ddd;'>
            <li>Projects have name, version, description, GitHub URL</li>
            <li>Tasks have title, description, priority, due date, and labels</li>
            <li>Subtasks inherit parent task properties and can have their own labels</li>
            <li>Automatic completion: when all subtasks are done, parent task is marked complete</li>
            <li>Progress bars show completion percentage</li>
            <li>Right-click tasks for quick actions</li>
            <li>Drag and drop tasks to reorder them</li>
            </ul>

            <p style='color: #007acc; font-weight: bold;'>Data:</p>
            <p style='color: #ddd;'>Data is automatically saved to <code style="color: #2ecc71;">~/.smart_project_manager/projects.json</code></p>
            <p style='color: #ddd;'>Backups are stored in <code style="color: #2ecc71;">~/.smart_project_manager/backups/</code> and cleaned up automatically after 30 days.</p>

            <hr style='border-color: #3a3d45;'>

            <p style='color: #999;'>GitHub: <a href="https://github.com/smartlegionlab/smart-project-manager/" style="color: #007acc;">Smart Project Manager</a></p>
            """
        )
        help_label.setTextFormat(Qt.RichText)
        help_label.setWordWrap(True)
        help_label.setOpenExternalLinks(True)
        help_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        help_label.setStyleSheet("""
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
            code {
                background-color: #23262d;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: Consolas, monospace;
            }
        """)

        content_layout.addWidget(help_label)
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