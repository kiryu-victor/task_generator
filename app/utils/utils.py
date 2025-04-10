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
