import json

class Utils:
    def __init__(self):
        self.config = Utils.load_config()


    @staticmethod
    def center_window_on_screen(window, width, height):
        """Center a window on any screen"""
        # Updates the data from geometry
        window.update_idletasks()
        # Get both screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        # Center horizontally
        position_x = (screen_width - width) // 2
        # Center vertically
        position_y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{position_x}+{position_y}")

    @staticmethod
    def load_config():
        """Load the configuration from the config.json file"""
        with open("app/utils/config.json", "r") as file:
            return json.load(file)


    def validate_inputs(self, machine, material, speed):
        """Validate that inputs are not empty and speed is a valid number"""
        # Check all the values are filled
        if not machine or not material or not speed:
            return False, Utils.validate_inputs_which(machine, material)
        try:
            current_speed = int(speed)
        # If the value on the speed is not a number
        except ValueError:
            # Return False, and the message for the messagebox
            return False, "Speed must be a valid number."
        
        for material_config in self.config["materials"]:
            if material_config["name"] == material:
                if "carbide" in machine.lower():
                    min_speed = int(material_config["carbide_minSpeed"])
                    max_speed = int(material_config["carbide_maxSpeed"])
                elif "hss" in machine.lower():
                    min_speed = int(material_config["hss_minSpeed"])
                    max_speed = int(material_config["hss_maxSpeed"])
                
                # Check if the speed is on the range
                if current_speed < min_speed or current_speed > max_speed:
                    return False, f"The speed is not within the correct limits ({min_speed} - {max_speed})"
                break

        return True, None


    @staticmethod
    def validate_inputs_which(machine, material):
        """Return the correspponding message based on the missing field"""
        if not machine:
            return "There is no machine type specified."
        elif not material:
            return "Select a material."
        else:
            return "No cutting speed is specified."