from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


class ProjectsTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_tree()

    def setup_tree(self):
        self.setHeaderLabel('Projects')
        self.setStyleSheet("""
            QTreeWidget {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 5px;
            }
            QTreeWidget::item {
                padding: 8px 5px;
                border-bottom: 1px solid #333;
            }
            QTreeWidget::item:selected {
                background-color: #2a82da;
                color: white;
            }
            QTreeWidget::item:hover:!selected {
                background-color: #3a3a3a;
            }
        """)

    def add_project(self, project, manager):
        item = QTreeWidgetItem(self)
        item.setText(0, f"{project.name} v{project.version}")
        item.project_id = project.id

        task_count = len(project.tasks)
        completed_tasks = sum(1 for task_id in project.tasks
                             if manager.get_task(task_id) and
                             manager.get_task(task_id).completed)

        progress_text = f" ({completed_tasks}/{task_count})"
        item.setText(0, f"{project.name} v{project.version}{progress_text}")

        if project.description:
            item.setToolTip(0, project.description)

        return item
