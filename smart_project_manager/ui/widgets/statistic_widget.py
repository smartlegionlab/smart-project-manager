from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QProgressBar, QPushButton
)


class StatisticsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

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

        self.projects_box = self._create_stat_box("📁", "Projects", "#3498db")
        self.stats_projects = QLabel("0")
        self.stats_projects.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: white;
                qproperty-alignment: 'AlignCenter';
            }
        """)
        self.projects_box.layout().insertWidget(1, self.stats_projects)
        main_stats_layout.addWidget(self.projects_box, 0, 0)

        self.tasks_box = self._create_stat_box("✅", "Tasks", "#2ecc71")
        self.stats_tasks = QLabel("0")
        self.stats_tasks.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: white;
                qproperty-alignment: 'AlignCenter';
            }
        """)
        self.tasks_box.layout().insertWidget(1, self.stats_tasks)
        main_stats_layout.addWidget(self.tasks_box, 0, 1)

        self.subtasks_box = self._create_stat_box("📝", "Subtasks", "#9b59b6")
        self.stats_subtasks = QLabel("0")
        self.stats_subtasks.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: white;
                qproperty-alignment: 'AlignCenter';
            }
        """)
        self.subtasks_box.layout().insertWidget(1, self.stats_subtasks)
        main_stats_layout.addWidget(self.subtasks_box, 1, 0)

        self.labels_box = self._create_stat_box("🏷️", "Labels", "#e74c3c")
        self.stats_labels = QLabel("0")
        self.stats_labels.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: white;
                qproperty-alignment: 'AlignCenter';
            }
        """)
        self.labels_box.layout().insertWidget(1, self.stats_labels)
        main_stats_layout.addWidget(self.labels_box, 1, 1)

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
        refresh_stats_btn.clicked.connect(self.parent().update_statistics)
        refresh_stats_btn.setToolTip("Refresh statistics")
        data_info_layout.addWidget(refresh_stats_btn)

        stats_layout.addLayout(data_info_layout)

        layout.addWidget(stats_group)

    def _create_stat_box(self, icon: str, title: str, color: str) -> QGroupBox:
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

    def update_stats(self, stats):
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
