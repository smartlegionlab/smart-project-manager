# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QDialog,
    QHBoxLayout, QMenu, QAction, QDesktopWidget, QStatusBar, QFileDialog,
    QMainWindow, QSplitter
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from smart_project_manager.core.managers.project_manager import ProjectManager
from smart_project_manager.ui.dialogs.label_manager_dialog import LabelManagerDialog
from smart_project_manager.ui.dialogs.project_dialog import ProjectDialog
from smart_project_manager.ui.dialogs.task_dialog import TaskDialog
from smart_project_manager.ui.dialogs.subtask_dialog import SubTaskDialog
from smart_project_manager.ui.widgets.project_progress_widget import ProjectProgressWidget
from smart_project_manager.ui.widgets.project_list_widget import ProjectListWidget
from smart_project_manager.ui.widgets.task_list_widget import TaskListWidget
from smart_project_manager.ui.widgets.subtask_list_widget import SubtaskListWidget
from smart_project_manager.ui.widgets.statistic_widget import StatisticsWidget
from smart_project_manager.ui.widgets.task_header_widget import TaskHeaderWidget
from smart_project_manager.ui.widgets.panel_header import PanelHeader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = ProjectManager()
        self.current_project_id: Optional[str] = None
        self.current_task_id: Optional[str] = None

        self._updating = False

        self.setWindowTitle('Smart Project Manager')
        self.setMinimumSize(1100, 700)
        self.resize(1300, 800)

        self.setup_application_icon()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #14171b;
            }
            QWidget {
                color: #ffffff;
                font-family: Arial;
            }
            QSplitter::handle {
                background-color: #14171b;
            }
            QSplitter::handle:horizontal {
                width: 8px;
            }
            QSplitter::handle:vertical {
                height: 8px;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setup_menu_bar()
        self.setup_ui()
        self.setup_status_bar()

        self._reload_preserving_selection()
        self.cleanup_old_backups_on_start()

        self.center_window()

    def setup_application_icon(self):
        project_root = Path(__file__).parent.parent
        icon_path = project_root / "data" / "icons" / "icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

    def create_desktop_entry(self):
        from smart_project_manager.ui.dialogs.desktop_entry_dialog import DesktopEntryDialog
        dialog = DesktopEntryDialog(self)
        dialog.exec_()

    def center_window(self):
        frame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())

    def setup_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')

        if sys.platform.startswith('linux'):
            desktop_entry_action = QAction('Create Desktop Entry...', self)
            desktop_entry_action.triggered.connect(self.create_desktop_entry)
            file_menu.addAction(desktop_entry_action)
            file_menu.addSeparator()

        new_project_action = QAction('New Project', self)
        new_project_action.setShortcut('Ctrl+N')
        new_project_action.triggered.connect(self.create_project)
        file_menu.addAction(new_project_action)

        new_task_action = QAction('New Task', self)
        new_task_action.setShortcut('Ctrl+T')
        new_task_action.triggered.connect(self.create_task_in_current_project)
        file_menu.addAction(new_task_action)

        new_subtask_action = QAction('New Subtask', self)
        new_subtask_action.setShortcut('Ctrl+Shift+T')
        new_subtask_action.triggered.connect(self.create_subtask_in_current_task)
        file_menu.addAction(new_subtask_action)

        file_menu.addSeparator()

        backup_action = QAction('Create Backup', self)
        backup_action.setShortcut('Ctrl+B')
        backup_action.triggered.connect(self.create_backup)
        file_menu.addAction(backup_action)

        backup_manager_action = QAction('Show Backups', self)
        backup_manager_action.triggered.connect(self.show_backup_manager)
        file_menu.addAction(backup_manager_action)

        file_menu.addSeparator()

        import_action = QAction('Import...', self)
        import_action.setShortcut('Ctrl+I')
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)

        export_action = QAction('Export...', self)
        export_action.setShortcut('Ctrl+Shift+S')
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu('Edit')

        edit_project_action = QAction('Edit Project', self)
        edit_project_action.setShortcut('Ctrl+E')
        edit_project_action.triggered.connect(self.edit_current_project)
        edit_menu.addAction(edit_project_action)

        delete_project_action = QAction('Delete Project', self)
        delete_project_action.setShortcut('Ctrl+D')
        delete_project_action.triggered.connect(self.delete_current_project)
        edit_menu.addAction(delete_project_action)

        edit_menu.addSeparator()

        edit_task_action = QAction('Edit Task', self)
        edit_task_action.setShortcut('Ctrl+Shift+E')
        edit_task_action.triggered.connect(self.edit_current_task)
        edit_menu.addAction(edit_task_action)

        delete_task_action = QAction('Delete Task', self)
        delete_task_action.setShortcut('Ctrl+Shift+D')
        delete_task_action.triggered.connect(self.delete_current_task)
        edit_menu.addAction(delete_task_action)

        edit_menu.addSeparator()

        labels_action = QAction('Manage Labels', self)
        labels_action.setShortcut('Ctrl+L')
        labels_action.triggered.connect(self.manage_labels)
        edit_menu.addAction(labels_action)

        view_menu = menubar.addMenu('View')

        refresh_action = QAction('Refresh', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_view)
        view_menu.addAction(refresh_action)

        help_menu = menubar.addMenu('Help')

        help_action = QAction('Help', self)
        help_action.setShortcut('F1')
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        shortcuts_action = QAction('Keyboard Shortcuts', self)
        shortcuts_action.setShortcut('Ctrl+/')
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)

        help_menu.addSeparator()

        about_action = QAction('About', self)
        about_action.setShortcut('Ctrl+A')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_ui(self):
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(0)

        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.setChildrenCollapsible(False)
        self.main_splitter.setHandleWidth(8)

        left_panel = self._build_left_panel()
        self.main_splitter.addWidget(left_panel)

        right_panel = self._build_right_panel()
        self.main_splitter.addWidget(right_panel)

        self.main_splitter.setStretchFactor(0, 0)
        self.main_splitter.setStretchFactor(1, 1)
        self.main_splitter.setSizes([320, 980])

        main_layout.addWidget(self.main_splitter)

    def _build_left_panel(self):
        panel = QWidget()
        panel.setMinimumWidth(240)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        header = PanelHeader("PROJECTS")
        layout.addWidget(header)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(4)

        self.btn_new_project = self._make_flat_button("+ New", "#2a8f5e", "#34a56e")
        self.btn_new_project.clicked.connect(self.create_project)
        buttons_layout.addWidget(self.btn_new_project)

        self.btn_edit_project = self._make_flat_button("Edit", "#3a3f48", "#4a505b")
        self.btn_edit_project.clicked.connect(self.edit_current_project)
        buttons_layout.addWidget(self.btn_edit_project)

        self.btn_delete_project = self._make_flat_button("Delete", "#3a3f48", "#4a505b")
        self.btn_delete_project.clicked.connect(self.delete_current_project)
        buttons_layout.addWidget(self.btn_delete_project)

        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        self.project_list = ProjectListWidget(self)
        self.project_list.project_selected.connect(self.on_project_selected)
        self.project_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_list.customContextMenuRequested.connect(self.show_project_context_menu)
        layout.addWidget(self.project_list, 1)

        return panel

    def _build_right_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 0, 0, 0)
        layout.setSpacing(8)

        project_header = PanelHeader("PROJECT")
        layout.addWidget(project_header)

        self.project_progress_widget = ProjectProgressWidget(self)
        self.project_progress_widget.btn_edit_project.clicked.connect(self.edit_current_project)
        self.project_progress_widget.btn_delete_project.clicked.connect(self.delete_current_project)
        self.project_progress_widget.setVisible(False)

        self.right_splitter = QSplitter(Qt.Vertical)
        self.right_splitter.setChildrenCollapsible(False)
        self.right_splitter.setHandleWidth(8)

        project_section = QWidget()
        project_section_layout = QVBoxLayout(project_section)
        project_section_layout.setContentsMargins(0, 0, 0, 0)
        project_section_layout.setSpacing(0)
        project_section_layout.addWidget(self.project_progress_widget)

        self.right_splitter.addWidget(project_section)

        bottom_splitter = QSplitter(Qt.Horizontal)
        bottom_splitter.setChildrenCollapsible(False)
        bottom_splitter.setHandleWidth(8)

        tasks_panel = QWidget()
        tasks_layout = QVBoxLayout(tasks_panel)
        tasks_layout.setContentsMargins(0, 0, 0, 0)
        tasks_layout.setSpacing(8)

        tasks_header_row = QHBoxLayout()
        tasks_header_row.setSpacing(6)
        tasks_header = PanelHeader("TASKS")
        tasks_header_row.addWidget(tasks_header, 1)

        self.btn_new_task = self._make_flat_button("+ Add", "#2a8f5e", "#34a56e")
        self.btn_new_task.clicked.connect(self.create_task_in_current_project)
        tasks_header_row.addWidget(self.btn_new_task)

        tasks_layout.addLayout(tasks_header_row)

        self.task_list = TaskListWidget(self)
        self.task_list.manager = self.manager
        self.task_list.task_selected.connect(self.on_task_selected)
        self.task_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.task_list.customContextMenuRequested.connect(self.show_task_context_menu)
        tasks_layout.addWidget(self.task_list, 1)

        bottom_splitter.addWidget(tasks_panel)

        subtasks_panel = QWidget()
        subtasks_layout = QVBoxLayout(subtasks_panel)
        subtasks_layout.setContentsMargins(0, 0, 0, 0)
        subtasks_layout.setSpacing(8)

        task_header_row = QHBoxLayout()
        task_header_row.setSpacing(6)
        task_header = PanelHeader("TASK")
        task_header_row.addWidget(task_header, 1)
        subtasks_layout.addLayout(task_header_row)

        self.task_header = TaskHeaderWidget(self)
        self.task_header.set_callbacks(
            self.toggle_task_status,
            self.edit_task_by_id,
            self.delete_task_by_id
        )
        subtasks_layout.addWidget(self.task_header)

        subtasks_header_row = QHBoxLayout()
        subtasks_header_row.setSpacing(6)
        subtasks_header = PanelHeader("SUBTASKS")
        subtasks_header_row.addWidget(subtasks_header, 1)

        self.btn_new_subtask = self._make_flat_button("+ Add", "#2a8f5e", "#34a56e")
        self.btn_new_subtask.clicked.connect(self.create_subtask_in_current_task)
        subtasks_header_row.addWidget(self.btn_new_subtask)

        subtasks_layout.addLayout(subtasks_header_row)

        self.subtask_list = SubtaskListWidget(self)
        self.subtask_list.manager = self.manager
        self.subtask_list.subtask_selected.connect(self.on_subtask_selected)
        self.subtask_list.subtask_toggled.connect(self.toggle_subtask_status)
        self.subtask_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.subtask_list.customContextMenuRequested.connect(self.show_subtask_context_menu)
        subtasks_layout.addWidget(self.subtask_list, 1)

        bottom_splitter.addWidget(subtasks_panel)

        bottom_splitter.setStretchFactor(0, 1)
        bottom_splitter.setStretchFactor(1, 1)
        bottom_splitter.setSizes([480, 480])

        self.right_splitter.addWidget(bottom_splitter)
        self.right_splitter.setStretchFactor(0, 0)
        self.right_splitter.setStretchFactor(1, 1)
        self.right_splitter.setSizes([230, 550])

        layout.addWidget(self.right_splitter, 1)

        return panel

    def _make_flat_button(self, text, bg, bg_hover):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFlat(True)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: #ffffff;
                font-weight: bold;
                font-size: 11px;
                padding: 5px 12px;
                border: none;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {bg_hover};
            }}
            QPushButton:pressed {{
                background-color: #23262c;
            }}
        """)
        return btn

    def setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #14171b;
                color: #7f8794;
                border-top: 1px solid #1f2227;
            }
        """)

        self.mini_stats = StatisticsWidget(self)
        self.status_bar.addPermanentWidget(self.mini_stats)

        self.status_bar.showMessage('Ready')

    def _save_selection(self):
        return self.current_project_id, self.current_task_id

    def _reload_preserving_selection(self, project_id=None, task_id=None):
        if self._updating:
            return

        self._updating = True

        if project_id is None:
            project_id = self.current_project_id
        if task_id is None:
            task_id = self.current_task_id

        projects = self.manager.get_all_projects()
        self.project_list.load_projects(projects, self.manager)

        project_exists = project_id and self.manager.get_project(project_id)
        if not project_exists and projects:
            project_id = projects[0].id
        elif not projects:
            project_id = None

        self.current_project_id = project_id
        self.current_task_id = task_id

        if project_id:
            self.project_progress_widget.setVisible(True)
            self.project_progress_widget.update_progress(
                self.manager.get_project(project_id), self.manager
            )

            self.project_list.set_current_id(project_id)

            tasks = self.manager.get_tasks_by_project(project_id)
            project = self.manager.get_project(project_id)
            if project and project.task_order:
                tasks_dict = {task.id: task for task in tasks}
                sorted_tasks = []
                for tid in project.task_order:
                    if tid in tasks_dict:
                        sorted_tasks.append(tasks_dict.pop(tid))
                sorted_tasks.extend(tasks_dict.values())
                tasks = sorted_tasks

            self.task_list.load_tasks(tasks)

            task_exists = task_id and self.manager.get_task(task_id) and \
                          self.manager.get_task(task_id).project_id == project_id

            if not task_exists and tasks:
                task_id = tasks[0].id
            elif not tasks:
                task_id = None

            self.current_task_id = task_id

            if task_id:
                self.task_list.set_current_id(task_id)
                task = self.manager.get_task(task_id)
                self.task_header.update_task(task, self.manager)

                subtasks = self.manager.get_subtasks_by_task(task_id)
                self.subtask_list.load_subtasks(subtasks)
            else:
                self.task_list.set_current_id(None)
                self.task_header.update_task(None, self.manager)
                self.subtask_list.load_subtasks([])
        else:
            self.project_progress_widget.setVisible(False)
            self.project_list.set_current_id(None)
            self.task_list.load_tasks([])
            self.task_header.update_task(None, self.manager)
            self.subtask_list.load_subtasks([])

        self.update_statistics()

        self._updating = False

    def on_project_selected(self, project_id: str):
        if self._updating:
            return
        self.current_project_id = project_id
        self.current_task_id = None
        self._reload_preserving_selection(project_id=project_id, task_id=None)

    def on_task_selected(self, task_id: str):
        if self._updating:
            return
        self.current_task_id = task_id
        task = self.manager.get_task(task_id)
        if not task:
            return

        self.task_header.update_task(task, self.manager)
        subtasks = self.manager.get_subtasks_by_task(task_id)
        self.subtask_list.load_subtasks(subtasks)

    def on_subtask_selected(self, subtask_id: str):
        pass

    def create_project(self):
        dialog = ProjectDialog(self, manager=self.manager)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_project_data()
            if not data['name']:
                QMessageBox.warning(self, 'Error', 'Project name is required')
                return

            project = self.manager.create_project(**data)
            self._reload_preserving_selection(project_id=project.id, task_id=None)

    def edit_current_project(self):
        if not self.current_project_id:
            self.status_bar.showMessage('No project selected', 2000)
            return

        project = self.manager.get_project(self.current_project_id)
        if not project:
            return

        dialog = ProjectDialog(self, project=project, manager=self.manager)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_project_data()
            if not data['name']:
                QMessageBox.warning(self, 'Error', 'Project name is required')
                return

            self.manager.update_project(project.id, **data)
            self._reload_preserving_selection(project_id=project.id)

    def delete_current_project(self):
        if not self.current_project_id:
            self.status_bar.showMessage('No project selected', 2000)
            return

        project = self.manager.get_project(self.current_project_id)
        if not project:
            return

        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f'Delete project "{project.name}" and all its tasks/subtasks?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.manager.delete_project(project.id)
            self._reload_preserving_selection(project_id=None, task_id=None)

    def show_project_context_menu(self, position):
        item = self.project_list.itemAt(position)
        menu = QMenu()

        if item:
            project_id = item.data(Qt.UserRole)
            if project_id:
                open_action = QAction("Open", self)
                open_action.triggered.connect(lambda: self.on_project_selected(project_id))
                menu.addAction(open_action)

                menu.addSeparator()

                edit_action = QAction("Edit Project", self)
                edit_action.triggered.connect(lambda: self.edit_project_by_id(project_id))
                menu.addAction(edit_action)

                delete_action = QAction("Delete Project", self)
                delete_action.triggered.connect(lambda: self.delete_project_by_id(project_id))
                menu.addAction(delete_action)

                menu.addSeparator()

        new_action = QAction("New Project", self)
        new_action.triggered.connect(self.create_project)
        menu.addAction(new_action)

        menu.exec_(self.project_list.viewport().mapToGlobal(position))

    def edit_project_by_id(self, project_id: str):
        if self.current_project_id != project_id:
            self.current_project_id = project_id
            self.current_task_id = None
            self._reload_preserving_selection(project_id=project_id, task_id=None)
        self.edit_current_project()

    def delete_project_by_id(self, project_id: str):
        if self.current_project_id != project_id:
            self.current_project_id = project_id
            self.current_task_id = None
            self._reload_preserving_selection(project_id=project_id, task_id=None)
        self.delete_current_project()

    def create_task_in_current_project(self):
        if not self.current_project_id:
            QMessageBox.warning(self, 'Error', 'Please select a project first')
            return

        dialog = TaskDialog(self, manager=self.manager, project_id=self.current_project_id)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_task_data()
            if not data['title']:
                QMessageBox.warning(self, 'Error', 'Task title is required')
                return

            task = self.manager.create_task(**data)
            self._reload_preserving_selection(
                project_id=self.current_project_id, task_id=task.id
            )

    def edit_current_task(self):
        if not self.current_task_id:
            self.status_bar.showMessage('No task selected', 2000)
            return
        self.edit_task_by_id(self.current_task_id)

    def delete_current_task(self):
        if not self.current_task_id:
            self.status_bar.showMessage('No task selected', 2000)
            return
        self.delete_task_by_id(self.current_task_id)

    def show_task_context_menu(self, position):
        item = self.task_list.itemAt(position)
        menu = QMenu()

        if item:
            task_id = item.data(Qt.UserRole)
            if task_id:
                task = self.manager.get_task(task_id)
                if task:
                    toggle_action = QAction(
                        "Mark as Pending" if task.completed else "Mark as Complete",
                        self
                    )
                    toggle_action.triggered.connect(lambda: self.toggle_task_status(task_id))
                    menu.addAction(toggle_action)

                    menu.addSeparator()

                    edit_action = QAction("Edit Task", self)
                    edit_action.triggered.connect(lambda: self.edit_task_by_id(task_id))
                    menu.addAction(edit_action)

                    delete_action = QAction("Delete Task", self)
                    delete_action.triggered.connect(lambda: self.delete_task_by_id(task_id))
                    menu.addAction(delete_action)

                    menu.addSeparator()

        new_action = QAction("New Task", self)
        new_action.triggered.connect(self.create_task_in_current_project)
        menu.addAction(new_action)

        menu.exec_(self.task_list.viewport().mapToGlobal(position))

    def toggle_task_status(self, task_id: str):
        task = self.manager.get_task(task_id)
        if not task:
            return

        task.toggle_complete()
        self.manager.update_task(task_id, completed=task.completed)

        self._reload_preserving_selection(
            project_id=self.current_project_id, task_id=task_id
        )

    def edit_task_by_id(self, task_id: str):
        task = self.manager.get_task(task_id)
        if not task:
            return

        dialog = TaskDialog(self, task=task, manager=self.manager)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_task_data()
            if not data['title']:
                QMessageBox.warning(self, 'Error', 'Task title is required')
                return

            self.manager.update_task(task.id, **data)
            self._reload_preserving_selection(
                project_id=self.current_project_id, task_id=task_id
            )

    def delete_task_by_id(self, task_id: str):
        task = self.manager.get_task(task_id)
        if not task:
            return

        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f'Delete task "{task.title}" and all its subtasks?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.manager.delete_task(task.id)
            self._reload_preserving_selection(
                project_id=self.current_project_id, task_id=None
            )

    def create_subtask_in_current_task(self):
        if not self.current_task_id:
            QMessageBox.warning(self, 'Error', 'Please select a task first')
            return

        task = self.manager.get_task(self.current_task_id)
        if not task:
            return

        dialog = SubTaskDialog(
            self,
            manager=self.manager,
            task_id=task.id,
            project_id=task.project_id
        )

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_subtask_data()
            if not data['title']:
                QMessageBox.warning(self, 'Error', 'Subtask title is required')
                return

            self.manager.create_subtask(**data)
            self._reload_preserving_selection(
                project_id=self.current_project_id, task_id=self.current_task_id
            )

    def show_subtask_context_menu(self, position):
        item = self.subtask_list.itemAt(position)
        menu = QMenu()

        if item:
            subtask_id = item.data(Qt.UserRole)
            if subtask_id:
                subtask = self.manager.get_subtask(subtask_id)
                if subtask:
                    toggle_action = QAction(
                        "Mark as Pending" if subtask.completed else "Mark as Complete",
                        self
                    )
                    toggle_action.triggered.connect(lambda: self.toggle_subtask_status(subtask_id))
                    menu.addAction(toggle_action)

                    menu.addSeparator()

                    edit_action = QAction("Edit Subtask", self)
                    edit_action.triggered.connect(lambda: self.edit_subtask_by_id(subtask_id))
                    menu.addAction(edit_action)

                    delete_action = QAction("Delete Subtask", self)
                    delete_action.triggered.connect(lambda: self.delete_subtask_by_id(subtask_id))
                    menu.addAction(delete_action)

                    menu.addSeparator()

        new_action = QAction("New Subtask", self)
        new_action.triggered.connect(self.create_subtask_in_current_task)
        menu.addAction(new_action)

        menu.exec_(self.subtask_list.viewport().mapToGlobal(position))

    def toggle_subtask_status(self, subtask_id: str):
        subtask = self.manager.get_subtask(subtask_id)
        if not subtask:
            return

        subtask.toggle_complete()
        self.manager.update_subtask(subtask_id, completed=subtask.completed)

        self._reload_preserving_selection(
            project_id=self.current_project_id, task_id=self.current_task_id
        )

    def edit_subtask_by_id(self, subtask_id: str):
        subtask = self.manager.get_subtask(subtask_id)
        if not subtask:
            return

        dialog = SubTaskDialog(self, subtask=subtask, manager=self.manager)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_subtask_data()
            if not data['title']:
                QMessageBox.warning(self, 'Error', 'Subtask title is required')
                return

            self.manager.update_subtask(subtask_id, **data)
            self._reload_preserving_selection(
                project_id=self.current_project_id, task_id=self.current_task_id
            )

    def delete_subtask_by_id(self, subtask_id: str):
        subtask = self.manager.get_subtask(subtask_id)
        if not subtask:
            return

        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f'Delete subtask "{subtask.title}"?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.manager.delete_subtask(subtask_id)
            self._reload_preserving_selection(
                project_id=self.current_project_id, task_id=self.current_task_id
            )

    def manage_labels(self):
        dialog = LabelManagerDialog(self, self.manager)
        dialog.exec_()
        self._reload_preserving_selection(
            project_id=self.current_project_id, task_id=self.current_task_id
        )

    def refresh_view(self):
        self.manager.load_data()
        self._reload_preserving_selection(
            project_id=self.current_project_id, task_id=self.current_task_id
        )
        self.status_bar.showMessage('View refreshed', 3000)

    def update_statistics(self):
        stats = self.manager.get_statistics()
        self.mini_stats.update_stats(stats)

    def import_data(self):
        home_dir = str(Path.home())
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Data", home_dir, "JSON Files (*.json);;All Files (*)"
        )
        if not file_path:
            return

        reply = QMessageBox.warning(
            self, "Import Data",
            "This will REPLACE all current data with imported data!\n\n"
            "Current data will be lost. Are you sure?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        try:
            result = self.manager.import_data(file_path)

            if not result.get('success'):
                QMessageBox.critical(
                    self, "Import Error",
                    f"Import failed:\n\n{result.get('error', 'Unknown error')}"
                )
                return

            self.manager.load_data()
            self.current_project_id = None
            self.current_task_id = None
            self._reload_preserving_selection(project_id=None, task_id=None)

            items = result.get('imported_items', {})
            message = "Import successful!\n\n"
            if items.get('projects', 0) > 0:
                message += f"Projects: {items.get('projects', 0)}\n"
            if items.get('tasks', 0) > 0:
                message += f"Tasks: {items.get('tasks', 0)}\n"
            if items.get('subtasks', 0) > 0:
                message += f"Subtasks: {items.get('subtasks', 0)}\n"
            if items.get('labels', 0) > 0:
                message += f"Labels: {items.get('labels', 0)}\n"
            QMessageBox.information(self, "Import Complete", message)

        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Import failed:\n\n{str(e)}")

    def export_data(self):
        home_dir = str(Path.home())
        default_file_name = os.path.join(
            home_dir,
            f"projects_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Data", default_file_name, "JSON Files (*.json);;All Files (*)"
        )
        if not file_path:
            return
        if not file_path.endswith('.json'):
            file_path += '.json'
        try:
            result = self.manager.export_data(file_path)
            if result['success']:
                message = (
                    f"Export successful!\n\n"
                    f"File: {result['export_path']}\n"
                    f"Size: {result['export_size'] / 1024:.1f} KB"
                )
                QMessageBox.information(self, "Export Complete", message)
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Export failed:\n\n{str(e)}")

    def create_backup(self):
        try:
            backup_path = self.manager.create_backup()
            QMessageBox.information(self, "Backup Created", f"Backup created successfully!\n\n{backup_path}")
        except FileNotFoundError:
            QMessageBox.warning(self, "No Data File", "Cannot create backup: No data file found.")
        except Exception as e:
            QMessageBox.critical(self, "Backup Error", f"Failed to create backup:\n\n{str(e)}")

    def cleanup_old_backups_on_start(self):
        try:
            self.manager.cleanup_old_backups(days_to_keep=30)
        except Exception as e:
            print(f"Backup cleanup error: {e}")

    def show_backup_manager(self):
        try:
            info = self.manager.get_backup_info()
            message = "Backup Manager\n\n"
            if info['total'] == 0:
                message += "No backups found."
            else:
                message += f"Total backups: {info['total']}\n"
                message += f"Total size: {info['total_size_mb']:.2f} MB\n\n"
                for backup in info['backups']:
                    message += f"- {backup['date']} ({backup['size_mb']:.1f} MB)\n"

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Backup Manager")
            msg_box.setText(message)
            msg_box.setIcon(QMessageBox.Information)
            clear_btn = msg_box.addButton("Clear All Backups", QMessageBox.ActionRole)
            close_btn = msg_box.addButton("Close", QMessageBox.RejectRole)
            msg_box.exec_()
            if msg_box.clickedButton() == clear_btn:
                self.clear_all_backups()
        except Exception as e:
            QMessageBox.warning(self, "Backup Error", f"Failed to show backup info: {str(e)}")

    def clear_all_backups(self):
        info = self.manager.get_backup_info()
        if info['total'] == 0:
            return
        reply = QMessageBox.warning(
            self, "Clear All Backups",
            f"Delete ALL {info['total']} backups?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.manager.clear_all_backups()

    def show_about(self):
        from smart_project_manager.ui.dialogs.about_dialog import AboutDialog
        dialog = AboutDialog(self)
        dialog.exec_()

    def show_help(self):
        from smart_project_manager.ui.dialogs.help_dialog import HelpDialog
        dialog = HelpDialog(self)
        dialog.exec_()

    def show_shortcuts(self):
        from smart_project_manager.ui.dialogs.shortcuts_dialog import ShortcutsDialog
        dialog = ShortcutsDialog(self)
        dialog.exec_()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Exit', 'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()