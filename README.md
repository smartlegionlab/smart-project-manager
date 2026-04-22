# Smart Project Manager <sup>v1.0.6</sup>

---

## Overview

**Smart Project Manager** is a desktop application for comprehensive project and task management, 
built with Python and PyQt5. It provides a hierarchical system for organizing projects, 
tasks, and subtasks, featuring visual labels, automatic progress tracking, and a dark-themed user interface.

*   **Author:** Alexander Suvorov
*   **GitHub:** [smartlegionlab](https://github.com/smartlegionlab)

---

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/smartlegionlab/smart-project-manager)](https://github.com/smartlegionlab/smart-project-manager/)
![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smart-project-manager)
[![GitHub](https://img.shields.io/github/license/smartlegionlab/smart-project-manager)](https://github.com/smartlegionlab/smart-project-manager/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/smart-project-manager?style=social)](https://github.com/smartlegionlab/smart-project-manager/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/smart-project-manager?style=social)](https://github.com/smartlegionlab/smart-project-manager/network/members)

---

## ⚠️ Disclaimer

**By using this software, you agree to the full disclaimer terms.**

**Summary:** Software provided "AS IS" without warranty. You assume all risks.

**Full legal disclaimer:** See [DISCLAIMER.md](https://github.com/smartlegionlab/smart-project-manager/blob/master/DISCLAIMER.md)

---

## Features

### 1. Project Management
*   Create, edit, and delete projects with name, version, and description.
*   Hierarchical structure: **Projects → Tasks → Subtasks**.
*   Automatic progress calculation for each project based on task completion.

### 2. Task & Subtask System
*   Create tasks and subtasks with titles, descriptions, priorities (High/Medium/Low), and optional due dates.
*   Automatic completion logic: A task is marked as complete when all its subtasks are completed.
*   Toggle completion status for tasks and subtasks directly from the main interface.

### 3. Label System
*   Create custom labels with name, color, and description.
*   Assign labels to both tasks and subtasks for categorization and filtering.
*   Dedicated Label Manager dialog for creating, editing, and deleting labels.

### 4. Progress Tracking & Statistics
*   Visual progress bars for tasks, subtasks, and overall projects.
*   Real-time global statistics dashboard showing counts and completion rates for all entities.
*   Detailed project progress panel showing task/subtask counts and last update time.

### 5. User Interface
*   **Dark theme** optimized for extended use.
*   **Two-panel layout:** Project tree on the left, task table and details on the right.
*   Context menus for quick task actions (view, edit, mark complete, delete).
*   Interactive tables with buttons for editing, deleting, and toggling status.

### 6. Data Persistence
*   Automatic saving to `~/.smart_project_manager/projects.json`.
*   JSON-based storage for projects, tasks, subtasks, and labels.
*   Data is automatically loaded on application startup.

---

## Installation & Launch

### Prerequisites
*   Python 3.7 or higher
*   Required Python packages: `PyQt5`

### Steps
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/smartlegionlab/smart-project-manager.git
    cd smart-project-manager
    ```

2.  **Install Dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application:**
    Execute the main entry point:
    ```bash
    python app.py
    ```

---

## How to Use

### Getting Started
1.  **Create a Project:** Use `File → New Project` or the "New Project" button.
2.  **Select a Project:** Click on a project in the left panel to view and manage its tasks.
3.  **Create a Task:** With a project selected, use `File → New Task` or the "New Task" button.
4.  **Add Subtasks:** Edit a task and navigate to the "Subtasks" tab to add detailed steps.
5.  **Manage Labels:** Use `Edit → Manage Labels` to create and organize your label system.

---

### Desktop Integration (Linux)

**Creating Application Shortcuts:**

The application allows you to create desktop entries directly from the menu:

1. **Go to File → Create Desktop Entry**
2. **Choose locations:**
   - ✓ Application Menu (`~/.local/share/applications/`) - adds to system app menu
   - □ Desktop (`~/Desktop/`) - creates shortcut on desktop
3. **Click "Create Entry"**

**What happens:**
- Creates `.desktop` file(s) with proper configuration
- Sets executable permissions automatically
- Uses application icon if available

**After creation:**
- **Application Menu**: Log out and back in (or restart desktop) for entry to appear
- **Desktop shortcut**: May show "Unsecured Application Launcher" warning
  - Right-click on shortcut → "Allow Launching" or "Trust"
  - This is a one-time security confirmation

**Note:** This feature is only available on Linux systems with desktop environments that support `.desktop` files (GNOME, KDE, XFCE, etc.).

---

### Keyboard Shortcuts
*   `Ctrl+N`: New Project
*   `Ctrl+T`: New Task
*   `Ctrl+B`: Create BackUp
*   `Ctrl+I`: Import
*   `Ctrl+Shift+E`: Export
*   `Ctrl+E`: Edit Selected Project
*   `Ctrl+D`: Delete Selected Project
*   `Ctrl+L`: Manage Labels
*   `F5`: Refresh View
*   `F1`: Open Help
*   `Ctrl+Q`: Exit Application

---

## License

This project is licensed under the **BSD 3-Clause License**. See the [`LICENSE`](LICENSE) file in the project 
repository for full details.

---

## Future Development Roadmap

The following features are identified in the code as future implementation targets:

### **Planned Features**
    
*   **Task Filtering System** - The "Show Completed Tasks" toggle in the `View` menu is implemented as a placeholder. Future implementation will:
    *   Enable filtering of completed vs. pending tasks in the task table
    *   Provide additional filtering options (by priority, due date, labels, etc.)
    *   Persist filter settings between sessions

---

**Copyright (©) 2026, Alexander Suvorov. All rights reserved.**

---

## Screenshot

![Smart Project Manager Logo](https://github.com/smartlegionlab/smart-project-manager/blob/master/data/images/smart-project-manager.png)