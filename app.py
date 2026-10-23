# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

from smart_project_manager.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    app.setStyle('Fusion')

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(24, 26, 30))
    dark_palette.setColor(QPalette.WindowText, QColor(220, 220, 230))
    dark_palette.setColor(QPalette.Base, QColor(30, 32, 38))
    dark_palette.setColor(QPalette.AlternateBase, QColor(36, 38, 44))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(45, 48, 56))
    dark_palette.setColor(QPalette.ToolTipText, QColor(220, 220, 230))
    dark_palette.setColor(QPalette.Text, QColor(220, 220, 230))
    dark_palette.setColor(QPalette.Button, QColor(45, 48, 56))
    dark_palette.setColor(QPalette.ButtonText, QColor(220, 220, 230))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 80, 80))
    dark_palette.setColor(QPalette.Link, QColor(0, 122, 204))
    dark_palette.setColor(QPalette.Highlight, QColor(0, 122, 204))
    dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(130, 130, 140))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(130, 130, 140))

    app.setPalette(dark_palette)

    window = MainWindow()
    window.showMaximized()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
