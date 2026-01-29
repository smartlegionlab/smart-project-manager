from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar, QWidget,
    QHBoxLayout, QPushButton, QAbstractItemView
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from datetime import datetime

from smart_project_manager.ui.widgets.priority_widget import PriorityIndicatorWidget
from smart_project_manager.ui.widgets.label_widget import LabelWidget


class TaskTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_selection_behavior()
        self.setup_table()
        self.setFocusPolicy(Qt.NoFocus)
        self.selected_task_id = None

        self.itemSelectionChanged.connect(self.save_selection)

    def save_selection(self):
        selected = self.selectedItems()
        if selected:
            row = selected[1].row()
            item = self.item(row, 1)
            self.selected_task_id = item.data(Qt.UserRole)

    def restore_selection(self):
        if not self.selected_task_id:
            return

        for row in range(self.rowCount()):
            item = self.item(row, 1)
            if item and item.data(Qt.UserRole) == self.selected_task_id:
                self.selectRow(row)
                break

    def setup_selection_behavior(self):
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def setup_table(self):
        self.setColumnCount(8)
        self.setHorizontalHeaderLabels(
            ['Status', 'Title', 'Priority', 'Progress', 'Due Date', 'Labels', '', '']
        )
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setStyleSheet("""
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

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)

    def add_task_row(self, row, task, manager, status_callback, edit_callback, delete_callback):
        self.insertRow(row)

        status_button = self._create_status_button(task.completed)
        status_button.clicked.connect(lambda checked, tid=task.id: status_callback(tid))
        self.setCellWidget(row, 0, status_button)

        title_item = QTableWidgetItem(task.title)
        title_item.setData(Qt.UserRole, task.id)  # Сохраняем ID задачи здесь
        if task.description:
            title_item.setToolTip(f"Double-click to view details\n\n{task.description}")
        else:
            title_item.setToolTip("Double-click to view details")
        if task.completed:
            title_item.setForeground(QColor(100, 100, 100))
            font = title_item.font()
            font.setStrikeOut(True)
            title_item.setFont(font)
        self.setItem(row, 1, title_item)

        priority_widget = PriorityIndicatorWidget(task.priority)
        self.setCellWidget(row, 2, priority_widget)

        progress_bar = self._create_progress_bar(manager.get_task_progress(task.id))
        self.setCellWidget(row, 3, progress_bar)

        due_item = self._create_due_item(task.due_date, task.completed)
        self.setItem(row, 4, due_item)

        labels_widget = self._create_labels_widget(task.labels, manager)
        self.setCellWidget(row, 5, labels_widget)

        edit_button = self._create_edit_button()
        edit_button.clicked.connect(lambda checked, tid=task.id: edit_callback(tid))
        self.setCellWidget(row, 6, edit_button)

        delete_button = self._create_delete_button()
        delete_button.clicked.connect(lambda checked, tid=task.id: delete_callback(tid))
        self.setCellWidget(row, 7, delete_button)

    def _create_status_button(self, completed):
        button = QPushButton("✅" if completed else "⏳")
        button.setFixedSize(30, 30)
        if completed:
            button.setToolTip("Mark as Pending")
            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: 1px solid #2e7d32;
                    border-radius: 4px;
                    font-size: 14px;
                    color: #2e7d32;
                }
                QPushButton:hover {
                    background-color: rgba(46, 125, 50, 0.1);
                }
            """)
        else:
            button.setToolTip("Mark as Completed")
            button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: 2px solid #ff9800;
                    border-radius: 4px;
                    font-size: 14px;
                    color: #ff9800;
                }
                QPushButton:hover {
                    background-color: rgba(255, 152, 0, 0.1);
                }
            """)
        return button

    def _create_progress_bar(self, progress):
        progress_bar = QProgressBar()
        progress_bar.setValue(int(progress))
        progress_bar.setTextVisible(True)
        progress_bar.setFormat(f"{progress:.1f}%")
        progress_bar.setFixedHeight(20)
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #444;
                border-radius: 3px;
                text-align: center;
                font-size: 10px;
            }
            QProgressBar::chunk {
                background-color: #2a82da;
                border-radius: 3px;
            }
        """)
        return progress_bar

    def _create_due_item(self, due_date, completed):
        due_text = due_date if due_date else "No due date"
        item = QTableWidgetItem(due_text)
        item.setTextAlignment(Qt.AlignCenter)

        if due_date and not completed:
            try:
                due_date_obj = datetime.fromisoformat(due_date).date()
                if due_date_obj < datetime.now().date():
                    item.setForeground(QColor(255, 100, 100))
            except:
                pass

        return item

    def _create_labels_widget(self, label_ids, manager):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)

        for label_id in label_ids:
            label = manager.get_label(label_id)
            if label:
                label_widget = LabelWidget(label.name, label.color, label.text_color)
                label_widget.setMinimumHeight(24)
                label_widget.setMinimumWidth(60)
                layout.addWidget(label_widget)

        layout.addStretch()
        return widget

    def _create_edit_button(self):
        button = QPushButton("✏️")
        button.setFixedSize(30, 30)
        button.setToolTip("Edit Task")
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #ff9800;
                border-radius: 4px;
                font-size: 14px;
                color: #ff9800;
            }
            QPushButton:hover {
                background-color: rgba(255, 152, 0, 0.1);
            }
        """)
        return button

    def _create_delete_button(self):
        button = QPushButton("🗑️")
        button.setFixedSize(30, 30)
        button.setToolTip("Delete Task")
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #e74c3c;
                border-radius: 4px;
                font-size: 14px;
                color: #e74c3c;
            }
            QPushButton:hover {
                background-color: rgba(231, 76, 60, 0.1);
            }
        """)
        return button
