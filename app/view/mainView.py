import tkinter as tk
from tkinter import ttk

class MainView():
    def __init__(self, root):
        self.window = root
        self.window.title("Main View")
        self.window.geometry("1000x600")
        self.window.resizable(False, False)

        # Create a frame for the main view
        self.main_frame = ttk.Frame(self.window, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Callbacks for button clicks
        self._on_create_task = None
        self._on_task_selected = None
        self._on_modify_task = None
        self._on_delete_task = None

        # Create the elements of the main view
        self._create_table()
        self._create_buttons()

    # Table for displaying tasks
    def _create_table(self):
        # Create a treeview for displaying data
        columns = ("Task ID", "Time", "Machine", "Material", "Speed", "Status")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        
        # Headings
        self.tree.heading("Task ID", text="Task ID")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Machine", text="Machine")
        self.tree.heading("Material", text="Material")
        self.tree.heading("Speed", text="Speed")
        self.tree.heading("Status", text="Status")

        # Column widths
        self.tree.column("Task ID", width=100)
        self.tree.column("Time", width=100)
        self.tree.column("Machine", width=100)
        self.tree.column("Material", width=100)
        self.tree.column("Speed", width=100)
        self.tree.column("Status", width=100)

        # Add a scrollbar
        self.scrollbar = ttk.Scrollbar(self.tree, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Add the table to the main frame
        self.tree.pack(fill=tk.BOTH, expand=True)



    # Buttons for creating, modifying, and deleting tasks
    def _create_buttons(self):
        # Create a frame for buttons
        self.button_frame = ttk.Frame(self.main_frame, padding=10)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # TODO: Find a way to make this less redundant
        # TODO: Make it look better
        self.create_button = tk.Button(self.button_frame, text="Create task",
                bg="green", font=('Arial', 20), padx=5, pady=5,
                command=lambda: self._on_create_task() if self._on_create_task else None)

        self.modify_button = tk.Button(self.button_frame, text="Modify task",
                bg="yellow", font=('Arial', 20), padx=5, pady=5,
                command=lambda: self._on_modify_task() if self._on_modify_task else None)
        
        self.delete_button = tk.Button(self.button_frame, text="Delete task",
                bg="red", font=('Arial', 20), padx=5, pady=5,
                command=lambda: self._on_delete_task() if self._on_delete_task else None)

        # Pack buttons
        self.create_button.pack(side=tk.LEFT, padx=5)
        self.modify_button.pack(side=tk.LEFT, padx=5, expand=True)  # Expand to fill space (center)
        self.delete_button.pack(side=tk.RIGHT, padx=5)


    # Fill the table with data
    def populate_table(self, tasks):
        """Populate the table with the tasks"""
        for task in tasks:
            self.tree.insert("", tk.END, values=task)

    def add_task_to_table(self, task):
        """Insert the task to be seen on the table"""
        self.tree.insert("", tk.END, values=task)

    def modify_task_in_table(self, task_id, updated_task):
        """Modify the selected task as it appears on the table"""
        for item in self.tree.get_children():
            # Check that the ID matches
            if self.tree.item(item, "values")[0] == task_id:
                self.tree.item(item, values=updated_task)
                break

    def delete_task_from_table(self, task_id):
        """Delete the selected task from the table"""
        for item in self.tree.get_children():
            if self.tree.item(item, "values")[0] == task_id:
                self.tree.delete(item)
                break


    # Callbacks for button clicks
    def set_on_create_task(self, callback):
        self._on_create_task = callback

    def set_on_modify_task(self, callback):
        self._on_modify_task = callback

    def set_on_delete_task(self, callback):
        self._on_delete_task = callback