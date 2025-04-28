from tkinter import messagebox
from utils.utils import Utils

from datetime import datetime as dt

class CreateTaskController:
    def __init__(self, view, task_manager, add_task_callback):
        self.view = view        
        self.task_manager = task_manager
        self.add_task_callback = add_task_callback

        # Load config.json for the machine, materials and speeds settings
        self.config = Utils.load_config()

        self.view.set_on_create_task(self._create_task)
        self.view.set_on_machine_type_change(self._on_machine_type_change)
        self.view.set_on_material_change(self._on_material_change)

        # Populate machine dropdown
        self.view.machine_combo["values"] = [machine["name"] for machine in self.config["machines"]]

    # Generate a new task when the button is pressed
    def _create_task(self):
        """Create a new task on the press of the button
        and after confirmation"""
        # Ge the fields values
        machine = self.view.machine_combo.get()
        material = self.view.material_combo.get()
        speed = self.view.speed_entry.get()
        # Validate the inputs before creating the task
        if self._validate_inputs(machine, material, speed):
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
            
            self.view.destroy()

    def _validate_inputs(self, machine, material, speed):
        """Check if the values aren't empty"""
        utils = Utils()
        is_valid, error_message = utils.validate_inputs(
                machine, material, speed
        )
        if not is_valid:
            messagebox.showerror("Input error", error_message)
        return is_valid

    def _on_machine_type_change(self, machine_type):
        """Modify the materials according to the machine type selected.
        Data is changed on utils/config.json"""
        # Reset the values that could be set by the user
        self.view.material_combo.set("")
        self.view.speed_entry.delete(0)
        self.view.speed_range_label.config(text="")

        # Populate the combobox with the materials
        for machine in self.config["machines"]:
            if machine["name"] == machine_type:
                self.view.material_combo["values"] = machine["materials"]
                break

    def _on_material_change(self, material_name):
        """Modify the speed range according to the material selected.
        Data is changed on utils/config.json"""
        # Get the type of machine selected
        machine_type = self.view.machine_combo.get()
        
        for material in self.config["materials"]:
            if material["name"] == material_name:
                if "carbide" in machine_type.lower():
                    min_speed = material["carbide_minSpeed"]
                    max_speed = material["carbide_maxSpeed"]
                elif "hss" in machine_type.lower():
                    min_speed = material["hss_minSpeed"]
                    max_speed = material["hss_maxSpeed"]
                
                # Check if the speed is on the range
                self.view.speed_range_label.config(
                    text=f"Speed range: {min_speed} - {max_speed}"
                )
                break