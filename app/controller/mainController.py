from datetime import datetime
from tkinter import messagebox
import tkinter as tk

from controller.createTaskController import CreateTaskController
from controller.modifyTaskController import ModifyTaskController
from controller.deleteTaskController import DeleteTaskController
from model.taskModel import TaskModel
from view.createTaskView import CreateTaskView
from view.modifyTaskView import ModifyTaskView
from view.deleteTaskView import DeleteTaskView


class MainController:
    def __init__(self, view, ws_client):
        self.view = view
        self.ws_client = ws_client
        self.sort_order = {}
        # Task instance
        self.task = TaskModel()
        self.previous_tasks = {}

        # Callbacks
        self.view.set_on_create_task(self.open_create_task_view)
        self.view.set_on_modify_task(self.open_modify_task_view)
        self.view.set_on_delete_task(self.open_delete_task_view)
        self.view.set_on_column_click(self.sort_table_by_column)

        # Start client-side countdown refresher
        self._start_countdown_refresher()

    
    # Open windows on button click
    def open_create_task_view(self):
        """Open the create task window and initiates its controller."""
        create_view = CreateTaskView(self.view.window)
        CreateTaskController(
                create_view,
                self.ws_client
        )

    def open_modify_task_view(self):
        """
        Open the modify task window.
        - Note: completed tasks cannot be modified.
        """
        selected_item = self.select_item()

        if not selected_item:
            return None
        else:
            self.task = self.get_task_from_selected_item(selected_item)
        
            # If the task is completed it cannot be modified
            if self.task.status == "Completed":
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
                        self.ws_client,
                        self.task
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
            self.task = self.get_task_from_selected_item(selected_item)
            
            # If the task is completed it cannot be deleted
            if self.task.status == "Completed":
                messagebox.showerror(
                        "Error",
                        "The selected task is completed and cannot be deleted."
                )
                return None
            else:
                delete_view = DeleteTaskView(self.view.window)
                DeleteTaskController(
                        delete_view,
                        self.ws_client,
                        self.task
                )

    # Other functions
    def select_item(self):
        """Returns the selected row in the table as tuple."""
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No task selected")
            return None
        return selected_item
    
    def get_task_from_selected_item(self, selected_item):
        """
        Returns a task from the selected item on the tree.
        This is done by accessing the values of the columns
        by the selected_item and passing them to the attribs on the task.
        """ 
        self.task.task_id = self.view.tree.item(selected_item, "values")[0]
        self.task.machine = self.view.tree.item(selected_item, "values")[2]
        self.task.material = self.view.tree.item(selected_item, "values")[3]
        self.task.speed = self.view.tree.item(selected_item, "values")[4]
        self.task.status = self.view.tree.item(selected_item, "values")[5]
        self.task.time_left = self.view.tree.item(selected_item, "values")[6]

        return self.task

    def sort_table_by_column(self, column):
        """
        Sort table by the column (ascending and descending) using only the data in the Treeview.
        Handles mixed types in the Status column: 'On queue' > int > 'Completed'.
        """
        column_indices = {
            "Task ID": 0,
            "Time": 1,
            "Machine": 2,
            "Material": 3,
            "Speed": 4,
            "Status": 5,
            "Time left": 6
        }
        col_index = column_indices[column]

        # Get the data from the table
        items = self.view.tree.get_children()
        # List of lists. Sublist has the values of a row
        rows = [self.view.tree.item(item)["values"] for item in items]
        
        # Toggles the order on click
        self.sort_order[column] = not self.sort_order.get(column, False)
        reverse = not self.sort_order[column]

        def status_sort_key(value):
            # Custom sort: 'On queue' > int > 'Completed'
            # It will sort by the first value on the tuple
            # and after that, by the second one
                # Example: On queue > In progress > Completed
            if value == "On queue":
                return (2, 0)
            if value == "In progress":
                return (1, 0)
            if value == "Completed":
                return (0, 0)

        # If sorting by status, use the custom sort above
        if column == "Status":
            sorted_rows = sorted(
                    rows,
                    key=lambda x: status_sort_key(x[col_index]),
                    reverse=reverse
            )
        else:
            sorted_rows = sorted(
                    rows,
                    key=lambda x: x[col_index],
                    reverse=reverse
            )
        
        for item in items:
            self.view.tree.delete(item)
        for row in sorted_rows:
            self.view.tree.insert("", tk.END, values=row)

    # Countdown logic for the client side
    def _start_countdown_refresher(self):
        "Start the countdown every 5 seconds after the client connects to the server."
        self.view.window.after(5000, self._countdown_refresher)

    def _countdown_refresher(self):
        """
        Iterate over all the rows and decrement the "Time left" for ongoing tasks.
        """
        for item in self.view.tree.get_children():
            values = list(self.view.tree.item(item, "values"))

            try:
                if values[5] == "In progress":
                    time_expected = values[7]
                    time_left = (
                            datetime.strptime(time_expected, "%Y-%m-%d %H:%M:%S.%f")
                            - datetime.now()
                            ).total_seconds()
                    seconds_left = int(time_left)

                    values[6] = seconds_left
                    self.view.tree.item(item, values=values)
            except Exception:
                continue
        # Next refresh in 5 seconds
        self.view.window.after(5000, self._countdown_refresher)