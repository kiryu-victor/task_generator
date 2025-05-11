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
        task = self.task_manager.read_task(task_id)
        print(f"Task: {task.to_tuple()}")
        # Set the old values on the modify menu
        if not task:
            messagebox.showerror("Error", "Task not found.")
            self.view.destroy()
            return
        
        # Populate the old values
        self.view.set_old_values(
            task.machine, # Machine
            task.material, # Material
            task.speed, # Speed
            task.status, # Status
        )
        
        # Set the button the _modify_task method
        self.view.set_on_modify_task(self._modify_task)
        self.view.set_on_machine_type_change(self._on_machine_type_change)
        self.view.set_on_material_change(self._on_material_change)

        # Populate the machine dropdown with the "name" of the machine
        # for every machine on "machines"
        self.view.machine_combo["values"] = [
                machine["name"] for machine in self.config["machines"]
        ]

        # If the task has started, populate the speed range this way
        if task.status.isdigit():
            self.on_started_task_modify()

    # Modify a task that has been selected
    def _modify_task(self):
        """Modify the selected task.
        Validate if a task can be modified first.
        Tasks that haven't started yet can be fully modified.
        Tasks that are ongoing can only have speed modified (recalculated).
        Tasks that are completed cannot be modified."""
        try:
            # Check the status of the task we selected
            # Depending on it the values will take the values from the combo
            # or from the label
            task = self.task_manager.read_task(self.task_id)
            if task.status == "On queue":
                machine = self.view.get_machine()
                material = self.view.get_material()
            else:
                machine = self.view.machine_old_value.cget("text")
                material = self.view.material_old_value.cget("text")
            speed = self.view.get_speed()

            # Tengo que pasar una tupla para cambiar los datos que han cambiado
            updating_tuple = (machine, material, str(speed), self.task_id)
            
            # Validate the inputs
            utils = Utils()
            is_valid, error_message = utils.validate_inputs(machine, material, speed)
            if not is_valid:
                messagebox.showerror("Input error", error_message)
                return
            
            # Set the values for a task
            updated_task = self.task_manager.read_task(self.task_id)
            updated_task.machine = machine
            updated_task.material = material
            updated_task.speed = int(speed)
            
            # Update the task on the DB
            self.task_manager.update_task(self.task_id, updating_tuple)

            # Modal window for success
            messagebox.showinfo("Success", "Task modified.")
            self.view.destroy()
        
        except ValueError as e:
            messagebox.showerror("Error", str(e))


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

    def on_started_task_modify(self):
        """Populates the speed range a started task can select."""
        machine_type = self.view.machine_old_value.cget("text")
        material_name = self.view.material_old_value.cget("text")

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