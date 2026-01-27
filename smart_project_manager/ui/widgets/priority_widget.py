# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen


class PriorityIndicatorWidget(QWidget):

    def __init__(self, priority: int, parent=None):
        super().__init__(parent)
        self.priority = priority

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(6)

        self.indicator = PriorityIndicator(priority)
        layout.addWidget(self.indicator)

        priority_text = ["High", "Medium", "Low"][priority - 1]
        self.text_label = QLabel(priority_text)
        self.text_label.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
        layout.addWidget(self.text_label)

        self.setFixedSize(90, 26)


class PriorityIndicator(QWidget):

    def __init__(self, priority: int, parent=None):
        super().__init__(parent)
        self.priority = priority
        self.setFixedSize(14, 14)

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
        painter.drawEllipse(2, 2, 10, 10)