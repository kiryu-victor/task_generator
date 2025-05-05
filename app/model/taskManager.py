from collections import defaultdict
from threading import Timer

import csv

class TaskManager:
    def __init__(self, csv_file_path="./reports/tasks.csv"):
        self.csv_path = csv_file_path
        self.tasks = self._load_tasks_from_csv()
        self.is_modified = False
        # New queue for each machine handled like a dictionary, where:
            # keys = machine
            # values = list of tasks on queue
        self.machine_queues = defaultdict(list)
        # Timer for each task
        self.timer = {}

    def _load_tasks_from_csv(self):
        """Load the tasks from the CSV file"""
        try:
            # Open the file in read mode
            with open(self.csv_path, mode="r") as file:
                reader = csv.reader(file)
                tasks = []
                # Append each row (task) on tasks
                for row in reader:
                    if len(row) < 6:
                        row.append("0")
                    tasks.append(row)
                return tasks
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            return []
        except csv.Error as e:
            print(f"CSV error ocurred while loading the tasks: {e}")
        except IOError as e:
            print(f"IO error occurred while loading the tasks: {e}")

    def _save_tasks_to_csv(self):
        """Save the tasks to the CSV file"""
        if self.is_modified:
            try:
                # Open the file in write mode
                with open(self.csv_path, mode="w", newline='') as file:
                    writer = csv.writer(file)
                    for task in self.tasks:
                        if len(task) < 7:
                            task.append("0")
                        writer.writerow(task)
                    self.is_modified = False
            except csv.Error as e:
                print(f"CSV error occurred while saving tasks: {e}")
            except IOError as e:
                print(f"IO error occurred while saving tasks: {e}")

    def sort_tasks(self, column, ascending=True):
        """Sort the table by the name"""
        # Columns mapped to their indices
        column_indices = {
            "Task ID": 0,
            "Time": 1,
            "Machine": 2,
            "Material": 3,
            "Speed": 4,
            "Status": 5
        }
        
        column_index = column_indices[column]

        # Sorting
        try:
            sorted_tasks = sorted(
                self.tasks, # Sort the tasks
                key=lambda task: task[column_index],    # By their index
                reverse=not ascending   # In the order indicated by ascending
            )
            return sorted_tasks
        except IndexError:
            raise ValueError(f"Index {column_index} out of range")

    def add_task(self, task):
        """Add the task"""
        machine = task[2]
        if len(task) < 7:
            task.append("0")
        self.tasks.append(task)
        self.is_modified = True

        # Add the task to the queue
        self.machine_queues[machine].append(task)

        # If it's the only task on the queue, start it
        if len(self.machine_queues[machine]) == 1:
            self._start_task(task)

    def modify_task(self, task_id, modified_task):
        """Modify the task"""
        # Loop through the tasks
        for i, task in enumerate(self.tasks):
            if task[0] == task_id:  # To find the task_id we want to modify
                if len(modified_task) < 6:
                    modified_task.append(task[5])
                self.tasks[i] = modified_task   # Modify it
                self.is_modified = True
                break

    def delete_task(self, task_id):
        """Delete the task"""
        # Loop through the tasks
        for i, task in enumerate(self.tasks):
            if task[0] == task_id:  # To find the task_id we want to delete
                machine = task[2]
                if task_id in self.timer:
                    # Stop and delete the task from the timer
                    self.timer[task_id].cancel()
                    del self.timer[task_id]

                # Delete the task from the queue by looking for all the ones
                # that are not equal to the one being deleted, keeping them
                self.machine_queues[machine] = [
                    task for task in self.machine_queues[machine] if task[0] != task_id
                ]
                
                self.is_modified = True
                del self.tasks[i]
                break

    def _start_task(self, task):
        """Start a given task from the queue"""
        task_id = task[0]
        machine = task[2]
        task[5] = str(task[6])
        
        def decrement_time():
            if int(task[6]) > 0:
                task[6] = str(int(task[6]) - 1)
                task[5] = task[6]
                self.is_modified = True
                self.timer[task_id] = Timer(1, decrement_time)
                self.timer[task_id].start()
            else:
                task[5] = "Completed"
                self.is_modified = True
                self.timer.pop(task_id, None)
                self._save_tasks_to_csv()

                self.machine_queues[machine].pop(0)
                if self.machine_queues[machine]:
                    self._start_task(self.machine_queues[machine][0])

        decrement_time()


    def get_tasks(self):
        return self.tasks

    def save_tasks(self):
        self._save_tasks_to_csv()