from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QFrame
)
from PyQt5.QtCore import Qt


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
        header.setStyleSheet("QFrame { background-color: #1e2026; }")
        header.setFixedHeight(70)

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 15, 20, 15)

        title_label = QLabel("Help")
        title_label.setStyleSheet(
            "QLabel { color: #007acc; font-size: 20px; font-weight: bold; }"
        )
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)

        layout.addWidget(header)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background-color: #181a1e; border: none; }")

        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #181a1e;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(14)

        content_layout.addWidget(self._make_section(
            "WORKSPACE LAYOUT",
            """<ul style='color: #ddd; margin: 0; padding-left: 18px;'>
            <li>The window has five labeled panes: <b>PROJECTS</b>, <b>PROJECT</b>, <b>TASKS</b>, <b>TASK</b>, <b>SUBTASKS</b></li>
            <li>All splitter handles are draggable. Panes never collapse completely</li>
            <li>The <b>PROJECT</b> card stays on top, the <b>TASK</b> card and the <b>SUBTASKS</b> list are stacked below it</li>
            <li>The <b>TASKS</b> list sits on the left of the workspace and the selected task is shown on the right</li>
            <li>The global statistics panel is in the status bar at the bottom</li>
            </ul>"""
        ))

        content_layout.addWidget(self._make_section(
            "FIRST STEPS",
            """<ol style='color: #ddd; margin: 0; padding-left: 20px;'>
            <li>Click <b>+ New</b> in the <b>PROJECTS</b> pane or use <b>File -> New Project</b> (<code>Ctrl+N</code>).</li>
            <li>Select the new project in the list. The <b>PROJECT</b> card and the <b>TASKS</b> list update automatically.</li>
            <li>Click <b>+ Add</b> in the <b>TASKS</b> pane or use <b>File -> New Task</b> (<code>Ctrl+T</code>). Fill in title, description, priority and due date.</li>
            <li>Select the task. The <b>TASK</b> card and the <b>SUBTASKS</b> list update automatically.</li>
            <li>Click <b>+ Add</b> in the <b>SUBTASKS</b> pane or use <b>File -> New Subtask</b> (<code>Ctrl+Shift+T</code>). Fill in title and priority.</li>
            </ol>"""
        ))

        content_layout.addWidget(self._make_section(
            "PROJECTS",
            """<ul style='color: #ddd; margin: 0; padding-left: 18px;'>
            <li>Name up to 100 characters, description up to 2000 characters, both with live counters in the dialog.</li>
            <li>The optional link is only shown in edit mode. It is validated, a scheme such as <code>https://</code> is required.</li>
            <li>The project card shows the name, description, optional link, a status badge, and four tiles: <b>TASKS</b>, <b>SUBTASKS</b>, <b>UPDATED</b>, <b>PROGRESS</b>.</li>
            <li>Full CRUD: right-click in the list, <b>Edit -> Edit Project</b> (<code>Ctrl+E</code>), <b>Edit -> Delete Project</b> (<code>Ctrl+D</code>), or the <b>Edit</b> / <b>Delete</b> buttons on the card.</li>
            <li>When no project is selected, the card shows a placeholder, so the pane never looks empty.</li>
            </ul>"""
        ))

        content_layout.addWidget(self._make_section(
            "TASKS",
            """<ul style='color: #ddd; margin: 0; padding-left: 18px;'>
            <li>Title up to 100 characters, description up to 2000 characters, both with live counters in the dialog.</li>
            <li>Each row shows a status dot, the title, the priority, the progress and the due date.</li>
            <li>Task completion is manual: use the toggle button in the <b>TASK</b> card, or right-click in the list and choose <b>Mark as Complete</b> / <b>Mark as Pending</b>.</li>
            <li><b>Clear Completed (N)</b> removes all completed tasks from the current project. The count is shown on the button.</li>
            <li>Full CRUD: right-click in the list, <b>Edit -> Edit Task</b> (<code>Ctrl+Shift+E</code>), <b>Edit -> Delete Task</b> (<code>Ctrl+Shift+D</code>), or the buttons in the <b>TASK</b> card.</li>
            <li>If no task is selected, the <b>TASK</b> card shows a placeholder.</li>
            </ul>"""
        ))

        content_layout.addWidget(self._make_section(
            "SUBTASKS",
            """<ul style='color: #ddd; margin: 0; padding-left: 18px;'>
            <li>Subtasks are simplified: title and priority only.</li>
            <li>Title up to 100 characters, with a live counter in the dialog.</li>
            <li>Toggle completion with the checkbox on the row, or via the context menu.</li>
            <li>Subtask completion does not change the parent task status. The task must be completed manually.</li>
            <li>Full CRUD: right-click in the list, or <b>+ Add</b> in the <b>SUBTASKS</b> pane header.</li>
            </ul>"""
        ))

        content_layout.addWidget(self._make_section(
            "STABLE SELECTION",
            """<ul style='color: #ddd; margin: 0; padding-left: 18px;'>
            <li>Selection in all three lists is preserved across every CRUD operation.</li>
            <li>Select a project, select a task, create a subtask - project and task selection stay in place.</li>
            <li>Switch to another project and come back - the previously selected task is restored.</li>
            <li>Programmatic selection updates never emit change signals, and a single reload path restores everything consistently.</li>
            </ul>"""
        ))

        content_layout.addWidget(self._make_section(
            "EXPORT AND IMPORT",
            """<ul style='color: #ddd; margin: 0; padding-left: 18px;'>
            <li><b>File -> Export</b> (<code>Ctrl+Shift+S</code>) - writes the whole dataset to a single JSON file.</li>
            <li><b>File -> Import</b> (<code>Ctrl+I</code>) - replaces the current dataset with a JSON file. <b>This overwrites all existing data.</b> A temporary backup of the current file is created automatically before import and removed on success.</li>
            <li>Use Export before Import to keep a copy of your current data if you want to be extra safe.</li>
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
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+Shift+T</code></td><td>New subtask in the current task</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+E</code></td><td>Edit current project</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+D</code></td><td>Delete current project</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+Shift+E</code></td><td>Edit current task</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+Shift+D</code></td><td>Delete current task</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+I</code></td><td>Import</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+Shift+S</code></td><td>Export</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>F5</code></td><td>Refresh view</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>F1</code></td><td>Open help</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+/</code></td><td>Show keyboard shortcuts</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+A</code></td><td>Open about</td></tr>
            <tr><td style='padding: 3px 16px 3px 0;'><code>Ctrl+Q</code></td><td>Exit application</td></tr>
            </table>"""
        ))

        content_layout.addWidget(self._make_section(
            "DATA LOCATION",
            """<p style='color: #ddd; margin: 0;'>
            All data is stored locally:
            </p>
            <ul style='color: #ddd; margin: 6px 0 0 0; padding-left: 18px;'>
            <li>Projects, tasks, subtasks: <code>~/.smart_project_manager/projects.json</code></li>
            </ul>
            <p style='color: #ddd; margin: 8px 0 0 0;'>
            The uninstaller never touches your data. To remove it manually: <code>rm -rf ~/.smart_project_manager</code>
            </p>"""
        ))

        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        button_panel = QFrame()
        button_panel.setStyleSheet("QFrame { background-color: #1e2026; }")
        button_panel.setFixedHeight(60)

        button_layout = QHBoxLayout(button_panel)
        button_layout.setContentsMargins(20, 12, 20, 12)
        button_layout.addStretch()

        ok_button = QPushButton("Close")
        ok_button.setFixedSize(110, 36)
        ok_button.setCursor(Qt.PointingHandCursor)
        ok_button.setStyleSheet(
            "QPushButton { background-color: #007acc; color: white; font-weight: bold; "
            "border: none; border-radius: 5px; padding: 8px 16px; }"
            "QPushButton:hover { background-color: #0066b3; }"
            "QPushButton:pressed { background-color: #005a99; }"
        )
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        layout.addWidget(button_panel)

    def _make_section(self, title, html_content):
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: transparent; }")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            "QLabel { color: #007acc; font-size: 11px; font-weight: bold; letter-spacing: 1px; }"
        )
        frame_layout.addWidget(title_label)

        content_label = QLabel(html_content)
        content_label.setTextFormat(Qt.RichText)
        content_label.setWordWrap(True)
        content_label.setOpenExternalLinks(True)
        content_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        content_label.setStyleSheet(
            "QLabel { color: #ddd; font-size: 12px; }"
            "code { font-family: Consolas, monospace; background-color: #23262d; "
            "padding: 2px 6px; border-radius: 3px; color: #2ecc71; }"
            "a:hover { text-decoration: underline; }"
        )
        frame_layout.addWidget(content_label)

        return frame

    def center_dialog(self):
        if self.parent():
            x = self.parent().x() + (self.parent().width() - self.width()) // 2
            y = self.parent().y() + (self.parent().height() - self.height()) // 2
            self.move(x, y)
