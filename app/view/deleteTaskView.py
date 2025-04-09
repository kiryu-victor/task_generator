import tkinter as tk
from tkinter import ttk

class DeleteTaskView(tk.Toplevel):
	def __init__(self, root, task):
		super().__init__(root)
		self.title("Delete task")
		self.geometry("400x300")
		self.resizable(False, False)

		# Make it a modal window
		self.grab_set()
		self.transient(root)
		self.focus_set()

		self.form_frame = ttk.Frame(self, padding=10)
		self.form_frame.pack(fill=tk.BOTH, expand=True)

		# Callbacks
		self._on_task_selected = None
		self._on_delete_task = None

		# Create the elements of the task deletion form
		self._create_form_elements()
		self._create_buttons()


	# Callbacks for events
	def set_on_delete_task(self, callback):
		self._on_delete_task = callback


	# Elements for the form
	def _create_form_elements(self):
		self.machine_label = ttk.Label(self.form_frame, text="Machine").grid(
				row=0, column=0, sticky=tk.W, padx=5, pady=5)
		self.machine_selected = ttk.Label(self.form_frame, text="Cambiar texto").grid(
				row=0, column=0, sticky=tk.EW, padx=5, pady=5)
		
		self.material_label = ttk.Label(self.form_frame, text="Material").grid(
				row=1, column=0, sticky=tk.W, padx=5, pady=5)
		self.material_selected = ttk.Label(self.form_frame, text="Cambiar texto").grid(
				row=1, column=1, sticky=tk.EW, padx=5, pady=5)
		
		self.speed_label = ttk.Label(self.form_frame, text="Speed").grid(
				row=2, column=0, sticky=tk.W, padx=5, pady=5)
		self.speed_selected = ttk.Label(self.form_frame, text="Cambiar texto").grid(
				row=2, column=1, sticky=tk.EW, padx=5, pady=5)

	def _create_buttons(self):
		self.button_frame = ttk.Frame(self.form_frame, padding=10).grid(
				row=3, column=1, sticky=tk.EW)

		self.delete_button = ttk.Button(self.form_frame, text="Delete",
				command=lambda: self._on_delete_task()
						if self._on_delete_task else None)
		self.delete_button.grid(row=4, column=0, sticky=tk.EW, padx=5, pady=5)

		self.cancel_button = ttk.Button(self.form_frame, text="Cancel",
				command=self.destroy)
		self.cancel_button.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)