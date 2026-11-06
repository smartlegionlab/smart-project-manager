# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont


class PanelHeader(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setFixedHeight(28)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 0, 2, 0)
        layout.setSpacing(8)

        self.title_label = QLabel(title)
        font = QFont("Arial", 10)
        font.setBold(True)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.2)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color: #7f8794;")

        layout.addWidget(self.title_label)
        layout.addStretch()

    def add_widget(self, widget):
        self.layout().addWidget(widget)

    def set_title(self, title: str):
        self.title_label.setText(title)

    def set_title_with_count(self, title: str, count: int):
        self.title_label.setText(f"{title} ({count})")

    def set_title_plain(self, title: str):
        self.title_label.setText(title)
