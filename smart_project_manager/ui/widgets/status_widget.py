# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QRect


class StatusWidget(QWidget):

    def __init__(self, completed: bool, parent=None):
        super().__init__(parent)
        self.completed = completed
        self.setFixedSize(90, 26)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.completed:
            painter.setBrush(QBrush(QColor("#2e7d32")))
            painter.setPen(QPen(QColor("#1b5e20"), 1))
            painter.drawRoundedRect(0, 0, 90, 26, 5, 5)

            painter.setPen(QPen(Qt.white))
            painter.setFont(QFont("Arial", 9, QFont.Bold))
            painter.drawText(QRect(0, 0, 90, 26), Qt.AlignCenter, "✅ Done")
        else:
            painter.setBrush(QBrush(QColor("#ff9800")))
            painter.setPen(QPen(QColor("#e65100"), 1))
            painter.drawRoundedRect(0, 0, 90, 26, 5, 5)

            painter.setPen(QPen(Qt.white))
            painter.setFont(QFont("Arial", 9, QFont.Bold))
            painter.drawText(QRect(0, 0, 90, 26), Qt.AlignCenter, "⏳ Pending")
