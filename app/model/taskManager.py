import csv

class TaskManager:
    def __init__(self, csv_file_path="./reports/tasks.csv"):
        self.csv_path = csv_file_path
        self.tasks = self._load_tasks_from_csv()
        self.is_modified = False

    def _load_tasks_from_csv(self):
        """Load the tasks from the CSV file"""
        try:
            with open(self.csv_path, mode="r") as file:
                reader = csv.reader(file)
                return [row for row in reader]
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")

    def _save_tasks_to_csv(self):
        """Save the tasks to the CSV file"""
        if self.is_modified:
            try:
                with open(self.csv_path, mode="w", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(self.tasks)
                self.is_modified = False
            except Exception as e:
                print(f"An error occurred while saving tasks: {e}")

    def add_task(self, task):
        self.tasks.append(task)
        self.is_modified = True

    def modify_task(self, task_id, modified_task):
        # Loop through the tasks
        for i, task in enumerate(self.tasks):
            if task[0] == task_id:  # To find the task_id we want to modify
                self.tasks[i] = modified_task   # Modify it
                self.is_modified = True
                break

    def delete_task(self, task_id):
        # Loop through the tasks
        for i, task in enumerate(self.tasks):
            if task[0] == task_id:  # To find the task_id we want to delete
                self.is_modified = True
                del self.tasks[i]
                break

    def get_tasks(self):
        return self.tasks

    def save_tasks(self):
        self._save_tasks_to_csv()