import tkinter as tk
from tkinter import ttk
from utils.utils import Utils


class ModifyTaskView(tk.Toplevel):
    def __init__(self, root, task):
        """Create a new window for modifying tasks"""
        super().__init__(root)
        self.title("Modify task")
        self.geometry("360x240")
        self.resizable(False, False)
        
        # Center the window on the screen
        Utils.center_window_on_screen(self, 360, 240)

        # Create a modal window
        self.grab_set()
        self.transient(root)
        self.focus_set()

        # Create a frame for the task creation form
        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Callbacks
        self._on_modify_task = None
        self._on_machine_change = None

        # Create the elements of the task creation form
        self._create_form_elements()
        self._create_buttons()

    # Callbacks for events
    def set_on_modify_task(self, callback):
        """Callback for a click on the modify task button"""
        self._on_modify_task = callback

    def set_on_machine_type_change(self, callback):
        """ Callback for the machine type change."""
        self._on_machine_change = callback


    # Create the elements for the modification menu
    def _create_form_elements(self):
        """Create the elements of the task modification form
        Old values will be showing on the left side
        New values will be input on the right side"""
        # Create a frame for the task creation form
        self.form_frame = ttk.Frame(self.main_frame, padding=10)
        self.form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Heading
        self.old_values_label = ttk.Label(self.form_frame, text="Old value")
        self.old_values_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        # Vertical separator between the old and new values
        ttk.Separator(self.form_frame, orient="vertical").grid(row=0, column=2,
                rowspan=4, sticky=tk.NS
		)
        self.new_values_label = ttk.Label(self.form_frame, text="New value")
        self.new_values_label.grid(row=0, column=3, sticky=tk.E, padx=5, pady=5)
        
        # Machine type
        self.machine_label = ttk.Label(self.form_frame, text="Machine")
        self.machine_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.machine_old_value = ttk.Label(self.form_frame)
        self.machine_old_value.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        self.machine_combo = ttk.Combobox(self.form_frame, state="readonly",
                values=["Machine A", "Machine B", "Machine C"]
		)
        self.machine_combo.bind("<<ComboboxSelected>>",
                lambda e: self._on_machine_type_change(self.machine_combo.get())
                        if self._on_machine_change else None
		)        
        self.machine_combo.grid(row=1, column=3, sticky=tk.EW, padx=5, pady=5)

        # Materials
        self.material_label = ttk.Label(self.form_frame, text="Material")
        self.material_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        self.material_old_value = ttk.Label(self.form_frame)
        self.material_old_value.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        # The materials available depend on the machine type selected
        self.material_combo = ttk.Combobox(self.form_frame, state="readonly",)
        self.material_combo.grid(row=2, column=3, sticky=tk.EW, padx=5, pady=5)

        # Speed (RPM)
        self.speed_label = ttk.Label(self.form_frame, text="Speed (RPM)")
        self.speed_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        self.speed_old_value = ttk.Label(self.form_frame)
        self.speed_old_value.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        self.speed_entry = ttk.Entry(self.form_frame)
        self.speed_entry.grid(row=3, column=3, sticky=tk.EW, padx=5, pady=5)

    # On the event of the machine type being changed
    def _on_machine_type_change(self, event=None):
        """Handle machine type change event."""
        if self._on_machine_change:
            self._on_machine_change(self.machine_combo.get())

    # Create buttosn after the form
    def _create_buttons(self):
        """Create the buttons for the task creation form"""
        # Create a frame for buttons
        self.button_frame = ttk.Frame(self.main_frame, padding=10)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM) # , expand=True

        # Accept task modification button
        self.modify_button = tk.Button(self.button_frame, text="Modify",
                font=("Arial", 18), padx=5, pady=5, bg="#ffcf69",
                command=lambda: self._on_modify_task()
                        if self._on_modify_task else None
		)
        
        # Cancel task modification button
        self.cancel_button = tk.Button(self.button_frame, text="Cancel",
                font=("Arial", 18), padx=5, pady=5,
                command=self.destroy
		)

        # Pack buttons
        self.modify_button.pack(side=tk.LEFT, padx=5)
        self.cancel_button.pack(side=tk.RIGHT, padx=10)


    def set_old_values(self, machine, material, speed):
        """Set the old values """
        self.machine_old_value.config(text=machine)
        self.material_old_value.config(text=material)
        self.speed_old_value.config(text=speed)