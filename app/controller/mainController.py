from model.taskManager import TaskManager
from view.createTaskView import CreateTaskView
from view.modifyTaskView import ModifyTaskView
from view.deleteTaskView import DeleteTaskView
from controller.createTaskController import CreateTaskController
from controller.modifyTaskController import ModifyTaskController
from controller.deleteTaskController import DeleteTaskController
from utils.database import DatabaseManager

from tkinter import messagebox

class MainController:
    def __init__(self, view):
        self.view = view
        self.db_manager = DatabaseManager()
        self.task_manager = TaskManager(self.db_manager)
        self.sort_order = {}

        self._load_tasks_from_db()

        # Callbacks
        self.view.set_on_create_task(self.open_create_task_view)
        self.view.set_on_modify_task(self.open_modify_task_view)
        self.view.set_on_delete_task(self.open_delete_task_view)
        self.view.set_on_column_click(self.sort_table_by_column)

    # Load the tasks from the DB
    def _load_tasks_from_db(self):
        """Load the tasks from the DB."""
        tasks = self.task_manager.read_all_tasks()
        self.view.populate_table(tasks)


    # Open windows on button click
    def open_create_task_view(self):
        """Open the create task window and initiates its controller."""
        create_view = CreateTaskView(self.view.window)
        CreateTaskController(
                create_view,
                self.task_manager,
                self.refresh_main_view
        )

    def open_modify_task_view(self):
        """
        Open the modify task window.
        - Note: completed tasks cannot be modified.
        """
        selected_item = self.select_item()
        if not selected_item:
            return None

        task = self.get_task_from_selected_item(selected_item)
        
        # If the task is completed it cannot be modified
        if task.status == "Completed":
            messagebox.showerror(
                    "Error",
                    "The selected task is completed and cannot be modified."
            )
            return None
        else:
            # Open the modify task view and initiates its controller
            modify_view = ModifyTaskView(self.view.window)
            ModifyTaskController(
                    modify_view,
                    self.task_manager,
                    task.task_id,
                    self.refresh_main_view
        )

    def open_delete_task_view(self):
        """
        Open the delete task window and initiates its controller.
        - Note: completed tasks cannot be deleted.
        """
        selected_item = self.select_item()

        if not selected_item:
            return None
        else: 
            task = self.get_task_from_selected_item(selected_item)
            
            # If the task is completed it cannot be deleted
            if task.status == "Completed":
                messagebox.showerror(
                        "Error",
                        "The selected task is completed and cannot be deleted."
                        )
                return None
            else:
                delete_view = DeleteTaskView(self.view.window)
                DeleteTaskController(
                        delete_view,
                        self.task_manager,
                        task.task_id,
                        self.refresh_main_view
                )


    # Other utils
    def select_item(self):
        """Returns the selected row in the table as tuple."""
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No task selected")
        return selected_item or None
    
    def get_task_from_selected_item(self, selected_item):
        """
        Returns a task by getting the task_id.
        This is done by accessing the value
        of the first column [0] of a selected_item.
        """ 
        task_id = self.view.tree.item(selected_item, "values")[0]
        task = self.task_manager.read_task(task_id)
        return task
    
    def refresh_main_view(self):
        """Refresh the main view with the updated tasks from the DB."""
        tasks = self.task_manager.read_all_tasks()
        self.view.populate_table(tasks)

    def sort_table_by_column(self, column):
        """
        Sort table by the column (ascending and descending).
        Changes the current order to the opposite when clicking on it.
        Populates the table again with the new sorting order.
        """
        # Toggle sorting
        self.sort_order[column] = not self.sort_order.get(column, False)
        sorted_tasks = self.task_manager.sort_tasks(
                column,
                self.sort_order[column]
        )
        self.view.populate_table(sorted_tasks)