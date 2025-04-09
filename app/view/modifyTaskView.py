import tkinter as tk
from tkinter import ttk

class ModifyTaskView(tk.Toplevel):
    def __init__(self, root, task):
        """Create a new window for modifying tasks"""
        super().__init__(root)
        self.title("Modify task")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Create a modal window
        self.grab_set()
        self.transient(root)
        self.focus_set()

        # Create a frame for the task creation form
        self.form_frame = ttk.Frame(self, padding=10)
        self.form_frame.pack(fill=tk.BOTH, expand=True)

        # Callbacks
        self._on_task_selected = None
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


    # Genera los elementos de crear un formulario de modificacion
    def _create_form_elements(self):
        """Create the elements of the task creation form"""
        # Machine type
        self.machine_label = ttk.Label(self.form_frame, text="Machine")
        self.machine_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.machine_combo = ttk.Combobox(self.form_frame,
                values=["Machine A", "Machine B", "Machine C"])
        self.machine_combo.bind("<<ComboboxSelected>>",
                lambda e: self._on_machine_type_change(self.machine_combo.get())
                        if self._on_machine_change else None)        
        self.machine_combo.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        # Materials
        # The materials available depend on the machine type selected
        self.material_label = ttk.Label(self.form_frame, text="Material")
        self.material_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.material_combo = ttk.Combobox(self.form_frame)
        self.material_combo.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        # Speed (RPM)
        self.speed_label = ttk.Label(self.form_frame, text="Speed (RPM)")
        self.speed_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.speed_entry = ttk.Entry(self.form_frame)
        self.speed_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

    # On the event of the machine type being changed
    def _on_machine_type_change(self, event=None):
        """Handle machine type change event."""
        if self._on_machine_change:
            self._on_machine_change(self.machine_combo.get())

    # Create buttosn after the form
    def _create_buttons(self):
        """Create the buttons for the task creation form"""
        # Create a frame for buttons
        self.button_frame = ttk.Frame(self.form_frame, padding=10)
        self.button_frame.grid(row=3, column=0, columnspan=2, sticky=tk.EW)

        # Accept task modification button
        self.modify_button = ttk.Button(self.form_frame, text="Modify",
                command=lambda: self._on_modify_task()
                        if self._on_modify_task else None)
        self.modify_button.grid(row=4, column=0, sticky=tk.EW, padx=5, pady=5)
        # Cancel task modification button
        self.cancel_button = ttk.Button(self.form_frame, text="Cancel",
                command=self.destroy)
        self.cancel_button.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)