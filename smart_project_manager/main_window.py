# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QDialog,
    QHBoxLayout, QMenu, QAction, QDesktopWidget, QStatusBar, QFileDialog,
    QMainWindow, QLineEdit, QComboBox, QCheckBox, QFrame, QTextBrowser,
    QScrollArea, QSizePolicy, QTableWidget, QTabWidget, QSplitter,
    QTabBar
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

from smart_project_manager.core.managers.project_manager import ProjectManager
from smart_project_manager.ui.dialogs.label_manager_dialog import LabelManagerDialog
from smart_project_manager.ui.dialogs.project_dialog import ProjectDialog
from smart_project_manager.ui.dialogs.task_detail_dialog import TaskDetailsDialog
from smart_project_manager.ui.dialogs.task_dialog import TaskDialog
from smart_project_manager.ui.widgets.project_progress_widget import ProjectProgressWidget
from smart_project_manager.ui.widgets.project_tree_widget import ProjectsTreeWidget
from smart_project_manager.ui.widgets.statistic_widget import StatisticsWidget
from smart_project_manager.ui.widgets.task_table_widget import TaskTableWidget
from smart_project_manager.ui.widgets.subtask_panel_widget import SubtaskPanelWidget

from smart_project_manager import __version__ as ver


class ProjectTab(QWidget):
    def __init__(self, parent, project_id: str):
        super().__init__(parent)
        self.main_window = parent
        self.project_id = project_id
        self.selected_task_id: Optional[str] = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        top_bar_layout = QHBoxLayout()

        self.tasks_header = QLabel('Tasks')
        self.tasks_header.setFont(QFont("Arial", 14, QFont.Bold))
        top_bar_layout.addWidget(self.tasks_header)

        top_bar_layout.addStretch()

        self.btn_edit_project = QPushButton('Edit')
        self.btn_edit_project.clicked.connect(self.edit_project)
        self.btn_edit_project.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: black;
                font-weight: bold;
                padding: 6px 10px;
                border-radius: 5px;
                font-size: 11px;
            }
            QPushButton:hover:enabled {
                background-color: #FFA000;
            }
            QPushButton:disabled {
                background-color: #5a5d65;
                color: #999;
            }
        """)
        top_bar_layout.addWidget(self.btn_edit_project)

        self.btn_delete_project = QPushButton('Delete')
        self.btn_delete_project.clicked.connect(self.delete_project)
        self.btn_delete_project.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: black;
                font-weight: bold;
                padding: 6px 10px;
                border-radius: 5px;
                font-size: 11px;
            }
            QPushButton:hover:enabled {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #5a5d65;
                color: #999;
            }
        """)
        top_bar_layout.addWidget(self.btn_delete_project)

        layout.addLayout(top_bar_layout)

        self.project_progress_widget = ProjectProgressWidget(self)
        layout.addWidget(self.project_progress_widget)

        self.filters_panel = QFrame()
        self.filters_panel.setStyleSheet("""
            QFrame {
                background-color: #2a2d34;
                border-radius: 5px;
                padding: 8px;
            }
        """)

        filters_layout = QHBoxLayout(self.filters_panel)
        filters_layout.setContentsMargins(8, 5, 8, 5)
        filters_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tasks...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self.on_search_changed)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #1e2026;
                border: 1px solid #4a4d55;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
                min-width: 150px;
            }
            QLineEdit:focus {
                border: 1px solid #007acc;
            }
        """)
        filters_layout.addWidget(self.search_input)

        priority_label = QLabel("Priority:")
        priority_label.setStyleSheet("font-size: 11px; color: #aaa;")
        filters_layout.addWidget(priority_label)

        self.priority_filter_combo = QComboBox()
        self.priority_filter_combo.addItems(["All", "Low", "Medium", "High"])
        self.priority_filter_combo.currentTextChanged.connect(self.on_priority_filter_changed)
        self.priority_filter_combo.setStyleSheet("""
            QComboBox {
                background-color: #1e2026;
                border: 1px solid #4a4d55;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
                min-width: 80px;
            }
            QComboBox:hover {
                border: 1px solid #5a5d65;
            }
        """)
        filters_layout.addWidget(self.priority_filter_combo)

        label_label = QLabel("Label:")
        label_label.setStyleSheet("font-size: 11px; color: #aaa;")
        filters_layout.addWidget(label_label)

        self.label_filter_combo = QComboBox()
        self.label_filter_combo.addItem("All")
        self.label_filter_combo.currentTextChanged.connect(self.on_label_filter_changed)
        self.label_filter_combo.setStyleSheet("""
            QComboBox {
                background-color: #1e2026;
                border: 1px solid #4a4d55;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
                min-width: 100px;
            }
            QComboBox:hover {
                border: 1px solid #5a5d65;
            }
        """)
        filters_layout.addWidget(self.label_filter_combo)

        self.show_completed_checkbox = QCheckBox("Show Completed")
        self.show_completed_checkbox.setChecked(True)
        self.show_completed_checkbox.stateChanged.connect(self.on_show_completed_changed)
        self.show_completed_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 11px;
                color: #aaa;
                spacing: 5px;
            }
        """)
        filters_layout.addWidget(self.show_completed_checkbox)

        self.btn_reset_filters = QPushButton("Reset")
        self.btn_reset_filters.clicked.connect(self.reset_filters)
        self.btn_reset_filters.setStyleSheet("""
            QPushButton {
                background-color: #4a4d55;
                color: white;
                font-weight: bold;
                padding: 4px 10px;
                border-radius: 4px;
                font-size: 11px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #5a5d65;
            }
        """)
        filters_layout.addWidget(self.btn_reset_filters)

        filters_layout.addStretch()
        layout.addWidget(self.filters_panel)

        tasks_header_layout = QHBoxLayout()

        self.btn_new_task = QPushButton('Add Task')
        self.btn_new_task.clicked.connect(self.create_task)
        self.btn_new_task.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: black;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 5px;
                font-size: 12px;
                min-width: 90px;
            }
            QPushButton:hover:enabled {
                background-color: #219653;
            }
            QPushButton:disabled {
                background-color: #5a5d65;
                color: #999;
            }
        """)
        tasks_header_layout.addWidget(self.btn_new_task)

        self.btn_clear_completed = QPushButton('Clear Completed (0)')
        self.btn_clear_completed.clicked.connect(self.clear_completed_tasks)
        self.btn_clear_completed.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: black;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 5px;
                font-size: 12px;
                min-width: 140px;
            }
            QPushButton:hover:enabled {
                background-color: #d68910;
            }
            QPushButton:disabled {
                background-color: #5a5d65;
                color: #999;
            }
        """)
        tasks_header_layout.addWidget(self.btn_clear_completed)

        tasks_header_layout.addStretch()
        layout.addLayout(tasks_header_layout)

        self.tasks_table = TaskTableWidget(self)
        self.tasks_table.manager = self.main_window.manager
        self.tasks_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tasks_table.customContextMenuRequested.connect(self.show_task_context_menu)
        self.tasks_table.task_double_clicked.connect(self.on_task_double_clicked)
        self.tasks_table.task_dropped.connect(self.on_task_dropped)
        self.tasks_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tasks_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tasks_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tasks_table.setFrameStyle(QTableWidget.NoFrame)

        layout.addWidget(self.tasks_table, 1)

        self.subtasks_tab_widget = QTabWidget()
        self.subtasks_tab_widget.setTabsClosable(False)
        self.subtasks_tab_widget.setMovable(False)
        self.subtasks_tab_widget.tabCloseRequested.connect(self.close_subtask_tab)
        self.subtasks_tab_widget.setMaximumHeight(320)
        self.subtasks_tab_widget.setMinimumHeight(0)
        self.subtasks_tab_widget.setStyleSheet("""
            QTabWidget::pane {
                background-color: #23262d;
                border-top: 2px solid #3a3d45;
            }
            QTabBar::tab {
                background-color: #2a2d34;
                color: #aaa;
                padding: 6px 12px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #23262d;
                color: white;
                border-bottom: 2px solid #007acc;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3a3d45;
            }
        """)
        self.subtasks_tab_widget.hide()
        layout.addWidget(self.subtasks_tab_widget)

        self._subtask_tabs: Dict[str, SubtaskPanelWidget] = {}

        self.search_text = ""
        self.priority_filter = "All"
        self.label_filter = "All"
        self.show_completed = True

        self.load_project_data()

    def load_project_data(self):
        project = self.main_window.manager.get_project(self.project_id)
        if not project:
            return

        self.project_progress_widget.update_progress(project, self.main_window.manager)

        self.update_clear_completed_button()
        self.update_label_filter_combo()
        self.apply_filters()

    def update_label_filter_combo(self):
        current_text = self.label_filter_combo.currentText()
        self.label_filter_combo.blockSignals(True)
        self.label_filter_combo.clear()
        self.label_filter_combo.addItem("All")

        labels = self.main_window.manager.get_all_labels()
        for label in labels:
            self.label_filter_combo.addItem(label.name)

        if current_text and current_text != "All":
            index = self.label_filter_combo.findText(current_text)
            if index >= 0:
                self.label_filter_combo.setCurrentIndex(index)
            else:
                self.label_filter_combo.setCurrentIndex(0)
                self.label_filter = "All"
        else:
            self.label_filter_combo.setCurrentIndex(0)
            self.label_filter = "All"
        self.label_filter_combo.blockSignals(False)

    def update_clear_completed_button(self):
        tasks = self.main_window.manager.get_tasks_by_project(self.project_id)
        completed_count = sum(1 for task in tasks if task.completed)
        self.btn_clear_completed.setText(f'Clear Completed ({completed_count})')
        self.btn_clear_completed.setEnabled(completed_count > 0)

    def on_search_changed(self, text):
        self.search_text = text.strip().lower()
        self.apply_filters()

    def on_priority_filter_changed(self, priority):
        self.priority_filter = priority
        self.apply_filters()

    def on_label_filter_changed(self, label):
        self.label_filter = label
        self.apply_filters()

    def on_show_completed_changed(self, state):
        self.show_completed = (state == Qt.Checked)
        self.apply_filters()

    def reset_filters(self):
        self.search_input.clear()
        self.priority_filter_combo.setCurrentIndex(0)
        self.label_filter_combo.setCurrentIndex(0)
        self.show_completed_checkbox.setChecked(True)

        self.search_text = ""
        self.priority_filter = "All"
        self.label_filter = "All"
        self.show_completed = True

        self.apply_filters()
        self.main_window.status_bar.showMessage('Filters reset', 2000)

    def apply_filters(self):
        selected_task_id = None
        selected_items = self.tasks_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            item = self.tasks_table.item(row, 1)
            if item:
                selected_task_id = item.data(Qt.UserRole)

        scroll_pos = self.tasks_table.verticalScrollBar().value()

        all_tasks = self.main_window.manager.get_tasks_by_project(self.project_id)
        project = self.main_window.manager.get_project(self.project_id)

        filtered_tasks = []
        PRIORITY_MAP = {"Low": 3, "Medium": 2, "High": 1}
        all_labels = self.main_window.manager.get_all_labels()
        label_name_to_id = {label.name: label.id for label in all_labels}

        for task in all_tasks:
            search_ok = True
            if self.search_text:
                search_in_title = self.search_text in task.title.lower()
                search_in_desc = task.description and self.search_text in task.description.lower()
                search_ok = search_in_title or search_in_desc

            priority_ok = True
            if self.priority_filter != "All":
                expected_priority = PRIORITY_MAP.get(self.priority_filter)
                if expected_priority is not None:
                    priority_ok = (task.priority == expected_priority)

            label_ok = True
            if self.label_filter != "All":
                label_id = label_name_to_id.get(self.label_filter)
                if label_id:
                    label_ok = (label_id in task.labels)
                else:
                    label_ok = False

            completed_ok = True
            if not self.show_completed:
                completed_ok = not task.completed

            if search_ok and priority_ok and label_ok and completed_ok:
                filtered_tasks.append(task)

        if project and project.task_order:
            tasks_dict = {task.id: task for task in filtered_tasks}
            sorted_tasks = []
            for task_id in project.task_order:
                if task_id in tasks_dict:
                    sorted_tasks.append(tasks_dict.pop(task_id))
            sorted_tasks.extend(tasks_dict.values())
            filtered_tasks = sorted_tasks

        self.display_filtered_tasks(filtered_tasks)

        if selected_task_id:
            for row in range(self.tasks_table.rowCount()):
                item = self.tasks_table.item(row, 1)
                if item and item.data(Qt.UserRole) == selected_task_id:
                    self.tasks_table.selectRow(row)
                    break

        self.tasks_table.verticalScrollBar().setValue(scroll_pos)

        filtered_count = len(filtered_tasks)
        total_count = len(all_tasks)
        if filtered_count == total_count:
            self.main_window.status_bar.showMessage(f'Showing all {total_count} tasks', 2000)
        else:
            self.main_window.status_bar.showMessage(f'Showing {filtered_count} of {total_count} tasks', 2000)

    def display_filtered_tasks(self, tasks):
        self.tasks_table.setRowCount(0)
        for row, task in enumerate(tasks):
            self.tasks_table.add_task_row(
                row, task, self.main_window.manager,
                self.toggle_task_status,
                self.edit_task,
                self.delete_task
            )
            item = self.tasks_table.item(row, 2)
            if item:
                item.setData(Qt.UserRole, task.id)

    def toggle_task_status(self, task_id: str):
        task = self.main_window.manager.get_task(task_id)
        scroll_pos = self.tasks_table.verticalScrollBar().value()
        current_row = self.get_task_row(task_id)

        if task:
            task.toggle_complete()
            self.main_window.manager.update_task(task_id, completed=task.completed)

            if task.completed and self.selected_task_id == task_id:
                self.close_subtask_tab_by_task(task_id)
                self.selected_task_id = None

            self.apply_filters()
            self.main_window.update_statistics()
            self.main_window.update_projects_tree_counts()
            self.load_project_data()

        self.update_clear_completed_button()
        self.tasks_table.verticalScrollBar().setValue(scroll_pos)
        if 0 <= current_row < self.tasks_table.rowCount():
            self.tasks_table.selectRow(current_row)

    def get_task_row(self, task_id: str) -> int:
        for row in range(self.tasks_table.rowCount()):
            item = self.tasks_table.item(row, 1)
            if item and item.data(Qt.UserRole) == task_id:
                return row
        return -1

    def create_task(self):
        dialog = TaskDialog(self, manager=self.main_window.manager, project_id=self.project_id)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_task_data()
            if not data['title']:
                QMessageBox.warning(self, 'Error', 'Task title is required')
                return

            self.main_window.manager.create_task(**data)
            self.apply_filters()
            self.main_window.update_statistics()
            self.main_window.update_projects_tree_counts()
            self.load_project_data()
            self.update_label_filter_combo()

    def edit_task(self, task_id: str):
        task = self.main_window.manager.get_task(task_id)
        if not task:
            return

        dialog = TaskDialog(self, task=task, manager=self.main_window.manager)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_task_data()
            if not data['title']:
                QMessageBox.warning(self, 'Error', 'Task title is required')
                return

            self.main_window.manager.update_task(task.id, **data)
            self.apply_filters()
            self.main_window.update_statistics()
            self.main_window.update_projects_tree_counts()
            self.load_project_data()
            self.update_label_filter_combo()

    def delete_task(self, task_id: str):
        task = self.main_window.manager.get_task(task_id)
        if not task:
            return

        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f'Delete task "{task.title}" and all its subtasks?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.selected_task_id == task_id:
                self.close_subtask_tab_by_task(task_id)
                self.selected_task_id = None

            self.main_window.manager.delete_task(task_id)
            self.apply_filters()
            self.main_window.update_statistics()
            self.main_window.update_projects_tree_counts()
            self.load_project_data()
            self.update_label_filter_combo()

    def on_task_dropped(self, from_row, to_row):
        new_order = self.tasks_table.get_task_order()
        project = self.main_window.manager.get_project(self.project_id)
        if not project:
            return
        project.task_order = new_order
        self.main_window.manager.update_project(project.id, task_order=new_order)
        self.main_window.status_bar.showMessage('Task order saved', 2000)

    def on_task_double_clicked(self, task_id):
        if not task_id:
            return
        task = self.main_window.manager.get_task(task_id)
        if not task:
            return

        if task_id in self._subtask_tabs:
            index = self.subtasks_tab_widget.indexOf(self._subtask_tabs[task_id])
            if index >= 0:
                self.subtasks_tab_widget.setCurrentIndex(index)
                self.subtasks_tab_widget.show()
                return

        subtask_widget = SubtaskPanelWidget(self, manager=self.main_window.manager)
        subtask_widget.subtask_updated.connect(self.on_subtask_updated)
        subtask_widget.panel_closed.connect(lambda: None)
        subtask_widget.show_for_task(task, self.project_id)

        subtask_widget.btn_close.hide()
        subtask_widget.title_label.hide()

        index = self.subtasks_tab_widget.addTab(subtask_widget, task.title)

        close_btn = QPushButton('✕')
        close_btn.setFixedSize(20, 20)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #e74c3c;
                border: none;
                font-size: 12px;
                font-weight: 900;
            }
            QPushButton:hover {
                background-color: #e74c3c;
                color: #ffffff;
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: #a93226;
                color: #ffffff;
                border-radius: 10px;
            }
        """)
        close_btn.clicked.connect(lambda _, w=subtask_widget: self.close_subtask_tab_by_widget(w))
        self.subtasks_tab_widget.tabBar().setTabButton(index, QTabBar.RightSide, close_btn)

        self._subtask_tabs[task_id] = subtask_widget
        self.subtasks_tab_widget.setCurrentWidget(subtask_widget)
        self.subtasks_tab_widget.show()
        self.selected_task_id = task_id

    def close_subtask_tab(self, index):
        widget = self.subtasks_tab_widget.widget(index)
        task_id_to_remove = None
        for tid, w in self._subtask_tabs.items():
            if w == widget:
                task_id_to_remove = tid
                break

        if task_id_to_remove:
            del self._subtask_tabs[task_id_to_remove]
            if self.selected_task_id == task_id_to_remove:
                self.selected_task_id = None

        self.subtasks_tab_widget.removeTab(index)
        widget.deleteLater()

        if self.subtasks_tab_widget.count() == 0:
            self.subtasks_tab_widget.hide()

    def close_subtask_tab_by_task(self, task_id: str):
        if task_id in self._subtask_tabs:
            widget = self._subtask_tabs[task_id]
            index = self.subtasks_tab_widget.indexOf(widget)
            if index >= 0:
                self.close_subtask_tab(index)

    def close_subtask_tab_by_widget(self, widget):
        index = self.subtasks_tab_widget.indexOf(widget)
        if index >= 0:
            self.close_subtask_tab(index)

    def on_subtask_updated(self):
        self.load_project_data()
        self.main_window.update_statistics()
        self.main_window.update_projects_tree_counts()

    def show_task_context_menu(self, position):
        row = self.tasks_table.rowAt(position.y())
        if row < 0:
            return

        self.tasks_table.selectRow(row)
        item = self.tasks_table.item(row, 2)
        if not item:
            return
        task_id = item.data(Qt.UserRole)
        if not task_id:
            return

        task = self.main_window.manager.get_task(task_id)
        if not task:
            return

        menu = QMenu()

        view_action = QAction("View Details", self)
        view_action.triggered.connect(lambda: self.view_task(task_id))
        menu.addAction(view_action)

        open_subtasks_action = QAction("Open Subtasks", self)
        open_subtasks_action.triggered.connect(lambda: self.on_task_double_clicked(task_id))
        menu.addAction(open_subtasks_action)

        mark_action = QAction("Mark as Complete" if not task.completed else "Mark as Pending", self)
        mark_action.triggered.connect(lambda: self.toggle_task_status(task_id))
        menu.addAction(mark_action)

        menu.addSeparator()

        edit_action = QAction("Edit Task", self)
        edit_action.triggered.connect(lambda: self.edit_task(task_id))
        menu.addAction(edit_action)

        menu.addSeparator()

        delete_action = QAction("Delete Task", self)
        delete_action.triggered.connect(lambda: self.delete_task(task_id))
        menu.addAction(delete_action)

        menu.exec_(self.tasks_table.viewport().mapToGlobal(position))

    def view_task(self, task_id: str):
        task = self.main_window.manager.get_task(task_id)
        if not task:
            return
        dialog = TaskDetailsDialog(self, task=task, manager=self.main_window.manager)
        dialog.exec_()

    def edit_project(self):
        self.main_window.edit_project_by_id(self.project_id)

    def delete_project(self):
        self.main_window.delete_project_by_id(self.project_id)

    def clear_completed_tasks(self):
        tasks = self.main_window.manager.get_tasks_by_project(self.project_id)
        completed_tasks = [task for task in tasks if task.completed]

        if not completed_tasks:
            QMessageBox.information(self, 'Info', 'No completed tasks to clear')
            return

        reply = QMessageBox.question(
            self, 'Clear Completed Tasks',
            f'Clear {len(completed_tasks)} completed task(s)?\n\n'
            'This action cannot be undone.',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            for task in completed_tasks:
                if task.id in self._subtask_tabs:
                    self.close_subtask_tab_by_task(task.id)
                self.main_window.manager.delete_task(task.id)

            self.apply_filters()
            self.main_window.update_statistics()
            self.main_window.update_projects_tree_counts()
            self.load_project_data()
            self.update_label_filter_combo()
            self.update_clear_completed_button()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = ProjectManager()
        self.current_project_id: Optional[str] = None

        self.search_text = ""
        self.priority_filter = "All"
        self.label_filter = "All"
        self.show_completed = True
        self.stats_visible = False

        self.setWindowTitle('Smart Project Manager')
        self.setMinimumSize(900, 650)
        self.resize(1000, 700)

        self.setup_application_icon()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #181a1e;
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

        show_stats_action = QAction('Show Statistics', self)
        show_stats_action.setCheckable(True)
        show_stats_action.setChecked(False)
        show_stats_action.triggered.connect(self.toggle_statistics)
        view_menu.addAction(show_stats_action)

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
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        splitter = QSplitter(Qt.Horizontal)

        left_panel = QWidget()
        left_panel.setMinimumWidth(260)
        left_panel.setMaximumWidth(400)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(8)

        projects_header = QLabel('Projects')
        projects_header.setFont(QFont("Arial", 14, QFont.Bold))
        left_layout.addWidget(projects_header)

        project_buttons_layout = QHBoxLayout()
        project_buttons_layout.setSpacing(5)

        self.btn_new_project = QPushButton('+ New Project')
        self.btn_new_project.clicked.connect(self.create_project)
        self.btn_new_project.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                font-weight: bold;
                padding: 8px 12px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0066b3;
            }
        """)
        project_buttons_layout.addWidget(self.btn_new_project)

        left_layout.addLayout(project_buttons_layout)

        self.projects_tree = ProjectsTreeWidget(self)
        self.projects_tree.itemClicked.connect(self.on_project_selected)
        self.projects_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.projects_tree.customContextMenuRequested.connect(self.show_project_context_menu)
        left_layout.addWidget(self.projects_tree, 1)

        stats_header_layout = QHBoxLayout()
        stats_label = QLabel('Statistics')
        stats_label.setFont(QFont("Arial", 12, QFont.Bold))
        stats_header_layout.addWidget(stats_label)

        stats_header_layout.addStretch()

        self.btn_toggle_stats = QPushButton('▼')
        self.btn_toggle_stats.setFixedSize(25, 25)
        self.btn_toggle_stats.setToolTip("Toggle statistics visibility")
        self.btn_toggle_stats.clicked.connect(self.toggle_statistics_button)
        self.btn_toggle_stats.setStyleSheet("""
            QPushButton {
                background-color: #2a2d34;
                color: white;
                border: 1px solid #4a4d55;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)
        stats_header_layout.addWidget(self.btn_toggle_stats)

        left_layout.addLayout(stats_header_layout)

        self.statistics_widget = StatisticsWidget(self)
        self.statistics_widget.setVisible(False)
        self.btn_toggle_stats.setText('▶')
        left_layout.addWidget(self.statistics_widget)

        splitter.addWidget(left_panel)

        self.project_tabs = QTabWidget()
        self.project_tabs.setTabsClosable(False)
        self.project_tabs.setMovable(True)
        self.project_tabs.currentChanged.connect(self.on_project_tab_changed)
        self.project_tabs.setStyleSheet("""
            QTabWidget::pane {
                background-color: #1e2026;
                border: 1px solid #3a3d45;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #2a2d34;
                color: #aaa;
                padding: 8px 16px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                background-color: #1e2026;
                color: white;
                border-bottom: 2px solid #007acc;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3a3d45;
            }
        """)
        splitter.addWidget(self.project_tabs)

        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([300, 700])

        main_layout.addWidget(splitter)

        self.empty_label = QLabel('Select a project to view tasks')
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("""
            QLabel {
                color: #5a5d65;
                font-size: 16px;
                padding: 40px;
            }
        """)

        self.project_tabs.addTab(self.empty_label, "Welcome")

    def setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')

    def update_projects_tree_counts(self):
        for i in range(self.projects_tree.topLevelItemCount()):
            item = self.projects_tree.topLevelItem(i)
            if hasattr(item, 'project_id'):
                project = self.manager.get_project(item.project_id)
                if project:
                    task_count = len(project.tasks)
                    completed_tasks = sum(1 for task_id in project.tasks
                                         if self.manager.get_task(task_id) and
                                         self.manager.get_task(task_id).completed)
                    item.setText(0, f"{project.name} ({completed_tasks}/{task_count})")

    def select_project_in_tree(self, project_id: str):
        for i in range(self.projects_tree.topLevelItemCount()):
            item = self.projects_tree.topLevelItem(i)
            if hasattr(item, 'project_id') and item.project_id == project_id:
                self.projects_tree.setCurrentItem(item)
                break

    def load_projects(self):
        self.projects_tree.clear()
        projects = self.manager.get_all_projects()

        for project in projects:
            self.projects_tree.add_project(project, self.manager)

        self.update_statistics()

    def on_project_selected(self, item, column):
        if not item or not hasattr(item, 'project_id'):
            return

        project_id = item.project_id
        self.open_project_tab(project_id)

    def open_project_tab(self, project_id: str):
        for i in range(self.project_tabs.count()):
            widget = self.project_tabs.widget(i)
            if isinstance(widget, ProjectTab) and widget.project_id == project_id:
                self.project_tabs.setCurrentIndex(i)
                self.select_project_in_tree(project_id)
                return

        if self.project_tabs.count() == 1:
            widget = self.project_tabs.widget(0)
            if isinstance(widget, QLabel) and widget is self.empty_label:
                self.project_tabs.removeTab(0)

        project = self.manager.get_project(project_id)
        if not project:
            return

        tab = ProjectTab(self, project_id)
        index = self.project_tabs.addTab(tab, project.name)

        close_btn = QPushButton('✕')
        close_btn.setFixedSize(20, 20)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #e74c3c;
                border: none;
                font-size: 12px;
                font-weight: 900;
            }
            QPushButton:hover {
                background-color: #e74c3c;
                color: #ffffff;
                border-radius: 10px;
            }
            QPushButton:pressed {
                background-color: #a93226;
                color: #ffffff;
                border-radius: 10px;
            }
        """)
        close_btn.clicked.connect(lambda _, t=tab: self.close_project_tab_by_widget(t))
        self.project_tabs.tabBar().setTabButton(index, QTabBar.RightSide, close_btn)

        self.project_tabs.setCurrentIndex(index)
        self.current_project_id = project_id
        self.select_project_in_tree(project_id)

    def close_project_tab(self, index):
        widget = self.project_tabs.widget(index)
        if isinstance(widget, ProjectTab):
            self.project_tabs.removeTab(index)
            widget.deleteLater()

            if self.project_tabs.count() == 0:
                self.project_tabs.addTab(self.empty_label, "Welcome")
                self.current_project_id = None
                self.projects_tree.clearSelection()

    def close_project_tab_by_widget(self, widget):
        index = self.project_tabs.indexOf(widget)
        if index >= 0:
            self.close_project_tab(index)

    def on_project_tab_changed(self, index):
        widget = self.project_tabs.widget(index)
        if isinstance(widget, ProjectTab):
            self.current_project_id = widget.project_id
            self.select_project_in_tree(widget.project_id)
        else:
            self.current_project_id = None
            self.projects_tree.clearSelection()

    def create_project(self):
        dialog = ProjectDialog(self, manager=self.manager)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_project_data()
            if not data['name']:
                QMessageBox.warning(self, 'Error', 'Project name is required')
                return

            project = self.manager.create_project(**data)
            self.load_projects()
            self.open_project_tab(project.id)

    def edit_project_by_id(self, project_id: str):
        project = self.manager.get_project(project_id)
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

            for i in range(self.project_tabs.count()):
                widget = self.project_tabs.widget(i)
                if isinstance(widget, ProjectTab) and widget.project_id == project_id:
                    self.project_tabs.setTabText(i, project.name)
                    widget.load_project_data()
                    break

    def delete_project_by_id(self, project_id: str):
        project = self.manager.get_project(project_id)
        if not project:
            return

        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f'Delete project "{project.name}" and all its tasks/subtasks?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            for i in range(self.project_tabs.count()):
                widget = self.project_tabs.widget(i)
                if isinstance(widget, ProjectTab) and widget.project_id == project_id:
                    self.close_project_tab(i)
                    break

            self.manager.delete_project(project_id)
            self.load_projects()
            self.projects_tree.clearSelection()

    def create_task_in_current_project(self):
        if not self.current_project_id:
            QMessageBox.warning(self, 'Error', 'Please select a project first')
            return

        for i in range(self.project_tabs.count()):
            widget = self.project_tabs.widget(i)
            if isinstance(widget, ProjectTab) and widget.project_id == self.current_project_id:
                widget.create_task()
                break

    def show_project_context_menu(self, position):
        item = self.projects_tree.itemAt(position)
        if not item or not hasattr(item, 'project_id'):
            menu = QMenu()
            new_project_action = QAction("New Project", self)
            new_project_action.triggered.connect(self.create_project)
            menu.addAction(new_project_action)
            menu.addSeparator()
            refresh_action = QAction("Refresh", self)
            refresh_action.triggered.connect(self.refresh_view)
            menu.addAction(refresh_action)
            menu.exec_(self.projects_tree.viewport().mapToGlobal(position))
            return

        project_id = item.project_id
        project = self.manager.get_project(project_id)
        if not project:
            return

        menu = QMenu()

        open_action = QAction("Open in Tab", self)
        open_action.triggered.connect(lambda: self.open_project_tab(project_id))
        menu.addAction(open_action)

        menu.addSeparator()

        edit_action = QAction("Edit Project", self)
        edit_action.triggered.connect(lambda: self.edit_project_by_id(project_id))
        menu.addAction(edit_action)

        menu.addSeparator()

        delete_action = QAction("Delete Project", self)
        delete_action.triggered.connect(lambda: self.delete_project_by_id(project_id))
        menu.addAction(delete_action)

        menu.exec_(self.projects_tree.viewport().mapToGlobal(position))

    def manage_labels(self):
        dialog = LabelManagerDialog(self, self.manager)
        dialog.exec_()
        self.update_statistics()
        for i in range(self.project_tabs.count()):
            widget = self.project_tabs.widget(i)
            if isinstance(widget, ProjectTab):
                widget.update_label_filter_combo()
                widget.apply_filters()

    def refresh_view(self):
        self.load_projects()
        for i in range(self.project_tabs.count()):
            widget = self.project_tabs.widget(i)
            if isinstance(widget, ProjectTab):
                widget.load_project_data()
        self.status_bar.showMessage('View refreshed', 3000)

    def update_statistics(self):
        stats = self.manager.get_statistics()
        self.statistics_widget.update_stats(stats)

    def toggle_statistics(self, show: bool = None):
        if show is None:
            show = not self.stats_visible
        self.stats_visible = show
        self.statistics_widget.setVisible(show)
        self.statistics_widget.update()
        self.repaint()
        if show:
            self.btn_toggle_stats.setText('▼')
            self.btn_toggle_stats.setToolTip("Hide statistics")
        else:
            self.btn_toggle_stats.setText('▶')
            self.btn_toggle_stats.setToolTip("Show statistics")

    def toggle_statistics_button(self):
        self.toggle_statistics(not self.stats_visible)

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

            while self.project_tabs.count() > 0:
                widget = self.project_tabs.widget(0)
                self.project_tabs.removeTab(0)
                if widget is not self.empty_label:
                    widget.deleteLater()

            self.project_tabs.addTab(self.empty_label, "Welcome")
            self.current_project_id = None

            self.load_projects()
            self.update_statistics()

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
