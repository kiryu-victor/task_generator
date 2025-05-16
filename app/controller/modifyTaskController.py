from tkinter import messagebox
from utils.utils import Utils


class ModifyTaskController:
    def __init__(self, view, task_manager, task_id, modify_task_callback):
        self.view = view
        self.task_manager = task_manager
        self.task_id = task_id
        self.modify_task_callback = modify_task_callback

        # Load config.json for the machine, materials and speeds settings
        self.config = Utils.load_config()

        # Get the task that we selected
        self.task = self.task_manager.read_task(task_id)
        if not self.task:
            messagebox.showerror("Error", "Task not found")
            self.view.destroy()
            return

        # Set the current values for reference and the enabled fields
        self._set_current_values()
        self._set_enabled_combos()

        # Callbacks
        self.view.set_on_modify_task(self._modify_task)
        self.view.set_on_machine_type_change(self._on_machine_type_change)
        self.view.set_on_material_change(self._on_material_change)

        # Populate the machine dropdown with the "name" of the machine
        # for every machine on "machines"
        self.view.machine_combo["values"] = [
                machine["name"] for machine in self.config["machines"]
        ]

    # Set the current values of the task
    def _set_current_values(self):
        """
        Set the values of the labels for the selected task
        so the user can see the data from the task about to be modified.
        """
        self.view.machine_current_value.config(text=self.task.machine)
        self.view.material_current_value.config(text=self.task.material)
        self.view.speed_current_value.config(text=self.task.speed)

        if self.task.status.isdigit():
            self._on_started_task_modify()

    # Populates the speed range of a task that has already started
    def _on_started_task_modify(self):
        """Populates the speed range for a started task."""
        machine_type = self.view.machine_current_value.cget("text")
        material_name = self.view.material_current_value.cget("text")

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

    def _set_enabled_combos(self):
        """
        Set what comboboxes are enabled.
        Tasks that haven't started ('On queue') yet can be fully modified.
        Tasks that are ongoing can only have speed modified (recalculated).
        Tasks that are 'Completed' cannot be modified.
        """
        if self.task.status == "On queue":
            # If the task is waiting on the queue
            self.view.machine_combo["state"] = "readonly"
            self.view.material_combo["state"] = "readonly"
            self.view.speed_entry["state"] = "normal"
        else:
            # Ongoing task - Only speed can be changed
            self.view.machine_combo["state"] = "disabled"
            self.view.material_combo["state"] = "disabled"
            self.view.speed_entry["state"] = "normal"


    # Modify a task that has been selected
    def _modify_task(self):
        """
        Modify the selected task.
        Validate if a task can be modified first.
        Tasks that haven't started ('On queue') yet can be fully modified.
        Tasks that are ongoing can only have speed modified (recalculated).
        Tasks that are 'Completed' cannot be modified.
        """
        try:
            task = self.task_manager.read_task(self.task_id)
            if task.status == "On queue":
                machine = self.view.machine_combo.get()
                material = self.view.material_combo.get()
            else:
                machine = self.view.machine_current_value.cget("text")
                material = self.view.material_current_value.cget("text")
            speed = self.view.speed_entry.get()

            updating_tuple = (machine, material, str(speed), self.task_id)

            # Validate the inputs
            utils = Utils()
            is_valid, error_message = utils.validate_inputs(machine, material, speed)
            if not is_valid:
                messagebox.showerror("Input error", error_message)
                return

            # Update task on the DB
            self.task_manager.update_task(updating_tuple)
            
            messagebox.showinfo("Success", "Task modified.")
            
            # Repopulate the view with updated tasks
            if self.modify_task_callback:
                self.modify_task_callback()
            self.view.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))


    # Modify the materials and speeds
    def _on_machine_type_change(self, machine_type):
        """Modify the materials according to the machine type selected."""
        # Reset the values that could be set by the user
        self.view.material_combo.set("")
        self.view.speed_entry.delete(0, "end")
        self.view.speed_range_label.config(text="")
        
        for machine in self.config["machines"]:
            if machine["name"] == machine_type:
                self.view.material_combo["values"] = machine["materials"]
                break

    def _on_material_change(self, material_name):
        """
        Modify the speed range according to the material selected.
        Data is changed on utils/config.json
        """
        # Reset the values that could be set by the user
        self.view.speed_entry.delete(0, "end")
        self.view.speed_range_label.config(text="")

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
