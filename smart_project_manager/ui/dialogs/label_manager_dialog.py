# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, QSize

from smart_project_manager.ui.dialogs.label_dialog import LabelDialog
from smart_project_manager.ui.widgets.label_widget import LabelWidget


class LabelManagerDialog(QDialog):
    label_selected = pyqtSignal(str)

    def __init__(self, parent=None, manager=None):
        super().__init__(parent)
        self.manager = manager

        self.setWindowTitle('📝 Label Manager')
        self.setMinimumSize(600, 700)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(15, 15, 15, 15)

        header_label = QLabel('📝 Label Manager')
        header_label.setFont(QFont("Arial", 18, QFont.Bold))
        header_label.setStyleSheet("color: #2a82da;")
        self.layout.addWidget(header_label)

        self.btn_new_label = QPushButton('+ Create New Label')
        self.btn_new_label.clicked.connect(self.create_label)
        self.btn_new_label.setFixedHeight(40)
        self.btn_new_label.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        self.layout.addWidget(self.btn_new_label)

        info_label = QLabel(f'Total labels: {len(self.manager.get_all_labels())}')
        info_label.setStyleSheet("color: #888; font-size: 12px;")
        self.layout.addWidget(info_label)

        self.labels_list = QListWidget()
        self.labels_list.itemDoubleClicked.connect(self.select_label)
        self.labels_list.setStyleSheet("""
            QListWidget {
                background-color: #2a2a2a;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 5px;
            }
            QListWidget::item {
                background-color: #353535;
                border-radius: 5px;
                margin: 1px;
                padding: 10px;
            }
            QListWidget::item:hover {
                background-color: #3a3a3a;
            }
            QListWidget::item:selected {
                background-color: rgba(42, 130, 218, 90);
                color: white;
                border: 1px solid #2a82da;
            }
        """)
        self.layout.addWidget(self.labels_list)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.btn_edit = QPushButton('✏️ Edit')
        self.btn_edit.clicked.connect(self.edit_label)
        self.btn_edit.setEnabled(False)
        self.btn_edit.setFixedSize(80, 35)
        self.btn_edit.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #e68900;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        button_layout.addWidget(self.btn_edit)

        self.btn_delete = QPushButton('🗑️ Delete')
        self.btn_delete.clicked.connect(self.delete_label)
        self.btn_delete.setEnabled(False)
        self.btn_delete.setFixedSize(80, 35)
        self.btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        button_layout.addWidget(self.btn_delete)

        self.btn_select = QPushButton('✓ Select')
        self.btn_select.clicked.connect(self.select_current_label)
        self.btn_select.setEnabled(False)
        self.btn_select.setFixedSize(100, 35)
        self.btn_select.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover:enabled {
                background-color: #219653;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        button_layout.addWidget(self.btn_select)

        button_layout.addStretch()

        self.btn_close = QPushButton('Close')
        self.btn_close.clicked.connect(self.accept)
        self.btn_close.setFixedSize(100, 35)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        button_layout.addWidget(self.btn_close)

        self.layout.addLayout(button_layout)

        self.labels_list.itemSelectionChanged.connect(self.on_selection_changed)

        self.load_labels()

    def load_labels(self):
        self.labels_list.clear()
        labels = self.manager.get_all_labels()

        for label in labels:
            item = QListWidgetItem()
            item.setSizeHint(QSize(0, 70))

            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(15)

            text_color = label.text_color if hasattr(label, 'text_color') and label.text_color else "#ffffff"
            label_widget = LabelWidget(label.name, label.color, text_color)
            label_widget.setMinimumHeight(40)
            label_widget.setMinimumWidth(120)
            layout.addWidget(label_widget)

            if label.description:
                desc_label = QLabel(label.description)
                desc_label.setStyleSheet("color: #aaa; font-size: 12px;")
                desc_label.setWordWrap(True)
                layout.addWidget(desc_label, 1)

            color_code = QLabel(f"Color: {label.color}")
            color_code.setStyleSheet("color: #888; font-size: 11px; font-family: monospace;")
            layout.addWidget(color_code)

            text_color_code = QLabel(f"Text: {text_color}")
            text_color_code.setStyleSheet("color: #888; font-size: 11px; font-family: monospace;")
            layout.addWidget(text_color_code)

            layout.addStretch()

            self.labels_list.addItem(item)
            self.labels_list.setItemWidget(item, widget)
            item.label_id = label.id

    def on_selection_changed(self):
        has_selection = len(self.labels_list.selectedItems()) > 0
        self.btn_edit.setEnabled(has_selection)
        self.btn_delete.setEnabled(has_selection)
        self.btn_select.setEnabled(has_selection)

    def create_label(self):
        dialog = LabelDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_label_data()

            if not data['name']:
                QMessageBox.warning(self, 'Error', 'Label name is required')
                return

            self.manager.create_label(**data)
            self.load_labels()

    def edit_label(self):
        items = self.labels_list.selectedItems()
        if not items:
            return

        item = items[0]
        label = self.manager.get_label(item.label_id)
        if not label:
            return

        dialog = LabelDialog(self, label)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_label_data()

            if not data['name']:
                QMessageBox.warning(self, 'Error', 'Label name is required')
                return

            self.manager.update_label(label.id, **data)
            self.load_labels()

    def delete_label(self):
        items = self.labels_list.selectedItems()
        if not items:
            return

        item = items[0]
        label = self.manager.get_label(item.label_id)
        if not label:
            return

        reply = QMessageBox.question(
            self,
            'Confirm Delete',
            f'Delete label "{label.name}"?\nThis will remove it from all projects, tasks, and subtasks.',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.manager.delete_label(label.id)
            self.load_labels()

    def select_current_label(self):
        items = self.labels_list.selectedItems()
        if not items:
            return

        item = items[0]
        self.label_selected.emit(item.label_id)
        self.accept()

    def select_label(self, item):
        self.label_selected.emit(item.label_id)
        self.accept()
