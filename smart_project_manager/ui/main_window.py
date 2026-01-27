import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QDialog,
    QHBoxLayout,
    QMenu,
    QAction,
    QDesktopWidget,
    QStatusBar,
    QFileDialog,
    QMainWindow
)
from PyQt5.QtGui import QFont, QDesktopServices
from PyQt5.QtCore import Qt, QUrl

from smart_project_manager.core.managers.project_manager import ProjectManager
from smart_project_manager.ui.dialogs.label_manager_dialog import LabelManagerDialog
from smart_project_manager.ui.dialogs.project_dialog import ProjectDialog
from smart_project_manager.ui.dialogs.task_detail_dialog import TaskDetailsDialog
from smart_project_manager.ui.dialogs.task_dialog import TaskDialog
from smart_project_manager.ui.widgets.project_progress_widget import ProjectProgressWidget
from smart_project_manager.ui.widgets.project_tree_widget import ProjectsTreeWidget
from smart_project_manager.ui.widgets.statistic_widget import StatisticsWidget
from smart_project_manager.ui.widgets.task_table_widget import TaskTableWidget

from smart_project_manager import __version__ as ver


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = ProjectManager()
        self.current_project_id: Optional[str] = None
        self.selected_project_item = None
        self.last_selected_project_id = None

        self.setWindowTitle(f'Smart Project Manager {ver}')
        self.showMaximized()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
            }
            QWidget {
                color: #ffffff;
                font-family: Arial;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.setup_menu_bar()
        self.setup_ui()
        self.setup_status_bar()

        self.load_projects()
        self.cleanup_old_backups_on_start()

        self.center_window()

    def center_window(self):
        frame = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())

    def setup_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')

        new_project_action = QAction('New Project', self)
        new_project_action.setShortcut('Ctrl+N')
        new_project_action.triggered.connect(self.create_project)
        file_menu.addAction(new_project_action)

        new_task_action = QAction('New Task', self)
        new_task_action.setShortcut('Ctrl+T')
        new_task_action.triggered.connect(self.create_task)
        file_menu.addAction(new_task_action)

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
        export_action.setShortcut('Ctrl+Shift+E')
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

        labels_action = QAction('Manage Labels', self)
        labels_action.setShortcut('Ctrl+L')
        labels_action.triggered.connect(self.manage_labels)
        edit_menu.addAction(labels_action)

        view_menu = menubar.addMenu('View')

        refresh_action = QAction('Refresh', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_view)
        view_menu.addAction(refresh_action)

        view_menu.addSeparator()

        show_completed_action = QAction('Show Completed Tasks', self)
        show_completed_action.setCheckable(True)
        show_completed_action.setChecked(True)
        show_completed_action.triggered.connect(self.toggle_show_completed)
        view_menu.addAction(show_completed_action)

        help_menu = menubar.addMenu('Help')

        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        help_action = QAction('Help', self)
        help_action.setShortcut('F1')
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

    def setup_ui(self):
        main_layout = QHBoxLayout(self.central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        left_panel = QWidget()
        left_panel.setMinimumWidth(320)
        left_panel.setMaximumWidth(400)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        projects_header = QLabel('📁 Projects')
        projects_header.setFont(QFont("Arial", 14, QFont.Bold))
        left_layout.addWidget(projects_header)

        project_buttons_layout = QHBoxLayout()
        project_buttons_layout.setSpacing(5)

        self.btn_new_project = QPushButton('+ New Project')
        self.btn_new_project.clicked.connect(self.create_project)
        self.btn_new_project.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                font-weight: bold;
                padding: 8px 12px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #1a72ca;
            }
        """)
        project_buttons_layout.addWidget(self.btn_new_project)

        left_layout.addLayout(project_buttons_layout)

        self.projects_tree = ProjectsTreeWidget(self)
        self.projects_tree.itemClicked.connect(self.on_project_selected)
        left_layout.addWidget(self.projects_tree, 1)

        self.statistics_widget = StatisticsWidget(self)
        left_layout.addWidget(self.statistics_widget)

        main_layout.addWidget(left_panel)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        tasks_header_layout = QHBoxLayout()

        self.tasks_header = QLabel('Select a project to view tasks')
        self.tasks_header.setFont(QFont("Arial", 14, QFont.Bold))
        tasks_header_layout.addWidget(self.tasks_header)

        tasks_header_layout.addStretch()

        self.btn_new_task = QPushButton('+ New Task')
        self.btn_new_task.clicked.connect(self.create_task)
        self.btn_new_task.setEnabled(False)
        self.btn_new_task.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: black;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        tasks_header_layout.addWidget(self.btn_new_task)

        self.btn_open_url = QPushButton('Open GitHub URL')
        self.btn_open_url.clicked.connect(self.open_github_url)
        self.btn_open_url.setEnabled(False)
        self.btn_open_url.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: black;
                        font-weight: bold;
                        padding: 8px 12px;
                        border-radius: 5px;
                        font-size: 12px;
                    }
                    QPushButton:hover:enabled {
                        background-color: #1976d2;
                    }
                    QPushButton:disabled {
                        background-color: #666;
                        color: #999;
                    }
                """)
        tasks_header_layout.addWidget(self.btn_open_url)

        self.btn_edit_project = QPushButton('Edit')
        self.btn_edit_project.clicked.connect(self.edit_current_project)
        self.btn_edit_project.setEnabled(False)
        self.btn_edit_project.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: black;
                font-weight: bold;
                padding: 8px 12px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover:enabled {
                background-color: #FFA000;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        tasks_header_layout.addWidget(self.btn_edit_project)

        self.btn_delete_project = QPushButton('Delete')
        self.btn_delete_project.clicked.connect(self.delete_current_project)
        self.btn_delete_project.setEnabled(False)
        self.btn_delete_project.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: black;
                font-weight: bold;
                padding: 8px 12px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover:enabled {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        tasks_header_layout.addWidget(self.btn_delete_project)

        right_layout.addLayout(tasks_header_layout)

        self.project_progress_widget = ProjectProgressWidget(self)
        right_layout.addWidget(self.project_progress_widget)

        self.tasks_table = TaskTableWidget(self)
        self.tasks_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tasks_table.customContextMenuRequested.connect(self.show_task_context_menu)
        self.tasks_table.itemDoubleClicked.connect(self.on_task_double_clicked)
        right_layout.addWidget(self.tasks_table, 3)

        main_layout.addWidget(right_panel, 1)

    def setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')

    def load_projects(self):
        if self.current_project_id:
            self.last_selected_project_id = self.current_project_id

        self.projects_tree.clear()

        projects = self.manager.get_all_projects()

        for project in projects:
            self.projects_tree.add_project(project, self.manager)

        if self.last_selected_project_id:
            for i in range(self.projects_tree.topLevelItemCount()):
                item = self.projects_tree.topLevelItem(i)
                if hasattr(item, 'project_id') and item.project_id == self.last_selected_project_id:
                    self.projects_tree.setCurrentItem(item)

                    self.current_project_id = self.last_selected_project_id
                    self.selected_project_item = item
                    self.btn_delete_project.setEnabled(True)
                    self.btn_edit_project.setEnabled(True)
                    self.btn_new_task.setEnabled(True)
                    break

        self.update_statistics()

    def on_project_selected(self, item, column):
        self.current_project_id = item.project_id
        self.selected_project_item = item
        self.btn_delete_project.setEnabled(True)
        self.btn_edit_project.setEnabled(True)
        self.btn_open_url.setEnabled(True)
        self.btn_new_task.setEnabled(True)

        self.last_selected_project_id = self.current_project_id

        project = self.manager.get_project(self.current_project_id)

        if project:
            self.tasks_header.setText(f'📋 Project: "{project.name}"')

            self.project_progress_widget.update_progress(project, self.manager)

            self.load_tasks_for_project(project.id)

    def load_tasks_for_project(self, project_id: str):
        self.tasks_table.setRowCount(0)

        tasks = self.manager.get_tasks_by_project(project_id)

        for row, task in enumerate(tasks):
            self.tasks_table.add_task_row(
                row, task, self.manager,
                self.toggle_task_status,
                self.edit_task,
                self.delete_task
            )

    def toggle_task_status(self, task_id: str):
        task = self.manager.get_task(task_id)
        if task:
            task.toggle_complete()
            self.manager.update_task(task_id, completed=task.completed)

            if self.current_project_id:
                self.load_tasks_for_project(self.current_project_id)
                self.update_statistics()

                self.load_projects()

                project = self.manager.get_project(self.current_project_id)
                if project:
                    self.project_progress_widget.update_progress(project, self.manager)

    def create_project(self):
        dialog = ProjectDialog(self, manager=self.manager)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_project_data()

            if not data['name']:
                QMessageBox.warning(self, 'Error', 'Project name is required')
                return

            project = self.manager.create_project(**data)
            self.load_projects()

            for i in range(self.projects_tree.topLevelItemCount()):
                item = self.projects_tree.topLevelItem(i)
                if item.project_id == project.id:
                    self.projects_tree.setCurrentItem(item)
                    self.on_project_selected(item, 0)
                    break

            QMessageBox.information(self, 'Success', f'Project "{project.name}" created')

    def open_github_url(self):
        if not self.current_project_id:
            QMessageBox.warning(self, 'Error', 'No project selected')
            return

        project = self.manager.get_project(self.current_project_id)
        if not project:
            QMessageBox.warning(self, 'Error', 'Project not found')
            return

        if not project.github_url:
            QMessageBox.warning(self, 'Error', 'No GitHub URL specified for this project')
            return

        try:
            url = project.github_url.strip()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            QDesktopServices.openUrl(QUrl(url))
        except Exception as e:
            QMessageBox.critical(
                self,
                'Error',
                f'Failed to open URL:\n{str(e)}\n\nURL: {project.github_url}'
            )

    def edit_current_project(self):
        if not self.current_project_id:
            QMessageBox.warning(self, 'Error', 'No project selected')
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
            self.load_projects()

            if self.current_project_id == project.id:
                self.load_tasks_for_project(project.id)

    def delete_current_project(self):
        if not self.current_project_id:
            QMessageBox.warning(self, 'Error', 'No project selected')
            return

        project = self.manager.get_project(self.current_project_id)
        if not project:
            return

        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            f'Delete project "{project.name}" and all its tasks/subtasks?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.manager.delete_project(project.id)

            self.last_selected_project_id = None

            self.current_project_id = None
            self.selected_project_item = None
            self.btn_delete_project.setEnabled(False)
            self.btn_new_task.setEnabled(False)
            self.tasks_header.setText('Select a project to view tasks')
            self.tasks_table.setRowCount(0)

            self.project_progress_widget.setVisible(False)

            self.load_projects()

    def create_task(self):
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

            self.load_tasks_for_project(self.current_project_id)
            self.update_statistics()

            self.load_projects()

            project = self.manager.get_project(self.current_project_id)
            if project:
                self.project_progress_widget.update_progress(project, self.manager)

            QMessageBox.information(self, 'Success', f'Task "{task.title}" created')

    def edit_task(self, task_id: str):
        task = self.manager.get_task(task_id)
        if not task:
            return

        self.tasks_table.save_selection()

        dialog = TaskDialog(self, task=task, manager=self.manager)
        dialog.task_updated.connect(self.on_task_updated)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_task_data()

            if not data['title']:
                QMessageBox.warning(self, 'Error', 'Task title is required')
                return

            self.manager.update_task(task.id, **data)

            if self.current_project_id:
                self.load_tasks_for_project(self.current_project_id)
                self.update_statistics()

                self.load_projects()

                project = self.manager.get_project(self.current_project_id)
                if project:
                    self.project_progress_widget.update_progress(project, self.manager)

            self.tasks_table.restore_selection()

    def on_task_updated(self):
        if self.current_project_id:
            self.tasks_table.save_selection()
            self.load_tasks_for_project(self.current_project_id)
            self.update_statistics()

            self.load_projects()

            project = self.manager.get_project(self.current_project_id)
            if project:
                self.project_progress_widget.update_progress(project, self.manager)

            self.tasks_table.restore_selection()

    def delete_task(self, task_id: str):
        task = self.manager.get_task(task_id)
        if not task:
            return

        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            f'Delete task "{task.title}" and all its subtasks?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.manager.delete_task(task_id)

            if self.current_project_id:
                self.load_tasks_for_project(self.current_project_id)
                self.update_statistics()

                self.load_projects()

                project = self.manager.get_project(self.current_project_id)
                if project:
                    self.project_progress_widget.update_progress(project, self.manager)

    def manage_labels(self):
        dialog = LabelManagerDialog(self, self.manager)
        dialog.exec_()
        self.update_statistics()

    def show_task_context_menu(self, position):
        row = self.tasks_table.rowAt(position.y())

        if row < 0:
            return

        self.tasks_table.selectRow(row)

        task_id = self.get_task_id_from_row(row)

        if task_id:
            self.show_task_menu(task_id, self.tasks_table.viewport().mapToGlobal(position))

    def get_task_id_from_row(self, row: int) -> Optional[str]:
        if not self.current_project_id:
            return None

        tasks = self.manager.get_tasks_by_project(self.current_project_id)
        if row < len(tasks):
            return tasks[row].id

        return None

    def show_task_menu(self, task_id: str, position):
        task = self.manager.get_task(task_id)
        if not task:
            return

        menu = QMenu()

        view_action = QAction("👁 View Details")
        view_action.triggered.connect(lambda: self.view_task(task_id))
        menu.addAction(view_action)

        mark_action = QAction("✅ Mark as Complete" if not task.completed else "⏳ Mark as Pending")
        mark_action.triggered.connect(lambda: self.toggle_task_status(task_id))
        menu.addAction(mark_action)

        menu.addSeparator()

        edit_action = QAction("✏️ Edit Task")
        edit_action.triggered.connect(lambda: self.edit_task(task_id))
        menu.addAction(edit_action)

        menu.addSeparator()

        delete_action = QAction("🗑️ Delete Task")
        delete_action.triggered.connect(lambda: self.delete_task(task_id))
        menu.addAction(delete_action)

        menu.exec_(position)

    def view_task(self, task_id: str):
        task = self.manager.get_task(task_id)
        if not task:
            return

        dialog = TaskDetailsDialog(self, task=task, manager=self.manager)
        dialog.exec_()

    def on_task_double_clicked(self, item):
        row = item.row()
        column = item.column()

        if column in [2, 6, 7]:
            return

        task_id = self.get_task_id_from_row(row)
        if task_id:
            self.view_task(task_id)

    def refresh_view(self):
        self.load_projects()
        if self.current_project_id:
            self.load_tasks_for_project(self.current_project_id)
            project = self.manager.get_project(self.current_project_id)
            if project:
                self.project_progress_widget.update_progress(project, self.manager)

        self.status_bar.showMessage('View refreshed', 3000)

    def toggle_show_completed(self, show: bool):
        self.refresh_view()

    def update_statistics(self):
        stats = self.manager.get_statistics()
        self.statistics_widget.update_stats(stats)

    def import_data(self):
        home_dir = str(Path.home())
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Data",
            home_dir,
            "JSON Files (*.json);;All Files (*)"
        )

        if not file_path:
            return

        reply = QMessageBox.warning(
            self,
            "Import Data",
            "⚠️ This will REPLACE all current data with imported data!\n\n"
            "Current data will be lost. Are you sure?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        try:
            result = self.manager.import_data(file_path)

            if result['success']:
                self.manager.load_data()

                self.current_project_id = None
                self.selected_project_item = None
                self.btn_delete_project.setEnabled(False)
                self.btn_edit_project.setEnabled(False)
                self.btn_new_task.setEnabled(False)
                self.tasks_header.setText('Select a project to view tasks')
                self.tasks_table.setRowCount(0)
                self.project_progress_widget.setVisible(False)

                self.load_projects()
                self.update_statistics()

                items = result.get('imported_items', {})
                message = f"✅ Import successful!\n\n"

                if items.get('projects', 0) > 0:
                    message += f"📁 Projects: {items.get('projects', 0)}\n"
                if items.get('tasks', 0) > 0:
                    message += f"✅ Tasks: {items.get('tasks', 0)}\n"
                if items.get('subtasks', 0) > 0:
                    message += f"📝 Subtasks: {items.get('subtasks', 0)}\n"
                if items.get('labels', 0) > 0:
                    message += f"🏷️ Labels: {items.get('labels', 0)}\n"

                QMessageBox.information(self, "Import Complete", message)
                self.status_bar.showMessage('Data imported successfully', 3000)
            else:
                QMessageBox.warning(
                    self,
                    "Import Failed",
                    f"Failed to import: {result.get('error', 'Unknown error')}\n\n"
                    f"Original data has been restored."
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Import Error",
                f"Import failed:\n\n{str(e)}"
            )

    def export_data(self):
        home_dir = str(Path.home())

        default_file_name = os.path.join(
            home_dir,
            f"projects_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Data",
            default_file_name,
            "JSON Files (*.json);;All Files (*)"
        )

        if not file_path:
            return

        if not file_path.endswith('.json'):
            file_path += '.json'

        try:
            result = self.manager.export_data(file_path)

            if result['success']:
                message = (
                    f"✅ Export successful!\n\n"
                    f"File: {result['export_path']}\n"
                    f"Size: {result['export_size'] / 1024:.1f} KB"
                )

                QMessageBox.information(self, "Export Complete", message)
                self.status_bar.showMessage('Data exported successfully', 3000)
            else:
                QMessageBox.warning(
                    self,
                    "Export Failed",
                    f"Failed to export: {result.get('error', 'Unknown error')}"
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Error",
                f"Export failed:\n\n{str(e)}"
            )

    def create_backup(self):
        try:
            backup_path = self.manager.create_backup()

            QMessageBox.information(
                self,
                "Backup Created",
                f"✅ Backup created successfully!\n\n{backup_path}"
            )

            self.status_bar.showMessage(f'Backup created', 3000)

        except FileNotFoundError as e:
            QMessageBox.warning(
                self,
                "No Data File",
                f"Cannot create backup: No data file found.\n"
                f"Please create at least one project first."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Backup Error",
                f"Failed to create backup:\n\n{str(e)}"
            )

    def cleanup_old_backups_on_start(self):
        try:
            stats = self.manager.cleanup_old_backups(days_to_keep=30)

            if stats['deleted'] > 0:
                print(f"Cleaned up {stats['deleted']} old backups")

        except Exception as e:
            print(f"Backup cleanup error: {e}")

    def show_backup_manager(self):
        try:
            info = self.manager.get_backup_info()

            message = "📂 Backup Manager\n\n"

            if info['total'] == 0:
                message += "No backups found."
            else:
                message += f"Total backups: {info['total']}\n"
                message += f"Total size: {info['total_size_mb']:.2f} MB\n\n"

                if info['total'] > 10:
                    message += f"Showing last 10 of {info['total']} backups:\n\n"
                else:
                    message += "All backups:\n\n"

                for backup in info['backups']:
                    message += f"• {backup['date']} ({backup['size_mb']:.1f} MB)\n"

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Backup Manager")
            msg_box.setText(message)
            msg_box.setIcon(QMessageBox.Information)

            clear_btn = msg_box.addButton("Clear All Backups", QMessageBox.ActionRole)

            if info['total'] == 0:
                clear_btn.setEnabled(False)
                clear_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #666;
                        color: #999;
                        font-weight: bold;
                        padding: 5px 10px;
                    }
                """)
            else:
                clear_btn.setEnabled(True)
                clear_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        font-weight: bold;
                        padding: 5px 10px;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                    QPushButton:disabled {
                        background-color: #666;
                        color: #999;
                    }
                """)

            msg_box.addButton("Close", QMessageBox.RejectRole)

            msg_box.exec_()

            if msg_box.clickedButton() == clear_btn and clear_btn.isEnabled():
                self.clear_all_backups()

        except Exception as e:
            QMessageBox.warning(
                self,
                "Backup Error",
                f"Failed to show backup info: {str(e)}"
            )

    def clear_all_backups(self):
        info = self.manager.get_backup_info()

        if info['total'] == 0:
            QMessageBox.information(
                self,
                "No Backups",
                "No backup files found to delete"
            )
            return

        reply = QMessageBox.warning(
            self,
            "Clear All Backups",
            f"⚠️ Are you sure you want to delete ALL {info['total']} backups?\n"
            f"Total size: {info['total_size_mb']:.2f} MB\n\n"
            "This action cannot be undone!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        try:
            result = self.manager.clear_all_backups()

            if result.get('success', True):
                QMessageBox.information(
                    self,
                    "Backups Cleared",
                    f"✅ Cleared {result.get('deleted', 0)} backup files\n"
                    f"Freed {result.get('total_size_mb', 0):.2f} MB"
                )
                self.status_bar.showMessage(f'Cleared {result.get("deleted", 0)} backups', 3000)
            else:
                QMessageBox.warning(
                    self,
                    "Clear Failed",
                    f"Failed to clear backups: {result.get('error', 'Unknown error')}"
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Clear Error",
                f"Failed to clear backups:\n\n{str(e)}"
            )

    def show_about(self):
        QMessageBox.about(
            self,
            "About Smart Project Manager",
            f"""<h2>Smart Project Manager {ver}</h2>
            <p>A powerful project and task management tool for developers and researchers.</p>
            <p><b>Features:</b></p>
            <ul>
            <li>Manage unlimited projects with versions</li>
            <li>Create tasks with priorities and due dates</li>
            <li>Add subtasks to tasks</li>
            <li>Label system</li>
            <li>Automatic progress tracking</li>
            <li>Dark theme interface</li>
            </ul>
            <p><b>Copyright © 2025, <a href="https://github.com/smartlegionlab/">Alexander Suvorov</a>. All rights reserved.</b></p>
            """
        )

    def show_help(self):
        QMessageBox.information(
            self,
            "Help - Smart Project Manager",
            """<h3>Smart Project Manager Help</h3>
            <p><b>Getting Started:</b></p>
            <ol>
            <li>Create a project using File → New Project or the New Project button</li>
            <li>Select a project from the left panel</li>
            <li>Add tasks to the project using File → New Task or the New Task button</li>
            <li>Add subtasks by editing a task and going to the Subtasks tab</li>
            <li>Use labels to categorize tasks and subtasks</li>
            </ol>
            <p><b>Keyboard Shortcuts:</b></p>
            <ul>
            <li>Ctrl+N: New Project</li>
            <li>Ctrl+T: New Task</li>
            <li>Ctrl+B: Create BackUp</li>
            <li>Ctrl+I: Import</li>
            <li>Ctrl+Shift+E: Export</li>
            <li>Ctrl+E: Edit Project</li>
            <li>Ctrl+D: Delete Project</li>
            <li>Ctrl+L: Manage Labels</li>
            <li>F5: Refresh View</li>
            <li>F1: Help</li>
            <li>Ctrl+Q: Exit</li>
            </ul>
            <p><b>Features:</b></p>
            <ul>
            <li>Projects have name, version, description</li>
            <li>Tasks have title, description, priority, due date, and labels</li>
            <li>Subtasks inherit parent task properties and can have their own labels</li>
            <li>Automatic completion: When all subtasks are done, parent task is marked complete</li>
            <li>Progress bars show completion percentage</li>
            <li>Right-click tasks for quick actions</li>
            </ul>
            <p>Data is automatically saved to ~/.project_manager/projects.json</p>
            <hr>
            <p>Github: <a href="https://github.com/smartlegionlab/smart-project-manager/">Smart Project Manager</a></p>
            """
        )

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            'Exit',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
