import tkinter as tk
from tkinter import ttk
from utils.utils import Utils


class MainView():
    def __init__(self, root):
        self.window = root
        self.window.title("Main View")
        self.window.geometry("1000x600")
        self.window.resizable(False, False)

        # Center the window on the screen
        Utils.center_window_on_screen(self.window, 1000, 600)

        # Create a frame for the main view
        self.main_frame = ttk.Frame(self.window, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Callbacks for button clicks
        self._on_create_task = None
        self._on_task_selected = None
        self._on_modify_task = None
        self._on_delete_task = None
        self._on_column_click = None

        # Create the elements of the main view
        self._create_table()
        self._create_buttons()

    # Table for displaying tasks
    def _create_table(self):
        # Create a treeview for displaying data
        columns = ("Task ID", "Time", "Machine", "Material", "Speed", "Status")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        
        # Headings
        self.tree.heading("Task ID", text="Task ID",
                command=lambda: self.on_column_click("Task ID"))
        self.tree.heading("Time", text="Time",
                command=lambda: self.on_column_click("Time"))
        self.tree.heading("Machine", text="Machine",
                command=lambda: self.on_column_click("Machine"))
        self.tree.heading("Material", text="Material",
                command=lambda: self.on_column_click("Material"))
        self.tree.heading("Speed", text="Speed",
                command=lambda: self.on_column_click("Speed"))
        self.tree.heading("Status", text="Status",
                command=lambda: self.on_column_click("Status"))

        # Column widths
        self.tree.column("Task ID", width=100)
        self.tree.column("Time", width=100)
        self.tree.column("Machine", width=100)
        self.tree.column("Material", width=100)
        self.tree.column("Speed", width=100)
        self.tree.column("Status", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)


    # Buttons for creating, modifying, and deleting tasks
    def _create_buttons(self):
        # Create a frame for buttons
        self.button_frame = ttk.Frame(self.main_frame, padding=5)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # TODO: Find a way to make this less redundant
        self.create_button = tk.Button(self.button_frame, text="Create task",
                bg="#7fff69", font=("Arial", 20),
                command=lambda: self._on_create_task()
                        if self._on_create_task else None
        )

        self.modify_button = tk.Button(self.button_frame, text="Modify task",
                bg="#ffcf69", font=("Arial", 20),
                command=lambda: self._on_modify_task()
                        if self._on_modify_task else None
        )
        
        self.delete_button = tk.Button(self.button_frame, text="Delete task",
                bg="#ff6973", font=("Arial", 20),
                command=lambda: self._on_delete_task()
                        if self._on_delete_task else None
        )

        # Pack buttons
        self.create_button.pack(side=tk.LEFT, padx=0)
        # Expand to fill space (center)
        self.modify_button.pack(side=tk.LEFT, padx=0, expand=True)
        self.delete_button.pack(side=tk.RIGHT, padx=5)


    # Fill the table with data
    def populate_table(self, tasks):
        """Populate the table with the tasks"""
        # Clear previous values
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Add the tasks
        for task in tasks:
            self.tree.insert("", tk.END, values=task)

    # Sort the data on the table
    def on_column_click(self, column):
        if self._on_column_click:
            self._on_column_click(column)


    # Callbacks for button clicks
    def set_on_create_task(self, callback):
        self._on_create_task = callback

    def set_on_modify_task(self, callback):
        self._on_modify_task = callback

    def set_on_delete_task(self, callback):
        self._on_delete_task = callback

    def set_on_column_click(self, callback):
        self._on_column_click = callback