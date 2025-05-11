from utils.wss import WebSocketServer
from model.taskManager import TaskManager
from view.createTaskView import CreateTaskView
from view.modifyTaskView import ModifyTaskView
from view.deleteTaskView import DeleteTaskView
from controller.createTaskController import CreateTaskController
from controller.modifyTaskController import ModifyTaskController
from controller.deleteTaskController import DeleteTaskController
from utils.db import DatabaseManager

from tkinter import messagebox

class MainController:
    def __init__(self, view, websocket_server):
        self.view = view
        self.websocket_server = websocket_server

        # Initialize the DB on app start
        db_manager = DatabaseManager()
        db_manager.initialize_database()

        self.task_manager = TaskManager(db_manager, websocket_server)
        self.sort_order = {}

        self._load_tasks_from_task_manager()
        # self.update_view()

        self.view.set_on_create_task(self.open_create_task_view)
        self.view.set_on_modify_task(self.open_modify_task_view)
        self.view.set_on_delete_task(self.open_delete_task_view)
        self.view.set_on_column_click(self.sort_table_by_column)

    # Load the tasks from the database
    def _load_tasks_from_task_manager(self):
        """Load the tasks from the CSV file."""
        tasks = self.task_manager.get_all_tasks()
        self.view.populate_table(tasks)


    # Open windows on button click
    def open_create_task_view(self):
        """Open the create task window"""
        create_view = CreateTaskView(self.view.window)
        CreateTaskController(
                create_view,
                self.task_manager,
                self.view.add_task_to_table
        )

    def open_modify_task_view(self):
        """Open the modify task window.
        - Note: completed tasks cannot be modified."""
        selected_item = self.select_item()
        if not selected_item:
            return None
        
        task_id = self.view.tree.item(selected_item[0], "values")[0]
        task = self.task_manager.read_task(task_id)

        # If the task is completed, pop an error message
        if task.status == "Completed":
            messagebox.showerror(
                "Error",
                "The selected task is completed and cannot be modified."
            )
            return None

        # Open the modify task view if the task is not completed
        modify_view = ModifyTaskView(self.view.window, task_id)
        ModifyTaskController(
                modify_view,
                self.task_manager,
                task_id,
                self.view.modify_task_in_table
        )

    def open_delete_task_view(self):
        """Open the delete task window:
        - First: user has to select a task for it to be deleted
        """
        selected_item = self.select_item()
        if not selected_item:
            return None
        
        task_id = self.view.tree.item(selected_item[0], "values")[0]
        task = self.task_manager.read_task(task_id)

        delete_view = DeleteTaskView(self.view.window, task.task_id)
        DeleteTaskController(
                delete_view,
                self.task_manager,
                task_id
        )

    # Other methods
    def select_item(self):
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No task selected")
        return selected_item or None

    def sort_table_by_column(self, column):
        """Sort table by the column (ascending and descending)"""
        self.task_manager.sort_tasks(column)

    # def update_view(self):
    #     """Update the view to show task updates"""
    #     tasks = self.task_manager.get_all_tasks()
    #     for task in tasks:
    #         self.view.modify_task_in_table(task[0], task)
    #     # Keep updating every second
    #     self.view.window.after(1000, self.update_view)

    def complete_task(self, task_id):
        self.task_manager.update_task_status(task_id, "Completed")
        task = self.task_manager.read_task(task_id)
        self.view.modify_task_in_table(task_id, task[0])