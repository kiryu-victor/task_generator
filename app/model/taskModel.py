from datetime import datetime

class TaskModel:
    def __init__(self, machine=None, material=None, speed=None, time_left=0):
        self.task_id = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.task_machine = machine
        self.task_material = material
        self.task_speed = speed
        self.task_time_left = time_left
        self.task_status = "Pending"