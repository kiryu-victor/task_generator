from datetime import datetime as dt
from tkinter import messagebox

from model.taskModel import TaskModel
from view.mainView import MainView
from utils.utils import Utils

class CreateTaskController:
    def __init__(self, view, task_manager, add_task_callback):
        self.view = view
        self.task_manager = task_manager
        self.add_task_callback = add_task_callback

        # Load config.json for the machine, materials and speeds settings
        self.config = Utils.load_config()

        # Callbacks
        self.view.set_on_create_task(self._create_task)
        self.view.set_on_machine_type_change(self._on_machine_type_change)
        self.view.set_on_material_change(self._on_material_change)

        # Populate machine dropdown
        self.view.machine_combo["values"] = [machine["name"]
                                                    for machine
                                                    in self.config["machines"]]


    def _create_task(self):
        """Create a new task on the press of the button and after confirmation."""
        # Get the fields values
        machine = self.view.machine_combo.get()
        material = self.view.material_combo.get()
        speed = self.view.speed_entry.get()

        # Validate the inputs
        utils = Utils()
        is_valid, error_message = utils.validate_inputs(machine, material, speed)
        if not is_valid:
            messagebox.showerror("Input error", error_message)
            return
        
        # Get the expected time of completion (ETC) from config.json
        expected_time = next(
            (
                machine_config["expected_time"]
                for machine_config in self.config["machines"]
                if machine_config["name"] == machine
            ), 0
        )

        # Create new task for inserting on the DB
        task = TaskModel(
            machine = machine,
            material = material,
            speed = int(speed),
            time_left = expected_time
        )

        # Insert said task
        self.task_manager.create_task(task)
        messagebox.showinfo("Success", "Task created successfully!")

        # Repopulate the view with updated tasks
        if self.add_task_callback:
            self.add_task_callback()

        # Clear the input fields after task creation
        self.view.machine_combo.set("")
        self.view.material_combo.set("")
        self.view.speed_entry.delete(0, 'end')
        
        self.view.destroy()

    def _on_machine_type_change(self, machine_type):
        """Modify the materials according to the machine type selected."""
        # Reset the values that could be set by the user
        self.view.material_combo.set("")
        self.view.speed_entry.delete(0, "end")
        self.view.speed_range_label.config(text="")

        # Populate the combobox with the materials
        for machine in self.config["machines"]:
            if machine["name"] == machine_type:
                self.view.material_combo["values"] = machine["materials"]
                break


    def _on_material_change(self, material_name):
        """Modify the speed range according to the material selected."""
        # Reset the values that could be set by the user
        self.view.speed_entry.delete(0, "end")
        self.view.speed_range_label.config(text="")

        # Get the type of machine selected
        machine_type = self.view.machine_combo.get()
        
        for material in self.config["materials"]:
            if material["name"] == material_name:
                # Set the speed range depending on the selected material
                if "carbide" in machine_type.lower():
                    min_speed = material["carbide_minSpeed"]
                    max_speed = material["carbide_maxSpeed"]
                elif "hss" in machine_type.lower():
                    min_speed = material["hss_minSpeed"]
                    max_speed = material["hss_maxSpeed"]
                
                # Write the speed range for the user to know
                self.view.speed_range_label.config(
                    text=f"Speed range: {min_speed} - {max_speed}"
                )
                break