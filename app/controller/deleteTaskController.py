from tkinter import messagebox


class DeleteTaskController:
    def __init__(self, view, ws_client, task):
        self.view = view
        self.ws_client = ws_client
        self.task = task

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
        self.ws_client.send("delete", {"task_id": self.task.task_id})
        messagebox.showinfo("Success", "Task deleted successfully!")
        
        self.view.destroy()