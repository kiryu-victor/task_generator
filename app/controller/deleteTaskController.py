from tkinter import messagebox

class DeleteTaskController:
    def __init__(self, view, task_manager, task_index, delete_task_callback):
        self.view = view
        self.task_manager = task_manager
        self.task_index = task_index
        self.delete_task_callback = delete_task_callback

        self.view.set_on_delete_task(self._delete_task)

    def _delete_task(self):
        """Delete the selected task"""
        task_id = self.task_manager.tasks[self.task_index][0]
        self.task_manager.delete_task(task_id)

        self.delete_task_callback(task_id)

        messagebox.showinfo("Success", "Task deleted successfully!")
        self.view.destroy()