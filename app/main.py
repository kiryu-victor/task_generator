from controller.mainController import MainController
from view.mainView import MainView

import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    main_view = MainView(root)
    main_controller = MainController(main_view)

    def on_close():
        main_controller.save_tasks_on_exit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()