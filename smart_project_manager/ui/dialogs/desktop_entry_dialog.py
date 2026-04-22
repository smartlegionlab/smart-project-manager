# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
import os
import sys
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QMessageBox,
    QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from smart_project_manager import __version__ as ver


class DesktopEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Create Desktop Entry")
        self.setMinimumWidth(550)
        self.setModal(True)

        self.app_name = "Smart Projects Manager"
        self.app_executable = sys.executable
        self.app_path = os.path.abspath(sys.argv[0])
        self.icon_path = self.find_icon_path()

        self.setup_ui()
        self.center_dialog()

    def find_icon_path(self):
        possible_paths = [
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data", "icons", "icon.png"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "icons", "icon.png"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "icons", "icon.png"),
            os.path.join(os.path.dirname(__file__), "..", "..", "data", "icons", "icon.png"),
            os.path.join(os.path.dirname(sys.argv[0]), "data", "icons", "icon.png"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path
        return ""

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title_label = QLabel("Create Desktop Entry")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2a82da; margin: 10px;")
        layout.addWidget(title_label)

        info_group = QGroupBox("Application Information")
        info_layout = QVBoxLayout(info_group)

        info_text = QLabel(
            f"<b>Name:</b> {self.app_name}<br>"
            f"<b>Application Path:</b> {self.app_path}<br>"
            f"<b>Icon:</b> {self.icon_path if self.icon_path else 'Not found'}"
        )
        info_text.setTextFormat(Qt.RichText)
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)

        layout.addWidget(info_group)

        options_group = QGroupBox("Create shortcuts in:")
        options_layout = QVBoxLayout(options_group)

        self.app_menu_checkbox = QCheckBox("Application Menu (~/.local/share/applications/)")
        self.app_menu_checkbox.setChecked(True)
        options_layout.addWidget(self.app_menu_checkbox)

        self.desktop_checkbox = QCheckBox("Desktop (~/Desktop/)")
        self.desktop_checkbox.setChecked(False)
        options_layout.addWidget(self.desktop_checkbox)

        layout.addWidget(options_group)

        note_label = QLabel(
            "📌 <b>Note:</b> After creation, you may need to log out and back in "
            "or restart your desktop for the entry to appear in the menu."
        )
        note_label.setTextFormat(Qt.RichText)
        note_label.setWordWrap(True)
        note_label.setStyleSheet("color: #0d47a1; background-color: #e3f2fd; padding: 8px; border-radius: 5px;")
        layout.addWidget(note_label)

        button_layout = QHBoxLayout()

        self.create_btn = QPushButton("Create Entry")
        self.create_btn.setMinimumHeight(40)
        self.create_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1a72ca;
            }
        """)
        self.create_btn.clicked.connect(self.create_desktop_entry)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(self.create_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)

    def center_dialog(self):
        if self.parent:
            x = self.parent.x() + (self.parent.width() - self.width()) // 2
            y = self.parent.y() + (self.parent.height() - self.height()) // 2
            self.move(x, y)

    def create_desktop_entry(self):

        created_files = []
        errors = []

        if self.app_menu_checkbox.isChecked():
            success, message = self.create_app_menu_entry()
            if success:
                created_files.append(message)
            else:
                errors.append(message)

        if self.desktop_checkbox.isChecked():
            success, message = self.create_desktop_shortcut()
            if success:
                created_files.append(message)
            else:
                errors.append(message)

        if created_files and not errors:
            QMessageBox.information(
                self,
                "Success",
                f"✅ Desktop entry created successfully!\n\n"
                f"Created:\n" + "\n".join(f"• {f}" for f in created_files)
            )
            self.accept()
        elif created_files and errors:
            QMessageBox.warning(
                self,
                "Partial Success",
                f"⚠️ Some entries were created with issues:\n\n"
                f"✅ Created:\n" + "\n".join(f"• {f}" for f in created_files) +
                f"\n\n❌ Errors:\n" + "\n".join(f"• {e}" for e in errors)
            )
            self.accept()
        elif errors:
            QMessageBox.critical(
                self,
                "Error",
                f"❌ Failed to create desktop entries:\n\n" + "\n".join(f"• {e}" for e in errors)
            )

    def create_app_menu_entry(self):
        try:
            desktop_dir = os.path.expanduser("~/.local/share/applications")
            os.makedirs(desktop_dir, exist_ok=True)

            desktop_file = os.path.join(desktop_dir, "smart-projects-manager.desktop")

            content = self.generate_desktop_content()

            with open(desktop_file, 'w', encoding='utf-8') as f:
                f.write(content)

            os.chmod(desktop_file, 0o755)

            return True, desktop_file

        except Exception as e:
            return False, str(e)

    def create_desktop_shortcut(self):
        try:
            desktop_dir = os.path.expanduser("~/Desktop")
            os.makedirs(desktop_dir, exist_ok=True)

            desktop_file = os.path.join(desktop_dir, "smart-projects-manager.desktop")

            content = self.generate_desktop_content()

            with open(desktop_file, 'w', encoding='utf-8') as f:
                f.write(content)

            os.chmod(desktop_file, 0o755)

            return True, desktop_file

        except Exception as e:
            return False, str(e)

    def generate_desktop_content(self):
        python_exec = sys.executable

        exec_line = f'"{python_exec}" "{self.app_path}"'

        content = f"""[Desktop Entry]
Version={ver}
Type=Application
Name={self.app_name}
Comment=Is a desktop application for comprehensive project and task management, built with Python and PyQt5.
Exec={exec_line}
Icon={self.icon_path if self.icon_path else 'system-run'}
Terminal=false
Categories=Utility;
StartupNotify=true
Keywords=manager;projects;
"""
        return content
