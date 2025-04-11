class Utils:
    @staticmethod
    def center_window_on_screen(window, width, height):
        """Center a window on any screen"""
        # Updates the data from geometry
        window.update_idletasks()
        # Get both screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        # Center horizontally (screen width / 2  -)
        position_x = (screen_width // 2) - (width // 2)
        # Center vertically
        position_y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{position_x}+{position_y}")

    @staticmethod
    def validate_inputs(machine, material, speed):
        """Validate that inputs are not empty and speed is a valid number"""
        # Check all the values are filled
        if not machine or not material or not speed:
            return False, Utils.validate_inputs_which(machine, material)
        try:
            int(speed)
            return True, None
        # If the value on the speed is not a number
        except ValueError:
            # Return False, and the message for the messagebox
            return False, "Speed must be a valid number."
        
    @staticmethod
    def validate_inputs_which(machine, material):
        """Return the correspponding message based on the missing field"""
        if not machine:
            return "There is no machine type specified."
        elif not material:
            return "Select a material."
        else:
            return "No cutting speed is specified."