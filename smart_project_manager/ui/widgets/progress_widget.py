# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QProgressBar
from PyQt5.QtCore import Qt


class ProgressWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("Progress: 0%")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-weight: bold; color: #fff;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #444;
                border-radius: 3px;
                background-color: #2a2a2a;
            }
            QProgressBar::chunk {
                background-color: #2a82da;
                border-radius: 3px;
            }
        """)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progress_bar)

    def set_progress(self, value: float):
        self.progress_bar.setValue(int(value))
        self.label.setText(f"Progress: {value:.1f}%")
