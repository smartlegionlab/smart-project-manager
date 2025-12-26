from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton,
    QFrame, QScrollArea, QWidget
)
from datetime import datetime

from smart_project_manager.ui.widgets.label_widget import LabelWidget


class TaskDetailsDialog(QDialog):
    def __init__(self, parent=None, task=None, manager=None):
        super().__init__(parent)
        self.task = task
        self.manager = manager
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(f'Task Details: {self.task.title}')
        self.setMinimumWidth(600)
        self.setMaximumWidth(800)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #2d2d2d;
                border: none;
            }
        """)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        self._create_header(content_layout)

        if self.task.description:
            self._create_description_section(content_layout)

        self._create_info_section(content_layout)

        if self.task.labels:
            self._create_labels_section(content_layout)

        subtasks = self.manager.get_subtasks_by_task(self.task.id)
        if subtasks:
            self._create_subtasks_section(content_layout, subtasks)

        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        button_frame = QFrame()
        button_frame.setFrameStyle(QFrame.NoFrame)
        button_frame.setStyleSheet("background-color: #353535;")
        button_frame.setFixedHeight(50)
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(20, 0, 20, 0)

        button_layout.addStretch()

        close_button = QPushButton('Close')
        close_button.setFixedSize(100, 30)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        main_layout.addWidget(button_frame)

    def _create_header(self, layout):
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.NoFrame)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        title_label = QLabel(self.task.title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
                padding-bottom: 5px;
                border-bottom: 1px solid #444;
            }
        """)
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label)

        meta_widget = QWidget()
        meta_layout = QHBoxLayout(meta_widget)
        meta_layout.setContentsMargins(0, 0, 0, 0)
        meta_layout.setSpacing(15)

        status_label = QLabel("Status:")
        status_label.setStyleSheet("color: #aaa; font-size: 12px;")
        meta_layout.addWidget(status_label)

        status_value = QLabel("Completed" if self.task.completed else "Pending")
        status_value.setStyleSheet("color: #2ecc71;" if self.task.completed else "color: #ff9800;")
        meta_layout.addWidget(status_value)

        meta_layout.addSpacing(20)

        priority_label = QLabel("Priority:")
        priority_label.setStyleSheet("color: #aaa; font-size: 12px;")
        meta_layout.addWidget(priority_label)

        priority_value = QLabel(["High", "Medium", "Low"][self.task.priority - 1])
        priority_colors = ["#e74c3c", "#f39c12", "#3498db"]
        priority_value.setStyleSheet(f"color: {priority_colors[self.task.priority - 1]};")
        meta_layout.addWidget(priority_value)

        meta_layout.addStretch()
        header_layout.addWidget(meta_widget)

        layout.addWidget(header_frame)

    def _create_description_section(self, layout):
        desc_frame = QFrame()
        desc_frame.setFrameStyle(QFrame.NoFrame)
        desc_layout = QVBoxLayout(desc_frame)
        desc_layout.setContentsMargins(0, 0, 0, 0)
        desc_layout.setSpacing(5)

        desc_label = QLabel("Description")
        desc_label.setStyleSheet("""
            QLabel {
                color: #3498db;
                font-weight: bold;
                font-size: 13px;
            }
        """)
        desc_layout.addWidget(desc_label)

        desc_text = QTextEdit()
        desc_text.setPlainText(self.task.description)
        desc_text.setReadOnly(True)
        desc_text.setMaximumHeight(100)
        desc_text.setStyleSheet("""
            QTextEdit {
                background-color: #353535;
                border: 1px solid #444;
                border-radius: 3px;
                color: #cccccc;
                font-size: 13px;
                padding: 8px;
            }
        """)
        desc_layout.addWidget(desc_text)

        layout.addWidget(desc_frame)

    def _create_info_section(self, layout):
        info_frame = QFrame()
        info_frame.setFrameStyle(QFrame.NoFrame)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(12)

        info_label = QLabel("Task Information")
        info_label.setStyleSheet("""
            QLabel {
                color: #3498db;
                font-weight: bold;
                font-size: 13px;
            }
        """)
        info_layout.addWidget(info_label)

        progress = self.manager.get_task_progress(self.task.id)
        progress_widget = self._create_info_row("Progress:", f"{progress:.1f}%")
        info_layout.addWidget(progress_widget)

        dates_widget = QWidget()
        dates_layout = QHBoxLayout(dates_widget)
        dates_layout.setContentsMargins(0, 0, 0, 0)
        dates_layout.setSpacing(30)

        created_widget = self._create_info_row("Created:", self.task.created_at[:10])
        dates_layout.addWidget(created_widget)

        if self.task.updated_at and self.task.updated_at != self.task.created_at:
            updated_widget = self._create_info_row("Updated:", self.task.updated_at[:10])
            dates_layout.addWidget(updated_widget)

        if self.task.due_date:
            due_widget = self._create_info_row("Due Date:", self.task.due_date)
            if not self.task.completed and self._is_overdue(self.task.due_date):
                due_widget.findChild(QLabel, "value_label").setStyleSheet("color: #e74c3c; font-weight: bold;")
            dates_layout.addWidget(due_widget)

        dates_layout.addStretch()
        info_layout.addWidget(dates_widget)

        layout.addWidget(info_frame)

    def _create_labels_section(self, layout):
        labels_frame = QFrame()
        labels_frame.setFrameStyle(QFrame.NoFrame)
        labels_layout = QVBoxLayout(labels_frame)
        labels_layout.setContentsMargins(0, 0, 0, 0)
        labels_layout.setSpacing(8)

        labels_label = QLabel("Labels")
        labels_label.setStyleSheet("""
            QLabel {
                color: #3498db;
                font-weight: bold;
                font-size: 13px;
            }
        """)
        labels_layout.addWidget(labels_label)

        labels_container = QWidget()
        labels_container_layout = QHBoxLayout(labels_container)
        labels_container_layout.setContentsMargins(0, 0, 0, 0)
        labels_container_layout.setSpacing(8)

        for label_id in self.task.labels:
            label = self.manager.get_label(label_id)
            if label:
                label_widget = LabelWidget(label.name, label.color)
                label_widget.setMinimumHeight(24)
                label_widget.setMinimumWidth(70)
                labels_container_layout.addWidget(label_widget)

        labels_container_layout.addStretch()
        labels_layout.addWidget(labels_container)

        layout.addWidget(labels_frame)

    def _create_subtasks_section(self, layout, subtasks):
        subtasks_frame = QFrame()
        subtasks_frame.setFrameStyle(QFrame.NoFrame)
        subtasks_layout = QVBoxLayout(subtasks_frame)
        subtasks_layout.setContentsMargins(0, 0, 0, 0)
        subtasks_layout.setSpacing(8)

        subtasks_label = QLabel(f"Subtasks ({len(subtasks)})")
        subtasks_label.setStyleSheet("""
            QLabel {
                color: #3498db;
                font-weight: bold;
                font-size: 13px;
            }
        """)
        subtasks_layout.addWidget(subtasks_label)

        completed_count = sum(1 for st in subtasks if st.completed)
        stats_label = QLabel(f"{completed_count} of {len(subtasks)} completed")
        stats_label.setStyleSheet("color: #888; font-size: 11px; margin-bottom: 8px;")
        subtasks_layout.addWidget(stats_label)

        for subtask in subtasks:
            subtask_row = self._create_subtask_row(subtask)
            subtasks_layout.addWidget(subtask_row)

        layout.addWidget(subtasks_frame)

    def _create_info_row(self, label: str, value: str) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        label_widget = QLabel(label)
        label_widget.setStyleSheet("color: #aaa; font-size: 13px; min-width: 80px;")
        layout.addWidget(label_widget)

        value_widget = QLabel(value)
        value_widget.setObjectName("value_label")
        value_widget.setStyleSheet("color: white; font-size: 13px;")
        layout.addWidget(value_widget)

        layout.addStretch()
        return widget

    def _create_subtask_row(self, subtask) -> QWidget:
        widget = QFrame()
        widget.setFrameStyle(QFrame.NoFrame)
        widget.setStyleSheet("""
            QFrame {
                background-color: #353535;
                padding: 8px;
                border-radius: 3px;
            }
        """)

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        status_label = QLabel("✓" if subtask.completed else "○")
        status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                min-width: 20px;
            }
        """)
        if subtask.completed:
            status_label.setStyleSheet("color: #2ecc71; font-size: 14px; min-width: 20px;")
        layout.addWidget(status_label)

        title_label = QLabel(subtask.title)
        if subtask.completed:
            title_label.setStyleSheet("color: #888; font-size: 13px; text-decoration: line-through;")
        else:
            title_label.setStyleSheet("color: white; font-size: 13px;")
        layout.addWidget(title_label, 1)

        if subtask.description:
            desc_label = QLabel(subtask.description)
            desc_label.setStyleSheet("color: #aaa; font-size: 11px;")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label, 2)

        if subtask.due_date:
            due_label = QLabel(f"Due: {subtask.due_date}")
            if not subtask.completed and self._is_overdue(subtask.due_date):
                due_label.setStyleSheet("color: #e74c3c; font-size: 11px;")
            else:
                due_label.setStyleSheet("color: #888; font-size: 11px;")
            layout.addWidget(due_label)

        priority_label = QLabel(["High", "Med", "Low"][subtask.priority - 1])
        priority_colors = ["#e74c3c", "#f39c12", "#3498db"]
        priority_label.setStyleSheet(f"""
            QLabel {{
                color: {priority_colors[subtask.priority - 1]};
                font-size: 11px;
                font-weight: bold;
                min-width: 30px;
            }}
        """)
        layout.addWidget(priority_label)

        return widget

    def _is_overdue(self, due_date_str: str) -> bool:
        try:
            due_date = datetime.fromisoformat(due_date_str).date()
            return due_date < datetime.now().date()
        except:
            return False
