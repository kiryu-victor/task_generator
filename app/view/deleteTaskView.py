import tkinter as tk
from tkinter import ttk

from utils.utils import Utils


class DeleteTaskView(tk.Toplevel):
	def __init__(self, root):
		super().__init__(root)
		self.title("Delete task")
		self.geometry("240x300")
		self.resizable(False, False)

		# Center the window on the screen
		Utils.center_window_on_screen(self, 240, 300)

		# Make it a modal window
		self.grab_set()
		self.transient(root)
		self.focus_set()

		self.main_frame = ttk.Frame(self, padding=10)
		self.main_frame.pack(fill=tk.BOTH, expand=True)

		# Callbacks
		self._on_delete_task = None

		# Create the elements of the task deletion form
		self._create_form_elements()
		self._create_buttons()


	# Callbacks for events
	def set_on_delete_task(self, callback):
		self._on_delete_task = callback


	def _create_form_elements(self):
		"""Create the elements of the task deletion form.
		Labels on the left.
		Values on the right."""
		# Create a frame for the task creation form
		self.form_frame = ttk.Frame(self.main_frame, padding=10)
		self.form_frame.pack(fill=tk.BOTH, expand=True)
		
		self.id_label = ttk.Label(self.form_frame, text="ID")
		self.id_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
		self.id_selected = ttk.Label(self.form_frame)
		self.id_selected.grid(row=0, column=1, sticky=tk.E, padx=5, pady=5)
		
		self.date_created_label = ttk.Label(self.form_frame,
				text="Date created"
		)
		self.date_created_label.grid(row=1, column=0, sticky=tk.W,
				padx=5, pady=5
		)
		self.date_created_selected = ttk.Label(self.form_frame)
		self.date_created_selected.grid(row=1, column=1, sticky=tk.E,
				padx=5, pady=5
		)
		
		self.machine_label = ttk.Label(self.form_frame, text="Machine")
		self.machine_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
		self.machine_selected = ttk.Label(self.form_frame)
		self.machine_selected.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)
		
		self.material_label = ttk.Label(self.form_frame, text="Material")
		self.material_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
		self.material_selected = ttk.Label(self.form_frame)
		self.material_selected.grid(row=3, column=1, sticky=tk.E, padx=5, pady=5)
		
		self.speed_label = ttk.Label(self.form_frame, text="Speed")
		self.speed_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
		self.speed_selected = ttk.Label(self.form_frame)
		self.speed_selected.grid(row=4, column=1, sticky=tk.E, padx=5, pady=5)
		
		self.status_label = ttk.Label(self.form_frame, text="Status")
		self.status_label.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
		self.status_selected = ttk.Label(self.form_frame)
		self.status_selected.grid(row=5, column=1, sticky=tk.E, padx=5, pady=5)


	def _create_buttons(self):
		self.button_frame = ttk.Frame(self.main_frame, padding=10)
		self.button_frame.pack(fill=tk.X, side=tk.BOTTOM)

		self.delete_button = tk.Button(self.button_frame, text="Delete",
				font=("Arial", 16), padx=5, pady=5, bg="#F15152",
				command=lambda: self._on_delete_task()
						if self._on_delete_task else None
		)
		self.delete_button.grid(row=4, column=0, sticky=tk.EW, padx=5, pady=5)

		self.cancel_button = tk.Button(self.button_frame, text="Cancel",
				font=("Arial", 16), padx=5, pady=5, bg="#505050", fg="#e3e3e3",
				command=self.destroy
		)

		# Pack buttons
		self.delete_button.pack(side=tk.LEFT, padx=5)
		self.cancel_button.pack(side=tk.RIGHT, padx=10)