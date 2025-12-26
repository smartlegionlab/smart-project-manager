# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
from datetime import datetime
from typing import Optional

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QHBoxLayout,
    QGroupBox,
    QMenu,
    QAction,
    QGridLayout,
    QDesktopWidget,
    QStatusBar,
    QMainWindow,
    QTreeWidget,
    QTreeWidgetItem,
    QProgressBar,
    QFileDialog
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

from smart_project_manager.managers.project_manager import ProjectManager
from smart_project_manager.ui.dialogs.label_manager_dialog import LabelManagerDialog
from smart_project_manager.ui.dialogs.project_dialog import ProjectDialog
from smart_project_manager.ui.dialogs.task_dialog import TaskDialog
from smart_project_manager.ui.widgets.label_widget import LabelWidget
from smart_project_manager.ui.widgets.priority_widget import PriorityIndicatorWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.manager = ProjectManager()
        self.current_project_id: Optional[str] = None

        self.setWindowTitle('Smart Project Manager v0.1.2')
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

        self.center_window()
        self.selected_project_item = None

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

        self.btn_delete_project = QPushButton('Delete')
        self.btn_delete_project.clicked.connect(self.delete_current_project)
        self.btn_delete_project.setEnabled(False)
        self.btn_delete_project.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
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
        project_buttons_layout.addWidget(self.btn_delete_project)

        left_layout.addLayout(project_buttons_layout)

        self.projects_tree = QTreeWidget()
        self.projects_tree.setHeaderLabel('Projects')
        self.projects_tree.setStyleSheet("""
            QTreeWidget {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 5px;
            }
            QTreeWidget::item {
                padding: 8px 5px;
                border-bottom: 1px solid #333;
            }
            QTreeWidget::item:selected {
                background-color: #2a82da;
                color: white;
            }
            QTreeWidget::item:hover:!selected {
                background-color: #3a3a3a;
            }
        """)
        self.projects_tree.itemClicked.connect(self.on_project_selected)
        left_layout.addWidget(self.projects_tree, 1)

        stats_group = QGroupBox("📊 Global Statistics")
        stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #444;
                border-radius: 8px;
                padding-top: 10px;
                margin-top: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2a82da;
            }
        """)
        stats_layout = QVBoxLayout(stats_group)
        stats_layout.setSpacing(8)

        main_stats_layout = QGridLayout()
        main_stats_layout.setSpacing(5)
        main_stats_layout.setContentsMargins(5, 5, 5, 5)

        projects_box = self.create_stat_box("📁", "Projects", "#3498db")
        self.stats_projects = QLabel("0")
        self.stats_projects.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: white;
                qproperty-alignment: 'AlignCenter';
            }
        """)
        projects_box.layout().insertWidget(1, self.stats_projects)
        main_stats_layout.addWidget(projects_box, 0, 0)

        tasks_box = self.create_stat_box("✅", "Tasks", "#2ecc71")
        self.stats_tasks = QLabel("0")
        self.stats_tasks.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: white;
                qproperty-alignment: 'AlignCenter';
            }
        """)
        tasks_box.layout().insertWidget(1, self.stats_tasks)
        main_stats_layout.addWidget(tasks_box, 0, 1)

        subtasks_box = self.create_stat_box("📝", "Subtasks", "#9b59b6")
        self.stats_subtasks = QLabel("0")
        self.stats_subtasks.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: white;
                qproperty-alignment: 'AlignCenter';
            }
        """)
        subtasks_box.layout().insertWidget(1, self.stats_subtasks)
        main_stats_layout.addWidget(subtasks_box, 1, 0)

        labels_box = self.create_stat_box("🏷️", "Labels", "#e74c3c")
        self.stats_labels = QLabel("0")
        self.stats_labels.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: white;
                qproperty-alignment: 'AlignCenter';
            }
        """)
        labels_box.layout().insertWidget(1, self.stats_labels)
        main_stats_layout.addWidget(labels_box, 1, 1)

        stats_layout.addLayout(main_stats_layout)

        completion_group = QGroupBox("Completion")
        completion_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #444;
                border-radius: 5px;
                margin-top: 5px;
            }
        """)
        completion_layout = QVBoxLayout(completion_group)
        completion_layout.setSpacing(5)
        completion_layout.setContentsMargins(8, 12, 8, 8)

        tasks_progress_layout = QHBoxLayout()
        tasks_progress_label = QLabel("Tasks:")
        tasks_progress_label.setStyleSheet("color: #aaa; font-size: 11px;")
        tasks_progress_layout.addWidget(tasks_progress_label)

        tasks_progress_layout.addStretch()

        self.stats_completed_tasks = QLabel("0/0")
        self.stats_completed_tasks.setStyleSheet("color: #2ecc71; font-weight: bold; font-size: 11px;")
        tasks_progress_layout.addWidget(self.stats_completed_tasks)

        completion_layout.addLayout(tasks_progress_layout)

        self.tasks_progress_bar = QProgressBar()
        self.tasks_progress_bar.setTextVisible(True)
        self.tasks_progress_bar.setFormat("%p%")
        self.tasks_progress_bar.setStyleSheet("""
            QProgressBar {
                height: 14px;
                border: 1px solid #444;
                border-radius: 7px;
                text-align: center;
                padding: 0px 2px;
                font-size: 9px;
                font-weight: bold;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
                border-radius: 6px;
            }
        """)
        self.tasks_progress_bar.setValue(0)
        completion_layout.addWidget(self.tasks_progress_bar)

        subtasks_progress_layout = QHBoxLayout()
        subtasks_progress_label = QLabel("Subtasks:")
        subtasks_progress_label.setStyleSheet("color: #aaa; font-size: 11px;")
        subtasks_progress_layout.addWidget(subtasks_progress_label)

        subtasks_progress_layout.addStretch()

        self.stats_completed_subtasks = QLabel("0/0")
        self.stats_completed_subtasks.setStyleSheet("color: #9b59b6; font-weight: bold; font-size: 11px;")
        subtasks_progress_layout.addWidget(self.stats_completed_subtasks)

        completion_layout.addLayout(subtasks_progress_layout)

        self.subtasks_progress_bar = QProgressBar()
        self.subtasks_progress_bar.setTextVisible(True)
        self.subtasks_progress_bar.setFormat("%p%")
        self.subtasks_progress_bar.setStyleSheet("""
            QProgressBar {
                height: 14px;
                border: 1px solid #444;
                border-radius: 7px;
                text-align: center;
                padding: 0px 2px;
                font-size: 9px;
                font-weight: bold;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #9b59b6;
                border-radius: 6px;
            }
        """)
        self.subtasks_progress_bar.setValue(0)
        completion_layout.addWidget(self.subtasks_progress_bar)

        stats_layout.addWidget(completion_group)

        data_info_layout = QHBoxLayout()
        data_info_layout.setSpacing(5)

        data_info_label = QLabel("💾")
        data_info_label.setStyleSheet("font-size: 11px;")
        data_info_layout.addWidget(data_info_label)

        data_path_label = QLabel("~/.project_manager")
        data_path_label.setStyleSheet("color: #888; font-size: 9px; font-family: monospace;")
        data_info_layout.addWidget(data_path_label)

        data_info_layout.addStretch()

        refresh_stats_btn = QPushButton("🔄")
        refresh_stats_btn.setFixedSize(20, 20)
        refresh_stats_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #3498db;
            }
        """)
        refresh_stats_btn.clicked.connect(self.update_statistics)
        refresh_stats_btn.setToolTip("Refresh statistics")
        data_info_layout.addWidget(refresh_stats_btn)

        stats_layout.addLayout(data_info_layout)

        left_layout.addWidget(stats_group)

        main_layout.addWidget(left_panel)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        tasks_header_layout = QHBoxLayout()

        self.tasks_header = QLabel('Select a project to view tasks')
        self.tasks_header.setFont(QFont("Arial", 14, QFont.Bold))
        tasks_header_layout.addWidget(self.tasks_header)

        tasks_header_layout.addStretch()

        self.btn_refresh = QPushButton('🔄 Refresh')
        self.btn_refresh.clicked.connect(self.refresh_view)
        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.btn_refresh.setToolTip("Refresh view (F5)")
        tasks_header_layout.addWidget(self.btn_refresh)

        self.btn_new_task = QPushButton('+ New Task')
        self.btn_new_task.clicked.connect(self.create_task)
        self.btn_new_task.setEnabled(False)
        self.btn_new_task.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        tasks_header_layout.addWidget(self.btn_new_task)

        right_layout.addLayout(tasks_header_layout)

        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(8)
        self.tasks_table.setHorizontalHeaderLabels(
            ['Title', 'Priority', 'Status', 'Progress', 'Due Date', 'Labels', 'Edit', 'Delete']
        )
        self.tasks_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tasks_table.setAlternatingRowColors(True)
        self.tasks_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tasks_table.customContextMenuRequested.connect(self.show_task_context_menu)
        self.tasks_table.setStyleSheet("""
            QTableWidget {
                background-color: #2a2a2a;
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #353535;
                padding: 8px;
                border: 1px solid #444;
                font-weight: bold;
            }
        """)

        self.tasks_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tasks_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tasks_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tasks_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tasks_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tasks_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.tasks_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.tasks_table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)

        right_layout.addWidget(self.tasks_table, 3)

        self.project_progress_group = QGroupBox("📊 Project Progress")
        self.project_progress_group.setStyleSheet("""
                    QGroupBox {
                        font-weight: bold;
                        border: 2px solid #444;
                        border-radius: 8px;
                        margin-top: 10px;
                        padding-top: 10px;
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        left: 10px;
                        padding: 0 5px 0 5px;
                        color: #2a82da;
                    }
                """)

        self.project_progress_layout = QVBoxLayout(self.project_progress_group)
        self.project_progress_layout.setSpacing(8)
        self.project_progress_layout.setContentsMargins(10, 12, 10, 10)

        top_line = QHBoxLayout()

        self.project_name_label = QLabel("--")
        self.project_name_label.setStyleSheet("""
                    QLabel {
                        font-size: 16px;
                        font-weight: bold;
                        color: #3498db;
                    }
                """)
        top_line.addWidget(self.project_name_label)

        top_line.addStretch()

        self.project_version_badge = QLabel("v-- | --")
        self.project_version_badge.setStyleSheet("""
                    QLabel {
                        background-color: #95a5a6;
                        color: white;
                        padding: 3px 8px;
                        border-radius: 10px;
                        font-weight: bold;
                        font-size: 10px;
                        min-width: 90px;
                        text-align: center;
                    }
                """)
        top_line.addWidget(self.project_version_badge)

        self.project_progress_layout.addLayout(top_line)

        self.project_description_label = QLabel("--")
        self.project_description_label.setStyleSheet("""
                    QLabel {
                        font-size: 11px;
                        color: #aaa;
                        font-style: italic;
                        margin-bottom: 5px;
                    }
                """)
        self.project_description_label.setWordWrap(True)
        self.project_progress_layout.addWidget(self.project_description_label)

        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(3)

        progress_line = QHBoxLayout()

        progress_label = QLabel("Progress")
        progress_label.setStyleSheet("font-weight: bold; font-size: 11px;")
        progress_line.addWidget(progress_label)

        progress_line.addStretch()

        progress_layout.addLayout(progress_line)

        progress_bar_line = QHBoxLayout()

        self.project_progress_bar = QProgressBar()
        self.project_progress_bar.setTextVisible(False)
        self.project_progress_bar.setFixedHeight(16)
        self.project_progress_bar.setStyleSheet("""
                    QProgressBar {
                        border: 1px solid #444;
                        border-radius: 8px;
                        background-color: #2a2a2a;
                    }
                    QProgressBar::chunk {
                        background-color: qlineargradient(
                            spread:pad, x1:0, y1:0, x2:1, y2:0,
                            stop:0 #3498db,
                            stop:1 #2ecc71
                        );
                        border-radius: 7px;
                    }
                """)
        progress_bar_line.addWidget(self.project_progress_bar, 3)

        self.project_progress_text = QLabel("0%")
        self.project_progress_text.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        color: #2ecc71;
                        font-size: 12px;
                        margin-left: 10px;
                        min-width: 40px;
                    }
                """)
        progress_bar_line.addWidget(self.project_progress_text)

        progress_layout.addLayout(progress_bar_line)
        self.project_progress_layout.addLayout(progress_layout)

        stats_line = QHBoxLayout()
        stats_line.setSpacing(15)

        tasks_container = QWidget()
        tasks_layout = QHBoxLayout(tasks_container)
        tasks_layout.setContentsMargins(0, 0, 0, 0)
        tasks_layout.setSpacing(5)

        tasks_icon = QLabel("✅")
        tasks_icon.setStyleSheet("font-size: 12px;")
        tasks_layout.addWidget(tasks_icon)

        tasks_stats = QVBoxLayout()
        tasks_stats.setSpacing(1)

        self.project_tasks_total = QLabel("0")
        self.project_tasks_total.setStyleSheet("""
                    QLabel {
                        font-size: 14px;
                        font-weight: bold;
                        color: white;
                    }
                """)
        tasks_stats.addWidget(self.project_tasks_total)

        tasks_label = QLabel("tasks")
        tasks_label.setStyleSheet("color: #2ecc71; font-size: 9px;")
        tasks_stats.addWidget(tasks_label)

        tasks_layout.addLayout(tasks_stats)
        stats_line.addWidget(tasks_container)

        subtasks_container = QWidget()
        subtasks_layout = QHBoxLayout(subtasks_container)
        subtasks_layout.setContentsMargins(0, 0, 0, 0)
        subtasks_layout.setSpacing(5)

        subtasks_icon = QLabel("📝")
        subtasks_icon.setStyleSheet("font-size: 12px;")
        subtasks_layout.addWidget(subtasks_icon)

        subtasks_stats = QVBoxLayout()
        subtasks_stats.setSpacing(1)

        self.project_subtasks_total = QLabel("0")
        self.project_subtasks_total.setStyleSheet("""
                    QLabel {
                        font-size: 14px;
                        font-weight: bold;
                        color: white;
                    }
                """)
        subtasks_stats.addWidget(self.project_subtasks_total)

        subtasks_label = QLabel("subtasks")
        subtasks_label.setStyleSheet("color: #9b59b6; font-size: 9px;")
        subtasks_stats.addWidget(subtasks_label)

        subtasks_layout.addLayout(subtasks_stats)
        stats_line.addWidget(subtasks_container)

        timeline_container = QWidget()
        timeline_layout = QHBoxLayout(timeline_container)
        timeline_layout.setContentsMargins(0, 0, 0, 0)
        timeline_layout.setSpacing(5)

        timeline_icon = QLabel("📅")
        timeline_icon.setStyleSheet("font-size: 12px;")
        timeline_layout.addWidget(timeline_icon)

        timeline_stats = QVBoxLayout()
        timeline_stats.setSpacing(1)

        self.project_updated_label = QLabel("--")
        self.project_updated_label.setStyleSheet("""
                    QLabel {
                        font-size: 11px;
                        font-weight: bold;
                        color: white;
                    }
                """)
        timeline_stats.addWidget(self.project_updated_label)

        timeline_label = QLabel("updated")
        timeline_label.setStyleSheet("color: #e74c3c; font-size: 9px;")
        timeline_stats.addWidget(timeline_label)

        timeline_layout.addLayout(timeline_stats)
        stats_line.addWidget(timeline_container)

        stats_line.addStretch()
        self.project_progress_layout.addLayout(stats_line)

        self.project_progress_group.setVisible(False)
        right_layout.addWidget(self.project_progress_group)

        main_layout.addWidget(right_panel, 1)

    def create_stat_box(self, icon: str, title: str, color: str) -> QGroupBox:
        box = QGroupBox()
        box.setStyleSheet(f"""
            QGroupBox {{
                border: 1px solid #444;
                border-radius: 6px;
                background-color: #2a2a2a;
                min-height: 70px;
            }}
        """)

        layout = QVBoxLayout(box)
        layout.setSpacing(3)
        layout.setContentsMargins(5, 8, 5, 8)

        header_layout = QHBoxLayout()

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 14px;")
        header_layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-weight: bold; color: {color}; font-size: 11px;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()
        layout.addLayout(header_layout)

        layout.addStretch()

        subtitle = QLabel("Total")
        subtitle.setStyleSheet("color: #aaa; font-size: 9px; qproperty-alignment: 'AlignCenter';")
        layout.addWidget(subtitle)

        return box

    def update_project_progress_panel(self, project_id: str):
        project = self.manager.get_project(project_id)
        if not project:
            self.project_progress_group.setVisible(False)
            return

        self.project_progress_group.setVisible(True)
        self.project_progress_group.setTitle(f"📊 Project Progress")

        self.project_name_label.setText(project.name)

        if project.description:
            self.project_description_label.setText(project.description)
        else:
            self.project_description_label.setText("No description")

        self.project_version_badge.setText(f"v{project.version}")

        tasks = self.manager.get_tasks_by_project(project_id)
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.completed)

        total_subtasks = 0
        completed_subtasks = 0

        for task in tasks:
            subtasks = self.manager.get_subtasks_by_task(task.id)
            total_subtasks += len(subtasks)
            completed_subtasks += sum(1 for subtask in subtasks if subtask.completed)

        progress = self.manager.get_project_progress(project_id)
        self.project_progress_bar.setValue(int(progress))
        self.project_progress_text.setText(f"{progress:.1f}%")

        if progress == 100:
            status_text = "✅ Completed"
            status_color = "#2e7d32"
        elif progress > 70:
            status_text = "⚡ In Progress"
            status_color = "#2ecc71"
        elif progress > 30:
            status_text = "🔄 Active"
            status_color = "#3498db"
        elif progress > 0:
            status_text = "🟡 Started"
            status_color = "#f39c12"
        else:
            status_text = "⏳ Not Started"
            status_color = "#95a5a6"

        self.project_version_badge.setText(f"v{project.version} | {status_text}")
        self.project_version_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {status_color};
                color: white;
                padding: 3px 8px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 10px;
                min-width: 90px;
                text-align: center;
            }}
        """)

        self.project_tasks_total.setText(f"{completed_tasks}/{total_tasks}")
        self.project_subtasks_total.setText(f"{completed_subtasks}/{total_subtasks}")

        if project.updated_at:
            try:
                updated_date = datetime.fromisoformat(project.updated_at.replace('Z', '+00:00'))
                updated_formatted = updated_date.strftime("%d %b")
                self.project_updated_label.setText(f"{updated_formatted}")
            except:
                self.project_updated_label.setText(f"{project.updated_at[:5]}")
        else:
            self.project_updated_label.setText("--")

    def setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('Ready')

    def load_projects(self):
        self.projects_tree.clear()

        projects = self.manager.get_all_projects()

        for project in projects:
            item = QTreeWidgetItem(self.projects_tree)
            item.setText(0, f"{project.name} v{project.version}")
            item.project_id = project.id

            task_count = len(project.tasks)
            completed_tasks = sum(1 for task_id in project.tasks
                                  if self.manager.get_task(task_id) and
                                  self.manager.get_task(task_id).completed)

            progress_text = f" ({completed_tasks}/{task_count})"
            item.setText(0, f"{project.name} v{project.version}{progress_text}")

            if project.description:
                item.setToolTip(0, project.description)

            if self.current_project_id and project.id == self.current_project_id:
                self.projects_tree.setCurrentItem(item)
                self.selected_project_item = item

        self.update_statistics()

    def on_project_selected(self, item, column):
        self.current_project_id = item.project_id
        self.selected_project_item = item
        self.btn_delete_project.setEnabled(True)
        self.btn_new_task.setEnabled(True)

        project = self.manager.get_project(self.current_project_id)
        if project:
            self.tasks_header.setText(f'📋 Tasks in "{project.name}"')

            self.update_project_progress_panel(project.id)

            self.load_tasks_for_project(project.id)

    def load_tasks_for_project(self, project_id: str):
        self.tasks_table.setRowCount(0)

        tasks = self.manager.get_tasks_by_project(project_id)

        for row, task in enumerate(tasks):
            self.tasks_table.insertRow(row)

            title_item = QTableWidgetItem(task.title)
            if task.description:
                title_item.setToolTip(task.description)
            if task.completed:
                title_item.setForeground(QColor(100, 100, 100))
                font = title_item.font()
                font.setStrikeOut(True)
                title_item.setFont(font)
            self.tasks_table.setItem(row, 0, title_item)

            priority_widget = PriorityIndicatorWidget(task.priority)
            self.tasks_table.setCellWidget(row, 1, priority_widget)

            status_button = QPushButton("✅ Completed" if task.completed else "⏳ Pending")
            status_button.setCheckable(True)
            status_button.setChecked(task.completed)
            status_button.setStyleSheet("""
                QPushButton {
                    border-radius: 3px;
                    padding: 5px 10px;
                    min-width: 100px;
                }
                QPushButton:checked {
                    background-color: #2e7d32;
                    color: white;
                }
                QPushButton:!checked {
                    background-color: #ff9800;
                    color: white;
                }
            """)
            status_button.clicked.connect(lambda checked, tid=task.id: self.toggle_task_status(tid))
            self.tasks_table.setCellWidget(row, 2, status_button)

            progress = self.manager.get_task_progress(task.id)
            progress_bar = QProgressBar()
            progress_bar.setValue(int(progress))
            progress_bar.setTextVisible(True)
            progress_bar.setFormat(f"{progress:.1f}%")
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #444;
                    border-radius: 3px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #2a82da;
                    border-radius: 3px;
                }
            """)
            self.tasks_table.setCellWidget(row, 3, progress_bar)

            due_text = task.due_date if task.due_date else "No due date"
            due_item = QTableWidgetItem(due_text)
            due_item.setTextAlignment(Qt.AlignCenter)

            if task.due_date and not task.completed:
                due_date = datetime.fromisoformat(task.due_date).date()
                if due_date < datetime.now().date():
                    due_item.setForeground(QColor(255, 100, 100))

            self.tasks_table.setItem(row, 4, due_item)

            labels_widget = QWidget()
            labels_layout = QHBoxLayout(labels_widget)
            labels_layout.setContentsMargins(5, 2, 5, 2)
            labels_layout.setSpacing(5)

            for label_id in task.labels:
                label = self.manager.get_label(label_id)
                if label:
                    label_widget = LabelWidget(label.name, label.color)
                    label_widget.setMinimumHeight(24)
                    label_widget.setMinimumWidth(60)
                    labels_layout.addWidget(label_widget)

            labels_layout.addStretch()
            self.tasks_table.setCellWidget(row, 5, labels_widget)

            edit_button = QPushButton("✏️ Edit")
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #ff9800;
                    color: white;
                    border-radius: 3px;
                    padding: 5px 10px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #e68900;
                }
            """)
            edit_button.clicked.connect(lambda checked, tid=task.id: self.edit_task(tid))
            self.tasks_table.setCellWidget(row, 6, edit_button)

            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #da2a2a;
                    color: white;
                    border-radius: 3px;
                    padding: 5px 10px;
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #ca1a1a;
                }
            """)
            delete_button.clicked.connect(lambda checked, tid=task.id: self.delete_task(tid))
            self.tasks_table.setCellWidget(row, 7, delete_button)

    def toggle_task_status(self, task_id: str):
        task = self.manager.get_task(task_id)
        if task:
            task.toggle_complete()
            self.manager.update_task(task_id, completed=task.completed)

            if self.current_project_id:
                self.load_tasks_for_project(self.current_project_id)
                self.update_statistics()

                self.load_projects()

                self.update_project_progress_panel(self.current_project_id)

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
            self.current_project_id = None
            self.selected_project_item = None
            self.btn_delete_project.setEnabled(False)
            self.btn_new_task.setEnabled(False)
            self.tasks_header.setText('Select a project to view tasks')
            self.tasks_table.setRowCount(0)

            self.project_progress_group.setVisible(False)

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

            self.update_project_progress_panel(self.current_project_id)

            QMessageBox.information(self, 'Success', f'Task "{task.title}" created')

    def edit_task(self, task_id: str):
        task = self.manager.get_task(task_id)
        if not task:
            return

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

                self.update_project_progress_panel(self.current_project_id)

    def on_task_updated(self):
        if self.current_project_id:
            self.load_tasks_for_project(self.current_project_id)
            self.update_statistics()

            self.load_projects()

            self.update_project_progress_panel(self.current_project_id)

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

                self.update_project_progress_panel(self.current_project_id)

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

        dialog = QDialog(self)
        dialog.setWindowTitle(f'Task: {task.title}')
        dialog.setMinimumWidth(500)

        layout = QVBoxLayout(dialog)

        title_label = QLabel(f'<h2>{task.title}</h2>')
        layout.addWidget(title_label)

        if task.description:
            desc_label = QLabel(task.description)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("padding: 10px; background-color: #2a2a2a; border-radius: 5px;")
            layout.addWidget(desc_label)

        details_group = QGroupBox("Details")
        details_layout = QVBoxLayout()

        priority_text = ["🚨 High", "⚠️ Medium", "📋 Low"][task.priority - 1]
        priority_label = QLabel(f'<b>Priority:</b> {priority_text}')
        details_layout.addWidget(priority_label)

        status_text = "✅ Completed" if task.completed else "⏳ Pending"
        status_label = QLabel(f'<b>Status:</b> {status_text}')
        details_layout.addWidget(status_label)

        progress = self.manager.get_task_progress(task.id)
        progress_label = QLabel(f'<b>Progress:</b> {progress:.1f}%')
        details_layout.addWidget(progress_label)

        dates_layout = QHBoxLayout()
        created_label = QLabel(f'<b>Created:</b> {task.created_at[:10]}')
        dates_layout.addWidget(created_label)

        dates_layout.addStretch()

        if task.due_date:
            due_label = QLabel(f'<b>Due:</b> {task.due_date}')
            dates_layout.addWidget(due_label)

        details_layout.addLayout(dates_layout)

        if task.labels:
            labels_label = QLabel('<b>Labels:</b>')
            details_layout.addWidget(labels_label)

            labels_widget = QWidget()
            labels_widget_layout = QHBoxLayout(labels_widget)
            labels_widget_layout.setContentsMargins(0, 0, 0, 0)

            for label_id in task.labels:
                label = self.manager.get_label(label_id)
                if label:
                    label_widget = LabelWidget(label.name, label.color)
                    labels_widget_layout.addWidget(label_widget)

            labels_widget_layout.addStretch()
            details_layout.addWidget(labels_widget)

        details_group.setLayout(details_layout)
        layout.addWidget(details_group)

        subtasks = self.manager.get_subtasks_by_task(task.id)
        if subtasks:
            subtasks_group = QGroupBox(f"Subtasks ({len(subtasks)})")
            subtasks_layout = QVBoxLayout()

            for subtask in subtasks:
                subtask_widget = QWidget()
                subtask_layout = QHBoxLayout(subtask_widget)

                status = "✅" if subtask.completed else "⏳"
                subtask_label = QLabel(f'{status} {subtask.title}')
                subtask_layout.addWidget(subtask_label)

                if subtask.due_date:
                    due_label = QLabel(f'Due: {subtask.due_date}')
                    due_label.setStyleSheet("color: #888;")
                    subtask_layout.addWidget(due_label)

                subtask_layout.addStretch()
                subtasks_layout.addWidget(subtask_widget)

            subtasks_group.setLayout(subtasks_layout)
            layout.addWidget(subtasks_group)

        close_button = QPushButton('Close')
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.exec_()

    def refresh_view(self):
        self.load_projects()
        if self.current_project_id:
            self.load_tasks_for_project(self.current_project_id)
            self.update_project_progress_panel(self.current_project_id)

        self.status_bar.showMessage('View refreshed', 3000)

    def toggle_show_completed(self, show: bool):
        # TODO
        self.refresh_view()

    def update_statistics(self):
        stats = self.manager.get_statistics()

        self.stats_projects.setText(str(stats['projects']))
        self.stats_tasks.setText(str(stats['tasks']))
        self.stats_subtasks.setText(str(stats['subtasks']))
        self.stats_labels.setText(str(stats['labels']))

        tasks_completed = stats['completed_tasks']
        tasks_total = stats['tasks']
        tasks_percentage = stats['task_completion_rate']

        self.stats_completed_tasks.setText(f"{tasks_completed}/{tasks_total}")
        self.tasks_progress_bar.setValue(int(tasks_percentage))

        subtasks_completed = stats['completed_subtasks']
        subtasks_total = stats['subtasks']
        subtasks_percentage = stats['subtask_completion_rate']

        self.stats_completed_subtasks.setText(f"{subtasks_completed}/{subtasks_total}")
        self.subtasks_progress_bar.setValue(int(subtasks_percentage))

        if tasks_total > 0:
            self.tasks_progress_bar.setFormat(f"{tasks_percentage:.1f}%")
        else:
            self.tasks_progress_bar.setFormat("No tasks")

        if subtasks_total > 0:
            self.subtasks_progress_bar.setFormat(f"{subtasks_percentage:.1f}%")
        else:
            self.subtasks_progress_bar.setFormat("No subtasks")

    def import_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Data",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if not file_path:
            return

        reply = QMessageBox.question(
            self,
            "Import Options",
            "How to import?\n\n"
            "Yes: Merge with current data\n"
            "No: Replace current data",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Cancel:
            return

        strategy = "merge" if reply == QMessageBox.Yes else "replace"

        try:
            result = self.manager.import_data(file_path, strategy)

            if result['success']:
                self.manager.load_data()

                self.current_project_id = None
                self.selected_project_item = None
                self.btn_delete_project.setEnabled(False)
                self.btn_new_task.setEnabled(False)
                self.tasks_header.setText('Select a project to view tasks')
                self.tasks_table.setRowCount(0)
                self.project_progress_group.setVisible(False)

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
                    f"Failed to import: {result.get('error', 'Unknown error')}"
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Import Error",
                f"Import failed:\n\n{str(e)}"
            )

    def export_data(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Data",
            f"projects_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
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
            """<h2>Smart Project Manager v0.1.2</h2>
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
