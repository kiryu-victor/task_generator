from datetime import datetime

class TaskModel:
    def __init__(self):
        self.task_id = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.task_start_time = self.task_id
        self.task_machine = None
        self.task_material = None
        self.task_speed = None
        self.task_end_time = ""
        self.task_status = "Pending"