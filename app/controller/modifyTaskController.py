from tkinter import messagebox

class ModifyTaskController:
    def __init__(self, view, task_manager, task_index, modify_task_callback):
        self.view = view
        self.task_manager = task_manager
        self.task_index = task_index
        self.modify_task_callback = modify_task_callback

        # Get the task that we selected
        task = self.task_manager.tasks[task_index]
        # Set the old values on the modify menu
        self.view.set_old_values(task[2], task[3], task[4])

        self.view.set_on_modify_task(self._modify_task)
        self.view.set_on_machine_type_change(self._on_machine_type_change)

    # Modify a task that has been selected
    def _modify_task(self):
        """Modify the selected task"""
        machine = self.view.machine_combo.get()
        material = self.view.material_combo.get()
        speed = self.view.speed_entry.get()

        if not machine or not material or not speed:
            messagebox.showerror("Error", "There should be no empty fields.")
            return

        # Update the values
        modified_task = [
            self.task_manager.tasks[self.task_index][0],    # Index
            self.task_manager.tasks[self.task_index][1],    # Start time
            machine,
            material,
            speed,
            self.task_manager.tasks[self.task_index][5],    # Status            
        ]

        task_id = self.task_manager.tasks[self.task_index][0]
        self.task_manager.modify_task(task_id, modified_task)

        self.modify_task_callback(task_id, modified_task)

        messagebox.showinfo("Success", "Task modified successfully!")
        self.view.destroy()

    # Modify the materials depending on the machine
    def _on_machine_type_change(self, machine_type):
        """Modify the materials according to the machine type selected"""
        if machine_type == "Machine A":
            self.view.material_combo["values"] = ["Mat A1", "Mat A2"]
        elif machine_type == "Machine B":
            self.view.material_combo["values"] = ["Mat B1", "Mat B2"]
        elif machine_type == "Machine C":
            self.view.material_combo["values"] = ["Mat C1", "Mat C2"]