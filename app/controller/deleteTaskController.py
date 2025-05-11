from tkinter import messagebox

class DeleteTaskController:
    def __init__(self, view, task_manager, task_id):
        self.view = view
        self.task_manager = task_manager
        self.task_id = task_id

        # Get the task that we selected
        task = self.task_manager.read_task(task_id)
        if not task:
            messagebox.showerror("Error", "Task not found.")
            self.view.destroy()
            return

        # Set the old values on the delete menu
        self.view.set_old_values(
                task.task_id,
                task.timestamp_start,
                task.machine,
                task.material,
                task.speed,
                task.status
        )
        # Set the button the _delete_task method
        self.view.set_on_delete_task(self._delete_task)


    def _delete_task(self):
        """Delete the selected task"""
        self.task_manager.delete_task(self.task_id)

        messagebox.showinfo("Success", "Task deleted successfully!")
        self.view.destroy()