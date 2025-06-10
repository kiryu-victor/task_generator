from datetime import datetime


class TaskModel:
    def __init__(self, task_id=None, timestamp_start=None,
                machine=None, material=None, speed=None,
                status="On queue", time_left=None, timestamp_expected_complete=None):
        self.task_id = task_id or datetime.now().strftime("%Y%m%d-%H%M%S")
        self.timestamp_start = timestamp_start or ""
        self.machine = machine
        self.material = material
        self.speed = speed
        # String status
        self.status = status
        # Time that's left (int - seconds)
        self.time_left = time_left
        # Time ex
        self.timestamp_expected_complete = timestamp_expected_complete


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
            str(self.timestamp_expected_complete),
        )