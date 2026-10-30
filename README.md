# Smart Project Manager <sup>v1.1.2</sup>

---

## Overview

**Smart Project Manager** is a desktop application for comprehensive project and task management, built with Python and PyQt5. It provides a hierarchical system for organizing projects, tasks, and subtasks, featuring visual labels, automatic progress tracking, and a dark-themed user interface.

*   **Author:** Alexander Suvorov
*   **GitHub:** [smartlegionlab](https://github.com/smartlegionlab)

---

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/smartlegionlab/smart-project-manager)](https://github.com/smartlegionlab/smart-project-manager/)
![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smart-project-manager)
[![GitHub](https://img.shields.io/github/license/smartlegionlab/smart-project-manager)](https://github.com/smartlegionlab/smart-project-manager/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/smart-project-manager?style=social)](https://github.com/smartlegionlab/smart-project-manager/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/smart-project-manager?style=social)](https://github.com/smartlegionlab/smart-project-manager/network/members)

---

## Disclaimer

**By using this software, you agree to the full disclaimer terms.**

**Summary:** Software provided "AS IS" without warranty. You assume all risks.

**Full legal disclaimer:** See [DISCLAIMER.md](https://github.com/smartlegionlab/smart-project-manager/blob/master/DISCLAIMER.md)

---

## Features

### Tab-Based Project Manager
*   Projects open as tabs on the right side, one tab per project
*   Multiple projects can be open at the same time
*   Close a project tab without deleting the project - it stays in the tree on the left
*   Tasks open as nested tabs below the task list, one tab per task
*   Multiple tasks can be open at the same time inside one project

### Project Management
*   Create, edit and delete projects with name and description
*   Hierarchical structure: **Projects -> Tasks -> Subtasks**
*   Automatic progress calculation per project based on task completion

### Task & Subtask System
*   Tasks with title, description, priority (High/Medium/Low) and optional due date
*   Subtasks with the same fields, nested inside tasks
*   Automatic completion logic: when all subtasks are completed, the parent task is marked complete
*   Toggle completion status for tasks and subtasks directly from the UI
*   Drag and drop task rows to reorder them

### Label System
*   Custom labels with name, color, text color and description
*   Assign labels to tasks and subtasks for categorization and filtering
*   Dedicated Label Manager dialog for creating, editing and deleting labels

### Progress Tracking & Statistics
*   Visual progress bars for tasks, subtasks and overall projects
*   Global statistics panel with counts and completion rates
*   Per-project progress panel with task/subtask counts and last update time

### User Interface
*   Dark theme optimized for extended use
*   Two-panel layout: project tree on the left, tabs and task details on the right
*   Context menus for quick task actions (view, edit, mark complete, delete)
*   Search and filters by priority, label and completion status
*   Built-in Keyboard Shortcuts dialog accessible from Help menu or `Ctrl+/`

### Data Persistence
*   Automatic saving to `~/.smart_project_manager/projects.json`
*   JSON-based storage for projects, tasks, subtasks and labels
*   Data loaded automatically on application startup
*   Manual backups and automatic cleanup of backups older than 30 days

---

## Requirements

*   Python 3.7 or higher
*   Git (only for the installer)
*   curl (only for the installer)
*   PyQt5

---

## Installation

There are **two independent ways** to use this application:

*   **Run from source** - clone the repo, create a virtual environment, launch manually. Nothing is installed system-wide.
*   **Install system-wide** - one command creates a menu entry. Desktop shortcut is opt-in.

Choose one. They are not meant to be combined.

### Option 1 - Run from Source (no system install)

Use this if you just want to try the app or run it manually from a folder.

```bash
# 1. Clone the repository
git clone https://github.com/smartlegionlab/smart-project-manager.git
cd smart-project-manager

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Launch the app
python app.py
```

To run it again later:

```bash
cd smart-project-manager
source venv/bin/activate
python app.py
```

Nothing is installed system-wide. The app runs from this folder.

### Option 2 - Install System-Wide (recommended)

Use this if you want the app in your application menu.

#### One-command install

```bash
curl -fsSL https://raw.githubusercontent.com/smartlegionlab/smart-project-manager/master/install.sh | bash
```

**What the installer does:**

1. Downloads the source code from GitHub.
2. Installs the application to `~/.local/share/smart-project-manager/`.
   No root, no sudo - everything lives inside your home directory.
3. Creates a dedicated Python virtual environment at `~/.local/share/smart-project-manager/venv/` and installs dependencies into it.
4. Registers the app in your desktop environment by creating `~/.local/share/applications/smart-project-manager.desktop`.
5. Refreshes the desktop database so the menu entry appears without a full re-login on most systems.

**Launch after install:**
*   Application menu -> **Smart Project Manager**

**Desktop shortcut (opt-in):**

By default, no Desktop shortcut is created. This is intentional - on GNOME (default on Ubuntu), desktop icons are hidden by default, which would make a shortcut invisible and confusing.

To also create a Desktop shortcut during install, pass the `SPM_CREATE_DESKTOP_SHORTCUT=1` environment variable to **bash** - the second command in the pipeline:

```bash
curl -fsSL https://raw.githubusercontent.com/smartlegionlab/smart-project-manager/master/install.sh | SPM_CREATE_DESKTOP_SHORTCUT=1 bash
```

Or export it first, then run the normal installer:

```bash
export SPM_CREATE_DESKTOP_SHORTCUT=1
curl -fsSL https://raw.githubusercontent.com/smartlegionlab/smart-project-manager/master/install.sh | bash
```

> **Note:** Writing `SPM_CREATE_DESKTOP_SHORTCUT=1 curl ... | bash` does **not** work - in a shell pipeline, an environment variable prefix applies only to the command on the **left** side of the `|`. The variable never reaches `bash`, which is on the right side. Pass it to `bash` directly, or `export` it beforehand.

**Notes:**
*   On GNOME (default on Ubuntu), desktop icons may be hidden by default. Enable Desktop Icons in GNOME Tweaks to see the shortcut.
*   The Desktop shortcut may show an **"Unsecured Application Launcher"** warning. Right-click -> **Allow Launching** (one-time action).
*   If the menu entry does not appear immediately, log out and back in.

#### Alternative - install from a cloned repo

If you already cloned the repository, you can run the installer locally:

```bash
cd smart-project-manager
./install.sh
```

It works the same way. It ignores any local `venv/` and creates its own under `~/.local/share/smart-project-manager/venv/`.

### Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/smartlegionlab/smart-project-manager/master/uninstall.sh | bash
```

**What the uninstaller removes:**
*   `~/.local/share/smart-project-manager/` - the application and its venv
*   `~/.local/share/applications/smart-project-manager.desktop` - the menu entry
*   `~/Desktop/smart-project-manager.desktop` - the Desktop shortcut (if present)

**What the uninstaller never touches:**
*   `~/.smart_project_manager/projects.json` - your projects, tasks, subtasks and labels. It is your data. Only you decide what to do with it.

If you want to remove your data as well, run after uninstall:

```bash
rm -rf ~/.smart_project_manager
```

### Installation Paths

| Item                       | Path                                                              |
|----------------------------|-------------------------------------------------------------------|
| Application files          | `~/.local/share/smart-project-manager/`                           |
| Virtual environment        | `~/.local/share/smart-project-manager/venv/`                      |
| Application menu entry     | `~/.local/share/applications/smart-project-manager.desktop`       |
| Desktop shortcut (opt-in)  | `~/Desktop/smart-project-manager.desktop`                         |
| User data (projects)       | `~/.smart_project_manager/projects.json`                          |

---

## How to Use

### Getting Started
1.  **Create a project:** `File -> New Project` or the **+ New Project** button in the left panel.
2.  **Open a project:** click it in the tree on the left - it opens as a tab on the right.
3.  **Create a task:** with a project tab active, use `File -> New Task` or the **Add Task** button.
4.  **Open a task:** double-click a task row - its subtasks open as a nested tab below the task list.
5.  **Manage labels:** `Edit -> Manage Labels` to create, edit and delete labels.

### Working with Tabs

*   Each opened project has its own tab on the right. Switching between project tabs switches the whole working context.
*   Inside a project tab, double-clicking a task opens a subtask tab below the task table. Multiple subtask tabs can be open at the same time.
*   Closing a project tab does not delete the project - it stays in the tree on the left.
*   Closing a subtask tab does not delete the task - it stays in the task list.

### Tasks and Subtasks

*   Tasks and subtasks support title, description, priority, due date and labels.
*   Marking all subtasks complete auto-marks the parent task complete.
*   Drag task rows up or down to reorder them inside a project.
*   Right-click a task for quick actions: view details, open subtasks, mark complete/pending, edit, delete.

### Search and Filters

*   Type into the search box to filter tasks by title and description.
*   Filter by priority using the Priority dropdown.
*   Filter by label using the Label dropdown.
*   Toggle **Show Completed** to hide or show completed tasks.
*   Click **Reset** to clear all filters.

---

### Desktop Integration (Linux)

> **Note:** If you installed the app via `install.sh`, the application menu entry is already created automatically. The in-app option described below is useful when you run the app manually from a custom location, or when you want to add a Desktop shortcut on demand. It is also the recommended way for development: it creates a shortcut pointing to the **currently running instance** (your working copy), not to a copy under `~/.local/share/`.

**Creating Application Shortcuts:**

The application allows you to create desktop entries directly from the menu:

1. **Go to File -> Create Desktop Entry**
2. **Choose locations:**
   *   Application Menu (`~/.local/share/applications/`) - adds to system app menu
   *   Desktop (`~/Desktop/`) - creates shortcut on desktop
3. **Click "Create Entry"**

**What happens:**
*   Creates `.desktop` file(s) with proper configuration
*   Sets executable permissions automatically
*   Uses application icon if available

**After creation:**
*   **Application Menu**: log out and back in (or restart desktop) for the entry to appear
*   **Desktop shortcut**: may show "Unsecured Application Launcher" warning
    *   Right-click on shortcut -> "Allow Launching" or "Trust"
    *   This is a one-time security confirmation

**Note:** this feature is only available on Linux systems with desktop environments that support `.desktop` files (GNOME, KDE, XFCE, etc.).

---

### Keyboard Shortcuts

| Shortcut       | Action                     |
|----------------|----------------------------|
| `Ctrl+N`       | New Project                |
| `Ctrl+T`       | New Task                   |
| `Ctrl+B`       | Create Backup              |
| `Ctrl+I`       | Import                     |
| `Ctrl+Shift+E` | Export                     |
| `Ctrl+L`       | Manage Labels              |
| `F5`           | Refresh View               |
| `F1`           | Open Help                  |
| `Ctrl+/`       | Show Keyboard Shortcuts    |
| `Ctrl+A`       | Open About                 |
| `Ctrl+Q`       | Exit Application           |

---

## Data Storage

| Item           | Path                                                       |
|----------------|------------------------------------------------------------|
| Projects       | `~/.smart_project_manager/projects.json`                   |
| Backups        | `~/.smart_project_manager/backups/`                        |

Backups older than 30 days are cleaned up automatically on application startup. Manual cleanup is also available from `File -> Show Backups`.

---

## License

This project is licensed under the **BSD 3-Clause License**. See the [`LICENSE`](LICENSE) file in the project repository for full details.

---

**Copyright (c) 2026, Alexander Suvorov. All rights reserved.**

---

## Screenshot

![Smart Project Manager](https://github.com/smartlegionlab/smart-project-manager/blob/master/data/images/smart-project-manager.png)

