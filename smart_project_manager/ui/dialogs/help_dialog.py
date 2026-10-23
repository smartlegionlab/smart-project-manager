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
        self.setMinimumWidth(720)
        self.setMinimumHeight(680)
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

        title_label = QLabel("Help")
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
            "FIRST STEPS",
            """<ol style='color: #ddd; margin: 0; padding-left: 20px;'>
            <li>Click <b>+ New Project</b> in the left panel or use <b>File -> New Project</b>. Enter a name and optional description.</li>
            <li>Click the new project in the tree on the left. It opens as a tab on the right.</li>
            <li>Click <b>Add Task</b> inside the project tab or use <b>File -> New Task</b>. Fill in title, priority, due date and labels.</li>
            <li>Double-click the task row. Its subtasks open as a new tab below the task list.</li>
            <li>Inside the subtask tab click <b>+ Add Subtask</b> to add nested steps for this task.</li>
            </ol>"""
        ))

        content_layout.addWidget(self._make_section(
            "TABS AND NAVIGATION",
            """<ul style='color: #ddd; margin: 0; padding-left: 18px;'>
            <li><b>Project tabs</b> - one tab per opened project, at the top of the right panel.</li>
            <li><b>Subtask tabs</b> - one tab per opened task, below the task list inside the project tab.</li>
            <li>Click a tab to switch. Close any tab with the <b>X</b> button.</li>
            <li>Closing a project tab does not delete the project. It stays in the tree on the left and can be reopened by clicking it again.</li>
            <li>Closing a subtask tab does not delete the task. It stays in the task list and can be reopened by double-clicking the task row again.</li>
            <li>You can keep multiple project tabs open, and multiple subtask tabs inside each project tab.</li>
            </ul>"""
        ))

        content_layout.addWidget(self._make_section(
            "TASKS AND SUBTASKS",
            """<ul style='color: #ddd; margin: 0; padding-left: 18px;'>
            <li>Each task and subtask has: title, description, priority (High / Medium / Low), due date, labels.</li>
            <li>Status toggle: click the status button on the row, or use right-click -> <b>Mark as Complete</b> / <b>Mark as Pending</b>.</li>
            <li>Automatic completion: when every subtask of a task is completed, the parent task is marked completed automatically.</li>
            <li>Reorder tasks: drag a task row up or down inside the task table. The new order is saved per project.</li>
            <li>Right-click a task row for quick actions: <b>View Details</b>, <b>Open Subtasks</b>, <b>Mark as Complete / Pending</b>, <b>Edit Task</b>, <b>Delete Task</b>.</li>
            </ul>"""
        ))

        content_layout.addWidget(self._make_section(
            "SEARCH AND FILTERS",
            """<ul style='color: #ddd; margin: 0; padding-left: 18px;'>
            <li><b>Search box</b> - filters tasks by title and description in the current project.</li>
            <li><b>Priority filter</b> - show only tasks with a specific priority.</li>
            <li><b>Label filter</b> - show only tasks that have a specific label.</li>
            <li><b>Show Completed</b> - hide or show completed tasks.</li>
            <li><b>Reset</b> - clear all filters and return to the full task list.</li>
            </ul>"""
        ))

        content_layout.addWidget(self._make_section(
            "LABELS",
            """<ul style='color: #ddd; margin: 0; padding-left: 18px;'>
            <li>Open <b>Edit -> Manage Labels</b> to create, edit and delete labels.</li>
            <li>Each label has a name (up to 8 characters), background color and text color.</li>
            <li>Assign labels to tasks and subtasks while creating or editing them.</li>
            <li>Deleting a label removes it from all tasks and subtasks that use it.</li>
            </ul>"""
        ))

        content_layout.addWidget(self._make_section(
            "BACKUPS, EXPORT, IMPORT",
            """<ul style='color: #ddd; margin: 0; padding-left: 18px;'>
            <li><b>File -> Create Backup</b> (<code>Ctrl+B</code>) - saves a timestamped copy of your data to <code>~/.smart_project_manager/backups/</code>.</li>
            <li><b>File -> Show Backups</b> - lists current backups, shows total size and lets you clear all backups at once.</li>
            <li>Backups older than 30 days are removed automatically at startup.</li>
            <li><b>File -> Export</b> (<code>Ctrl+Shift+E</code>) - writes the whole dataset to a single JSON file.</li>
            <li><b>File -> Import</b> (<code>Ctrl+I</code>) - replaces the current dataset with the contents of a JSON file. <b>This overwrites all existing data.</b> A temporary backup of the current file is created automatically before import.</li>
            </ul>"""
        ))

        content_layout.addWidget(self._make_section(
            "DESKTOP INTEGRATION (LINUX)",
            """<ul style='color: #ddd; margin: 0; padding-left: 18px;'>
            <li><b>File -> Create Desktop Entry</b> - creates a launcher in the application menu and/or on the desktop.</li>
            <li>Choose the application menu (<code>~/.local/share/applications/</code>) and/or the desktop (<code>~/Desktop/</code>).</li>
            <li>After creation you may need to log out and back in for the menu entry to appear.</li>
            <li>The desktop launcher may show "Unsecured Application Launcher" on first launch. Right-click -> <b>Allow Launching</b> (one-time).</li>
            </ul>"""
        ))

        content_layout.addWidget(self._make_section(
            "KEYBOARD SHORTCUTS",
            """<table style='color: #ddd; font-size: 12px; border-collapse: collapse;'>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+N</code></td><td>New project</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+T</code></td><td>New task in the current project</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+B</code></td><td>Create backup</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+I</code></td><td>Import</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+Shift+E</code></td><td>Export</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+L</code></td><td>Manage labels</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>F5</code></td><td>Refresh view</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>F1</code></td><td>Open help</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+Q</code></td><td>Exit application</td></tr>
            </table>"""
        ))

        content_layout.addWidget(self._make_section(
            "DATA LOCATION",
            """<p style='color: #ddd; margin: 0;'>
            All data is stored locally:
            </p>
            <ul style='color: #ddd; margin: 6px 0 0 0; padding-left: 18px;'>
            <li>Projects, tasks, subtasks, labels: <code>~/.smart_project_manager/projects.json</code></li>
            <li>Backups: <code>~/.smart_project_manager/backups/</code></li>
            </ul>
            <p style='color: #ddd; margin: 8px 0 0 0;'>
            The uninstaller never touches your data. To remove it manually: <code>rm -rf ~/.smart_project_manager</code>
            </p>"""
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
        content_label.setTextFormat(Qt.RichText)
        content_label.setWordWrap(True)
        content_label.setOpenExternalLinks(True)
        content_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        content_label.setStyleSheet("""
            QLabel {
                color: #ddd;
                font-size: 12px;
            }
            code {
                font-family: Consolas, monospace;
                background-color: #23262d;
                padding: 2px 6px;
                border-radius: 3px;
                color: #2ecc71;
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
