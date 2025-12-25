# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRect


class PriorityIndicatorWidget(QWidget):

    def __init__(self, priority: int, parent=None):
        super().__init__(parent)
        self.priority = priority
        self.setFixedSize(24, 24)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.priority == 1:
            color = QColor("#ff6b6b")
        elif self.priority == 2:
            color = QColor("#ffd166")
        else:
            color = QColor("#8ac926")

        painter.setBrush(QBrush(color))
        painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
        painter.drawEllipse(2, 2, 20, 20)

        painter.setPen(QPen(Qt.white))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(QRect(0, 0, 24, 24), Qt.AlignCenter, str(self.priority))
