import tkinter as tk
from tkinter import ttk

from utils.utils import Utils


class ModifyTaskView(tk.Toplevel):
    def __init__(self, root):
        """Create a new window for modifying tasks"""
        super().__init__(root)
        self.title("Modify task")
        self.geometry("420x240")
        self.resizable(False, False)
        
        # Center the window on the screen
        Utils.center_window_on_screen(self, 420, 240)

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
        self._on_material_change = None

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

    def set_on_material_change(self, callback):
        """Callback for the material change."""
        self._on_material_change = callback

    # Create the elements for the modification menu
    def _create_form_elements(self):
        """Create the elements of the task modification form
        current values will be showing on the left side
        New values will be input on the right side"""
        # Create a frame for the task creation form
        self.form_frame = ttk.Frame(self.main_frame, padding=10)
        self.form_frame.pack(fill=tk.BOTH, expand=True)

        # Configure columns so they stay fixed
        self.form_frame.grid_columnconfigure(0, weight=0, minsize=80)
        self.form_frame.grid_columnconfigure(1, weight=0, minsize=125)
        self.form_frame.grid_columnconfigure(2, weight=0, minsize=10)
        self.form_frame.grid_columnconfigure(3, weight=0, minsize=125)
        
        # Heading
        self.current_values_label = ttk.Label(self.form_frame, text="Current value")
        self.current_values_label.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        # Vertical separator between the current and new values
        ttk.Separator(self.form_frame, orient="vertical").grid(
                row=0, column=2, rowspan=4, sticky=tk.NS
		)
        self.new_values_label = ttk.Label(self.form_frame, text="New value")
        self.new_values_label.grid(row=0, column=3, sticky=tk.E, padx=5, pady=5)
        
        # Machine type
        self.machine_label = ttk.Label(self.form_frame, text="Machine")
        self.machine_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.machine_current_value = ttk.Label(self.form_frame)
        self.machine_current_value.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        self.machine_combo = ttk.Combobox(self.form_frame, state="readonly")
        self.machine_combo.bind("<<ComboboxSelected>>",
                lambda e: self._on_machine_change(self.machine_combo.get())
                        if self._on_machine_change else None
		)        
        self.machine_combo.grid(row=1, column=3, sticky=tk.EW, padx=5, pady=5)

        # Materials
        self.material_label = ttk.Label(self.form_frame, text="Material")
        self.material_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        self.material_current_value = ttk.Label(self.form_frame)
        self.material_current_value.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        # The materials available depend on the machine type selected
        self.material_combo = ttk.Combobox(self.form_frame, state="readonly",)
        self.material_combo.grid(row=2, column=3, sticky=tk.EW, padx=5, pady=5)
        # Bind material combo to material change event
        self.material_combo.bind("<<ComboboxSelected>>",
                lambda e: self._on_material_change(self.material_combo.get())
                        if self._on_material_change else None
        )

        # Speed (SMM)
        self.speed_label = ttk.Label(self.form_frame, text="Speed (SMM)")
        self.speed_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        self.speed_current_value = ttk.Label(self.form_frame)
        self.speed_current_value.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        self.speed_entry = ttk.Entry(self.form_frame)
        self.speed_entry.grid(row=3, column=3, sticky=tk.EW, padx=5, pady=5)

        self.speed_range_label = ttk.Label(self.form_frame, text="")
        self.speed_range_label.grid(
                row=4, column=3, sticky=tk.EW, padx=5, pady=5,
        )

        self.form_frame.columnconfigure(0, weight=1)
        self.form_frame.columnconfigure(1, weight=1)

    # Create buttosn after the form
    def _create_buttons(self):
        """Create the buttons for the task creation form"""
        # Create a frame for buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM) # , expand=True

        # Accept task modification button
        self.modify_button = tk.Button(self.button_frame, text="Modify",
                font=("Arial", 18), padx=10, pady=5, bg="#E1BC29",
                command=lambda: self._on_modify_task()
                        if self._on_modify_task else None
		)
        
        # Cancel task modification button
        self.cancel_button = tk.Button(self.button_frame, text="Cancel",
                font=("Arial", 18), padx=10, pady=5, bg="#505050", fg="#e3e3e3",
                command=self.destroy
		)

        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)

        # Pack buttons
        self.modify_button.pack(side=tk.LEFT, padx=15)
        self.cancel_button.pack(side=tk.RIGHT, padx=15)