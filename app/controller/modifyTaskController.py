from tkinter import messagebox
from utils.utils import Utils


class ModifyTaskController:
    def __init__(self, view, task_manager, task_index, modify_task_callback):
        self.view = view
        self.task_manager = task_manager
        self.task_index = task_index
        self.modify_task_callback = modify_task_callback

        # Load config.json for the machine, materials and speeds settings
        self.config = Utils.load_config()

        # Get the task that we selected
        task = self.task_manager.tasks[task_index]
        # Set the old values on the modify menu
        self.view.set_old_values(task[2], task[3], task[4], task[5])

        self.view.set_on_modify_task(self._modify_task)
        self.view.set_on_machine_type_change(self._on_machine_type_change)
        self.view.set_on_material_change(self._on_material_change)

        # Populate the machine dropdown with the "name" of the machine
        # for every machine on "machines"
        self.view.machine_combo["values"] = [
                machine["name"] for machine in self.config["machines"]
        ]

    # Modify a task that has been selected
    def _modify_task(self):
        """Modify the selected task.
        Validate if a task can be modified first.
        Tasks that haven't started yet can be fully modified.
        Tasks that are ongoing can only have speed modified (recalculated).
        Tasks that are completed cannot be modified."""
        machine = self.view.machine_combo.get()
        material = self.view.material_combo.get()
        speed = self.view.speed_entry.get()
        
        # Get the status of the selected task
        current_task = self.task_manager.tasks[self.task_index]

        # Madify the parameters that can be changed depending on status     
        # If it is ongoing task  
        if current_task[5].isdigit():
            current_task[4] = speed
        # If it has not started yet
        else:
            current_task[2] = machine
            current_task[3] = material
            current_task[4] = speed

        # Update the task in the model
        task_id = current_task[0]
        self.task_manager.modify_task(task_id, current_task)

        # Update in on the view
        self.modify_task_callback(task_id, current_task)

        # Modal window for success
        messagebox.showinfo("Success", "Task modified.")
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

    # Modify the materials depending on the machine
    def _on_machine_type_change(self, machine_type):
        """Modify the materials according to the machine type selected"""
        # Reset the values that could be set by the user
        self.view.material_combo.set("")
        self.view.speed_entry.delete(0)
        self.view.speed_range_label.config(text="")
        
        for machine in self.config["machines"]:
            if machine["name"] == machine_type:
                self.view.material_combo["values"] = machine["materials"]
                break

    # Modify the speeds depending on the material
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