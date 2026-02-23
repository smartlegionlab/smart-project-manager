# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QProgressBar,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QAbstractItemView,
    QLabel, QVBoxLayout
)
from PyQt5.QtGui import QColor, QDrag, QFont, QBrush, QPen, QPainter, QPixmap
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QPoint, QRect
from datetime import datetime

from smart_project_manager.ui.widgets.priority_widget import PriorityIndicatorWidget
from smart_project_manager.ui.widgets.label_widget import LabelWidget


class TaskTableWidget(QTableWidget):
    task_dropped = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_selection_behavior()
        self.setup_table()
        self.setFocusPolicy(Qt.NoFocus)
        self.selected_task_id = None
        self.manager = None
        self.current_project_id = None

        self.drag_indicator_rect = None
        self.drag_item_data = None
        self.setMouseTracking(True)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setDragDropOverwriteMode(False)

        self.task_order = []

        self.itemSelectionChanged.connect(self.save_selection)

    def save_selection(self):
        selected = self.selectedItems()
        if selected:
            row = selected[0].row()
            item = self.item(row, 2)
            if item:
                self.selected_task_id = item.data(Qt.UserRole)

    def restore_selection(self):
        if not self.selected_task_id:
            return

        for row in range(self.rowCount()):
            item = self.item(row, 2)
            if item and item.data(Qt.UserRole) == self.selected_task_id:
                self.selectRow(row)
                break

    def setup_selection_behavior(self):
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def setup_table(self):
        self.setColumnCount(9)
        self.setHorizontalHeaderLabels(
            ['', 'Status', 'Title', 'Priority', 'Progress', 'Due Date', 'Labels', '', '']
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
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)

        self.setSortingEnabled(True)

    def create_drag_handle(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        handle_container = QWidget()
        handle_layout = QVBoxLayout(handle_container)
        handle_layout.setContentsMargins(0, 0, 0, 0)
        handle_layout.setSpacing(3)

        for _ in range(2):
            line = QLabel("—")
            line.setStyleSheet("""
                QLabel {
                    color: #888;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 0px;
                    margin: -3px 0px;
                }
            """)
            line.setFont(QFont("Arial", 14))
            line.setAlignment(Qt.AlignCenter)
            handle_layout.addWidget(line)

        layout.addWidget(handle_container)

        widget.setProperty("is_drag_handle", True)

        return widget

    def add_task_row(self, row, task, manager, status_callback, edit_callback, delete_callback):
        self.insertRow(row)
        self.setRowHeight(row, 40)

        drag_handle = self.create_drag_handle()
        self.setCellWidget(row, 0, drag_handle)

        status_button = self._create_status_button(task.completed)
        status_button.clicked.connect(lambda checked, tid=task.id: status_callback(tid))
        self.setCellWidget(row, 1, status_button)

        title_item = QTableWidgetItem(task.title)
        title_item.setData(Qt.UserRole, task.id)
        title_item.setData(Qt.UserRole + 1, task.priority)
        if task.description:
            title_item.setToolTip(f"Double-click to view details\n\n{task.description}")
        else:
            title_item.setToolTip("Double-click to view details")
        if task.completed:
            title_item.setForeground(QColor(100, 100, 100))
            font = title_item.font()
            font.setStrikeOut(True)
            title_item.setFont(font)
        self.setItem(row, 2, title_item)

        priority_widget = PriorityIndicatorWidget(task.priority)
        self.setCellWidget(row, 3, priority_widget)

        progress_bar = self._create_progress_bar(manager.get_task_progress(task.id))
        self.setCellWidget(row, 4, progress_bar)

        due_item = self._create_due_item(task.due_date, task.completed)
        due_item.setData(Qt.UserRole, task.id)
        self.setItem(row, 5, due_item)

        labels_widget = self._create_labels_widget(task.labels, manager)
        self.setCellWidget(row, 6, labels_widget)

        edit_button = self._create_edit_button()
        edit_button.clicked.connect(lambda checked, tid=task.id: edit_callback(tid))
        self.setCellWidget(row, 7, edit_button)

        delete_button = self._create_delete_button()
        delete_button.clicked.connect(lambda checked, tid=task.id: delete_callback(tid))
        self.setCellWidget(row, 8, delete_button)

        self.update_task_order()

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

    def update_task_order(self):
        self.task_order = []
        for row in range(self.rowCount()):
            item = self.item(row, 2)
            if item:
                task_id = item.data(Qt.UserRole)
                if task_id:
                    self.task_order.append(task_id)

    def get_task_order(self):
        self.update_task_order()
        return self.task_order

    def _move_row(self, from_row, to_row):
        if from_row == to_row:
            return

        item = self.item(from_row, 2)
        if not item:
            return
        task_id = item.data(Qt.UserRole)

        main_window = self.get_main_window()
        if not main_window:
            return

        self.setSortingEnabled(False)

        row_items = {}
        for col in range(self.columnCount()):
            if col in [0, 1, 3, 4, 6, 7, 8]:
                row_items[col] = ('widget', None)
            else:
                item = self.item(from_row, col)
                if item:
                    new_item = QTableWidgetItem(item.text())
                    if col == 2:
                        new_item.setData(Qt.UserRole, item.data(Qt.UserRole))
                        new_item.setData(Qt.UserRole + 1, item.data(Qt.UserRole + 1))
                        new_item.setToolTip(item.toolTip())
                        if item.foreground().color() != Qt.black:
                            new_item.setForeground(item.foreground())
                        font = item.font()
                        new_item.setFont(font)
                    elif col == 5:
                        new_item.setTextAlignment(item.textAlignment())
                        if item.foreground().color() != Qt.black:
                            new_item.setForeground(item.foreground())
                    row_items[col] = ('item', new_item)

        self.removeRow(from_row)

        if to_row > from_row:
            insert_pos = to_row
        else:
            insert_pos = to_row

        self.insertRow(insert_pos)
        self.setRowHeight(insert_pos, 40)

        for col, (data_type, value) in row_items.items():
            if data_type == 'item' and value:
                self.setItem(insert_pos, col, value)

        if self.current_project_id and task_id:
            task = main_window.manager.get_task(task_id)
            if task:
                drag_handle = self.create_drag_handle()
                self.setCellWidget(insert_pos, 0, drag_handle)

                status_button = self._create_status_button(task.completed)
                status_button.clicked.connect(lambda checked, tid=task_id: main_window.toggle_task_status(tid))
                self.setCellWidget(insert_pos, 1, status_button)

                priority_widget = PriorityIndicatorWidget(task.priority)
                self.setCellWidget(insert_pos, 3, priority_widget)

                progress = main_window.manager.get_task_progress(task_id)
                progress_bar = self._create_progress_bar(progress)
                self.setCellWidget(insert_pos, 4, progress_bar)

                labels_widget = self._create_labels_widget(task.labels, main_window.manager)
                self.setCellWidget(insert_pos, 6, labels_widget)

                edit_button = self._create_edit_button()
                edit_button.clicked.connect(lambda checked, tid=task_id: main_window.edit_task(tid))
                self.setCellWidget(insert_pos, 7, edit_button)

                delete_button = self._create_delete_button()
                delete_button.clicked.connect(lambda checked, tid=task_id: main_window.delete_task(tid))
                self.setCellWidget(insert_pos, 8, delete_button)

        self.setSortingEnabled(True)

    def startDrag(self, supportedActions):
        selected = self.selectedItems()
        if not selected:
            return

        row = selected[0].row()
        item = self.item(row, 2)
        if not item:
            return

        task_id = item.data(Qt.UserRole)
        task_title = item.text()

        self.drag_item_data = {
            'row': row,
            'id': task_id,
            'title': task_title
        }

        pixmap = self.create_drag_preview(row)

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(str(task_id))
        mime_data.setData("application/x-task-id", str(task_id).encode())
        mime_data.setData("application/x-source-row", str(row).encode())

        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))

        drag.exec_(Qt.MoveAction)

        self.drag_item_data = None
        self.drag_indicator_rect = None
        self.viewport().update()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-task-id"):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if not event.mimeData().hasFormat("application/x-task-id"):
            event.ignore()
            return

        drop_pos = event.pos()
        target_row = self.rowAt(drop_pos.y())

        if target_row >= 0:
            rect = self.visualRect(self.model().index(target_row, 0))
            insert_above = drop_pos.y() < rect.center().y()

            y_pos = rect.top() if insert_above else rect.bottom()
            self.drag_indicator_rect = QRect(rect.left(), y_pos - 2, rect.width(), 4)
        else:
            last_row = self.rowCount() - 1
            if last_row >= 0:
                rect = self.visualRect(self.model().index(last_row, 0))
                self.drag_indicator_rect = QRect(rect.left(), rect.bottom() - 2, rect.width(), 4)
            else:
                self.drag_indicator_rect = QRect(10, 10, self.width() - 20, 4)

        self.viewport().update()
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.drag_indicator_rect = None
        self.viewport().update()
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        if not event.mimeData().hasFormat("application/x-task-id"):
            event.ignore()
            return

        task_id = event.mimeData().text()
        drop_pos = event.pos()
        target_row = self.rowAt(drop_pos.y())

        if target_row < 0 or target_row >= self.rowCount():
            target_row = self.rowCount()

        if target_row < self.rowCount():
            rect = self.visualRect(self.model().index(target_row, 0))
            insert_above = drop_pos.y() < rect.center().y()
            if not insert_above:
                target_row += 1

        source_row = -1
        for row in range(self.rowCount()):
            item = self.item(row, 2)
            if item and str(item.data(Qt.UserRole)) == task_id:
                source_row = row
                break

        if source_row >= 0 and source_row != target_row:
            if source_row < target_row:
                target_row -= 1

            scroll_pos = self.verticalScrollBar().value()

            main_window = self.get_main_window()
            if main_window:
                self.current_project_id = main_window.current_project_id

            self._move_row(source_row, target_row)
            self.update_task_order()
            self.task_dropped.emit(source_row, target_row)

            self.verticalScrollBar().setValue(scroll_pos)
            self.selectRow(target_row)

        self.drag_indicator_rect = None
        self.viewport().update()
        event.acceptProposedAction()

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.drag_indicator_rect:
            painter = QPainter(self.viewport())
            painter.setRenderHint(QPainter.Antialiasing)

            painter.setPen(QPen(QColor(100, 200, 255), 3))
            painter.drawLine(
                self.drag_indicator_rect.left() + 5,
                self.drag_indicator_rect.center().y(),
                self.drag_indicator_rect.right() - 5,
                self.drag_indicator_rect.center().y()
            )

            painter.setBrush(QBrush(QColor(100, 200, 255)))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(
                self.drag_indicator_rect.left(),
                self.drag_indicator_rect.center().y() - 4,
                8, 8
            )
            painter.drawEllipse(
                self.drag_indicator_rect.right() - 8,
                self.drag_indicator_rect.center().y() - 4,
                8, 8
            )

    def create_drag_preview(self, row):
        width = self.columnWidth(2) + self.columnWidth(3) + 40
        height = 40

        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(QColor(70, 130, 180, 200)))
        painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
        painter.drawRoundedRect(0, 0, width - 1, height - 1, 5, 5)

        title_item = self.item(row, 2)

        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        title_text = title_item.text() if title_item else "Task"
        if len(title_text) > 30:
            title_text = title_text[:27] + "..."
        painter.drawText(10, 5, width - 20, 30, Qt.AlignLeft | Qt.AlignVCenter, title_text)

        if title_item:
            priority = title_item.data(Qt.UserRole + 1)
            if priority == 'high':
                priority_color = QColor(255, 100, 100)
            elif priority == 'medium':
                priority_color = QColor(255, 200, 100)
            elif priority == 'low':
                priority_color = QColor(100, 200, 100)
            else:
                priority_color = QColor(150, 150, 150)

            painter.setBrush(QBrush(priority_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(width - 30, 12, 16, 16)

        painter.end()
        return pixmap

    def get_main_window(self):
        parent = self.parent()
        while parent:
            if hasattr(parent, 'current_project_id') and hasattr(parent, 'manager'):
                return parent
            parent = parent.parent()
        return None
