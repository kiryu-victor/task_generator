from model.taskManager import TaskManager
from view.createTaskView import CreateTaskView
from view.modifyTaskView import ModifyTaskView
from view.deleteTaskView import DeleteTaskView
from controller.createTaskController import CreateTaskController
from controller.modifyTaskController import ModifyTaskController
from controller.deleteTaskController import DeleteTaskController

from tkinter import messagebox

class MainController:
    def __init__(self, view):
        self.view = view
        self.task_manager = TaskManager()
        self.sort_order = {}

        self._load_tasks_from_task_manager()
        self.update_view()

        self.view.set_on_create_task(self.open_create_task_view)
        self.view.set_on_modify_task(self.open_modify_task_view)
        self.view.set_on_delete_task(self.open_delete_task_view)
        self.view.set_on_column_click(self.sort_table_by_column)

    # Load the tasks from the CSV
    def _load_tasks_from_task_manager(self):
        """Load the tasks from the CSV file."""
        tasks = self.task_manager.get_tasks()
        self.view.populate_table(tasks)


    # Open windows on button click
    def open_create_task_view(self):
        """Open the create task window"""
        create_view = CreateTaskView(self.view.window)
        CreateTaskController(
                create_view,
                self.task_manager,
                self.add_task_to_view
        )

    def open_modify_task_view(self):
        """Open the modify task window.
        - Note: completed tasks cannot be modified."""
        selected_item = self.select_item()
        if not selected_item:
            return None
        
        task_index = self.view.tree.index(selected_item[0])
        task = self.task_manager.tasks[task_index]

        # If the task is completed, pop an error message
        if task[5] == "Completed":
            messagebox.showerror(
                "Error",
                "The selected task is completed and cannot be modified."
            )
            return None

        # Open the modify task view if the task is not completed
        modify_view = ModifyTaskView(self.view.window, task)
        ModifyTaskController(
                modify_view,
                self.task_manager,
                task_index,
                self.modify_task_in_view
        )

    def open_delete_task_view(self):
        """Open the delete task window:
        - First: user has to select a task for it to be deleted
        """
        selected_item = self.select_item()
        if not selected_item:
            return None
        else: 
            task_index = self.view.tree.index(selected_item[0])
            task = self.task_manager.tasks[task_index]

            delete_view = DeleteTaskView(self.view.window, task)
            DeleteTaskController(
                    delete_view,
                    self.task_manager,
                    task_index,
                    self.delete_task_in_view
            )

    def select_item(self):
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No task selected")
        return selected_item or None

    def sort_table_by_column(self, column):
        """Sort table by the column (ascending and descending)"""
        # Toggle
        self.sort_order[column] = not self.sort_order.get(column, False)
        sorted_tasks = self.task_manager.sort_tasks(
                column,
                self.sort_order[column]
        )
        self.view.populate_table(sorted_tasks)


    # Visualize the tasks on the main window
    def add_task_to_view(self, task):
        self.view.add_task_to_table(task)

    def modify_task_in_view(self, task_id, updated_task):
        self.view.modify_task_in_table(task_id, updated_task)

    def delete_task_in_view(self, task_id):
        self.view.delete_task_from_table(task_id)

    def save_tasks_on_exit(self):
        self.task_manager.save_tasks()

    def update_view(self):
        """Update the view to show task updates"""
        for task in self.task_manager.tasks:
            self.view.modify_task_in_table(task[0], task)
        # Keep updating every second
        self.view.window.after(1000, self.update_view)