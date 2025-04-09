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

        self._load_tasks_from_task_manager()

        self.view.set_on_create_task(self.open_create_task_view)
        self.view.set_on_modify_task(self.open_modify_task_view)
        self.view.set_on_delete_task(self.open_delete_task_view)

    # Load the tasks from the CSV
    def _load_tasks_from_task_manager(self):
        """Load the tasks from the CSV file"""
        tasks = self.task_manager.get_tasks()
        self.view.populate_table(tasks)


    # Open windows on button click
    def open_create_task_view(self):
        """Open the create task window"""
        create_view = CreateTaskView(self.view.window)
        CreateTaskController(create_view, self.task_manager, self.add_task_to_view)

    def open_modify_task_view(self):
        """Open the modify task window"""
        selected_item = self.select_item()
        if not selected_item:
            return
        else:        
            task_index = self.view.tree.index(selected_item[0])
            task = self.task_manager.tasks[task_index]
            
            modify_view = ModifyTaskView(self.view.window, task)
            ModifyTaskController(modify_view, self.task_manager, task_index, self.modify_task_in_view)

    def open_delete_task_view(self):
        """Open the delete task window"""
        selected_item = self.select_item()

        if not selected_item:
            return
        else: 
            task_index = self.view.tree.index(selected_item[0])
            task = self.task_manager.tasks[task_index]

            delete_view = DeleteTaskView(self.view.window, task)
            DeleteTaskController(delete_view, self.task_manager, task_index, self.delete_task_in_view)

    def select_item(self):
        selected_item = self.view.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No task selected")
            return
        else:
            return selected_item

    # Visualize the tasks on the main window
    def add_task_to_view(self, task):
        self.view.add_task_to_table(task)

    def modify_task_in_view(self, task_id, updated_task):
        self.view.modify_task_in_table(task_id, updated_task)

    def delete_task_in_view(self, task_id):
        self.view.delete_task_from_table(task_id)

    def save_tasks_on_exit(self):
        self.task_manager.save_tasks()