import tkinter as tk
from tkinter import ttk
from utils.utils import Utils

class CreateTaskView(tk.Toplevel):
	def __init__(self, root):
		"""Create a new window for creating tasks"""
		super().__init__(root)
		self.title("Create task")
		self.geometry("260x210")
		self.resizable(False, False)

		# Center the window on the screen
		Utils.center_window_on_screen(self, 260, 210)

		# Make the window modal
		self.grab_set()
		self.transient(root)
		self.focus_set()

		# Create a frame for the task creation form
		self.form_frame = ttk.Frame(self, padding=10)
		self.form_frame.pack(fill=tk.BOTH, expand=True)

		# Callbacks
		self._on_task_selected = None
		self._on_create_task = None
		self._on_machine_change = None
		self._on_material_change = None

		# Create the elements of the task creation form
		self._create_form_elements()
		self._create_buttons()

	# Callbacks for events
	def set_on_create_task(self, callback):
		"""Callback for a click on the create task button"""
		self._on_create_task = callback

	def set_on_machine_type_change(self, callback):
		""" Callback for the machine type change."""
		self._on_machine_change = callback

	def set_on_material_change(self, callback):
		"""Callback for the material change."""
		self._on_material_change = callback

	# Generating elements for the form in the new window
	def _create_form_elements(self):
		"""Create the elements of the task creation form"""
		# Machine type
		self.machine_label = ttk.Label(self.form_frame, text="Machine")
		self.machine_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
		self.machine_combo = ttk.Combobox(
				self.form_frame,
				state="readonly",
				values=[]
		)
		self.machine_combo.bind("<<ComboboxSelected>>",
				lambda e: self._on_machine_change(self.machine_combo.get())
						if self._on_machine_change else None
		)        
		self.machine_combo.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

		# Materials
		# The materials available depend on the machine type selected
		self.material_label = ttk.Label(self.form_frame, text="Material")
		self.material_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
		self.material_combo = ttk.Combobox(self.form_frame, state="readonly")
		self.material_combo.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
		self.material_combo.bind("<<ComboboxSelected>>",
				lambda e: self._on_material_change(self.material_combo.get())
						if self._on_material_change else None
		)

		# Speed (SMM)
		self.speed_label = ttk.Label(self.form_frame, text="Speed (SMM)")
		self.speed_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
		
		self.speed_entry = ttk.Entry(self.form_frame)
		self.speed_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
		
		self.speed_range_label = ttk.Label(self.form_frame, text="")
		self.speed_range_label.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)

	# Create buttons after the form
	def _create_buttons(self):
		"""Create the buttons for the task creation form"""
		# Create a frame for buttons
		self.button_frame = ttk.Frame(self.form_frame)
		self.button_frame.grid(row=4, column=0, columnspan=2,
				sticky=tk.EW, pady=10
		)

		# Accept task creation button
		self.create_button = tk.Button(self.button_frame, text="Accept",
				font=("Arial", 16), padx=10, pady=5, bg="#7fff69",
				command=lambda: self._on_create_task()
						if self._on_create_task else None
		)
		# Cancel task creation button
		self.cancel_button = tk.Button(self.button_frame, text="Cancel",
				font=("Arial", 16), padx=10, pady=5,
				command=self.destroy
		)

		# Pack buttons
		self.create_button.pack(side=tk.LEFT, padx=5)
		self.cancel_button.pack(side=tk.RIGHT, padx=5)