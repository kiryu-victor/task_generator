import random
from tkinter import messagebox

from model.taskModel import TaskModel
from utils.utils import Utils


class CreateTaskController:
    def __init__(self, view, ws_client):
        self.view = view
        self.ws_client = ws_client

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
        """
        Create a new task on the press of the button and after confirmation.
        Each task has a random amount of surface to achieve blueprint variability.
        The task is then passed as a dictionary to the WebSocket client to then be sent to the WebSocket server.
        Clears the fields after and closes the window.
        """
        # Get the fields values
        machine = self.view.machine_combo.get()
        material = self.view.material_combo.get()
        speed = int(self.view.speed_entry.get())

        # Validate the inputs
        utils = Utils()
        is_valid, error_message = utils.validate_inputs(machine, material, speed)
        if not is_valid:
            messagebox.showerror("Input error", error_message)
            return
        
        # Create a task with a random surface for added variability
        surface_min = next(
            (
                machine_config["surface_min"]
                for machine_config in self.config["machines"]
                if machine_config["name"] == machine
            ), 0
        )
        surface_max = next(
            (
                machine_config["surface_max"]
                for machine_config in self.config["machines"]
                if machine_config["name"] == machine
            ), 0
        )
        surface = random.randrange(int(surface_min), int(surface_max))

        # Create new task for inserting on the DB
        task = TaskModel(
            machine= machine,
            material= material,
            speed= speed,
            time_left= int(surface / speed),
            surface= surface,
        )

        # Send the task to the server via WebSocket
        self.ws_client.send("create", task.__dict__)
        messagebox.showinfo("Success", "Task creation requested!")

        # Clear the input fields after task creation
        self.view.machine_combo.set("")
        self.view.material_combo.set("")
        self.view.speed_entry.delete(0, "end")
        
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