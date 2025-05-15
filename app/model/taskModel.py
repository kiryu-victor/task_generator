from datetime import datetime

class TaskModel:
    def __init__(self, task_id=None, timestamp_start=None,
                machine=None, material=None, speed=None,
                status="On queue", time_left=None, expected_time=None):
        self.task_id = task_id or datetime.now().strftime("%Y%m%d-%H%M%S")
        self.timestamp_start = timestamp_start or datetime.now().strftime("%H:%M:%S")
        self.machine = machine
        self.material = material
        self.speed = speed
        self.status = status
        self.time_left = time_left
        self.expected_time = expected_time


    def to_tuple(self):
        """Turn the task into a tuple."""
        return (
            self.task_id,
            str(self.timestamp_start),
            self.machine,
            self.material,
            self.speed,
            self.status,
            self.time_left,
            str(self.expected_time),
        )
