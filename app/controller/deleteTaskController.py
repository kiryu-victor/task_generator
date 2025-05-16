from tkinter import messagebox

class DeleteTaskController:
    def __init__(self, view, task_manager, task_id, delete_task_callback):
        self.view = view
        self.task_manager = task_manager
        self.task_id = task_id
        self.delete_task_callback = delete_task_callback

        # Get the task that we selected
        self.task = self.task_manager.read_task(task_id)
        if not self.task:
            messagebox.showerror("Error", "Task not found")
            self.view.destroy()

        # Show the values of the task
        self._set_values()
        # Delete on "DELETE" button click
        self.view.set_on_delete_task(self._delete_task)


    def _set_values(self):
        """
        Set the values of the labels for the selected task
        so the user can see the data from the task about to be deleted.
        """
        self.view.id_selected.config(text=self.task.task_id)
        self.view.date_created_selected.config(text=self.task.timestamp_start)
        self.view.machine_selected.config(text=self.task.machine)
        self.view.material_selected.config(text=self.task.material)
        self.view.speed_selected.config(text=self.task.speed)
        self.view.status_selected.config(text=self.task.status)


    def _delete_task(self):
        """Delete the selected task."""
        self.task_manager.delete_task(self.task_id)

        messagebox.showinfo("Success", "Task deleted successfully!")

        # Repopulate the view with updated tasks
        if self.delete_task_callback:
            self.delete_task_callback()
        
        self.view.destroy()