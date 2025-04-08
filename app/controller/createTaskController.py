from tkinter import messagebox

from datetime import datetime as dt

class CreateTaskController:
    def __init__(self, view, task_manager, add_task_callback):
        self.view = view        
        self.task_manager = task_manager
        self.add_task_callback = add_task_callback

        self.view.set_on_create_task(self._create_task)
        self.view.set_on_machine_type_change(self._on_machine_type_change)

    # Generate a new task when the button is pressed
    def _create_task(self):
        """Create a new task on the press of the button and after confirmation"""
        # Validate the inputs before creating the task
        if not self._validate_inputs():
            # Get the values from the view
            machine = self.view.machine_combo.get()
            material = self.view.material_combo.get()
            speed = self.view.speed_entry.get()
            
            # Create a new task model instance and set its attributes
            task = [
                dt.now().strftime('%Y%m%d-%H%M%S'),
                dt.now().strftime("%H:%M:%S"),
                machine,
                material,
                speed,
                "Pending"
            ]
            # Add it to the view
            self.task_manager.add_task(task)

            self.add_task_callback(task)

            messagebox.showinfo("Success", "Task created successfully!")

            # Clear the input fields after task creation
            self.view.machine_combo.set("")
            self.view.material_combo.set("")
            self.view.speed_entry.delete(0, 'end')
        else:
            # If validation fails, show an error message
            self._validate_input_which()

    def _validate_inputs(self):
        """Check if the values aren't empty"""
        if not self.view.machine_combo.get() or not self.view.material_combo.get() or not self.view.speed_entry.get():
            return True
        else:
            return False
        
    def _validate_input_which(self):
        """Check each input field and prompt a message accordingly"""
        if not self.view.machine_combo.get():
            messagebox.showerror("Error", "There is no machine type specified.")
        elif not self.view.material_combo.get():
            messagebox.showerror("Error", "Select a material.")
        elif not self.view.speed_entry.get():
            messagebox.showerror("Error", "No cutting speed is specified.")

    def _on_machine_type_change(self, machine_type):
        """Modify the materials according to the machine type selected"""
        if machine_type == "Machine A":
            self.view.material_combo["values"] = ["Mat A1", "Mat A2"]
        elif machine_type == "Machine B":
            self.view.material_combo["values"] = ["Mat B1", "Mat B2"]
        elif machine_type == "Machine C":
            self.view.material_combo["values"] = ["Mat C1", "Mat C2"]