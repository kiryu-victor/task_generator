from controller.mainController import MainController
from view.mainView import MainView

import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    
    # Load both the main view and controller
    main_view = MainView(root)
    main_controller = MainController(main_view)

    def on_close():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Shows all until the user terminates the program
    root.mainloop()