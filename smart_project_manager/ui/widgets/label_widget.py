# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QColor, QPainter, QFont
from PyQt5.QtCore import Qt, QRect


class LabelWidget(QWidget):

    def __init__(self, label_name: str, color: str, parent=None):
        super().__init__(parent)
        self.label_name = label_name
        self.color = QColor(color)
        self.setMinimumHeight(28)
        self.setMinimumWidth(60)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, width, height, 4, 4)

        painter.setPen(QColor(255, 255, 255, 50))
        painter.drawRoundedRect(0, 0, width, height, 4, 4)

        painter.setPen(Qt.white)
        font = QFont("Arial", 9)
        font.setBold(True)
        painter.setFont(font)

        text_rect = QRect(0, 0, width, height)
        painter.drawText(text_rect, Qt.AlignCenter, self.label_name)

    def set_label(self, label_name: str, color: str):
        self.label_name = label_name
        self.color = QColor(color)
        self.update()
