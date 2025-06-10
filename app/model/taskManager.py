from datetime import datetime, timedelta
from model.taskModel import TaskModel


class TaskManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager


    # Basic CRUD functions
    def create_task(self, task_model):
        """Create a task on the DB."""
        try:
            query = """
                    INSERT INTO tasks (
                        task_id,
                        timestamp_start,
                        machine,
                        material,
                        speed,
                        status,
                        time_left,
                        timestamp_expected_complete
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """
            self.db_manager.execute_query(query, task_model.to_tuple())
        except Exception as e:
            print(f"Error creating a task: {e}")
            raise RuntimeError("Failed to create the task")

    def read_task(self, task_id):
        """Reads a selected task from the DB and returns it."""
        try:
            query = "SELECT * FROM tasks WHERE task_id = ?"
            result = self.db_manager.execute_query(query, (task_id,))
            # Convert this list into a TaskModel and return it
            task = TaskModel(
                result[0][0],
                result[0][1],
                result[0][2],
                result[0][3],
                result[0][4],
                result[0][5],
                result[0][6],
                result[0][7],
            )
            return task
        except Exception as e:
            print(f"Error reading task: {e}")
            raise RuntimeError("Failed to read the task")

    def update_task(self, params_dict):
        """
        Modifies the task on the DB.
        Requires a tuple with the values of the fields that are modified.
        """
        params_tuple = (
                params_dict["machine"],
                params_dict["material"],
                params_dict["speed"],
                params_dict["task_id"],
        )
        try:
            query = """
                    UPDATE tasks
                    SET machine = ?,
                        material = ?,
                        speed = ?
                    WHERE task_id = ?
                    """
            self.db_manager.execute_query(query, params_tuple)
        except Exception as e:
            print(f"Error updating task: {e}")
            raise RuntimeError("Failed to update the task")

    def delete_task(self, task_id):
        """Deletes the task from the DB."""
        try:
            query = """DELETE FROM tasks WHERE task_id = ?"""
            self.db_manager.execute_query(query, (task_id,))
        except Exception as e:
            print(f"Error deleting task: {e}")
            raise RuntimeError("Failed to delete the task")


    # Other CRUD related functions
    def read_all_tasks(self):
        """Reads all the tasks on the DB and returns them."""
        try:
            query = "SELECT * FROM tasks"
            result = self.db_manager.execute_query(query)
            return result
        except Exception as e:
            print(f"Error fetching all the tasks: {e}")
            raise RuntimeError("Failed to fetch all the tasks")
        
    def update_task_start_parameters(self, time_left, task_id):
        """Updates a tasks timestamp_start, status and timestamp_expected_complete."""
        now = datetime.now()
        try:
            query = "UPDATE tasks SET timestamp_start = ?, status = ?, timestamp_expected_complete = ? WHERE task_id = ?"
            self.db_manager.execute_query(query, (now, "In progress", now + timedelta(seconds=time_left), task_id))
        except Exception as e:
            print(f"Error updating the task start parameters: {e}")
            raise RuntimeError("Failed to update the task status")
        
    def update_task_time_left(self, task_id, time_left):
        """Updates a tasks timestamp_start and status."""
        try:
            query = "UPDATE tasks SET time_left = ? WHERE task_id = ?"
            self.db_manager.execute_query(query, (time_left, task_id))
        except Exception as e:
            print(f"Error updating the task time left: {e}")
            raise RuntimeError("Failed to update the task status")

    def udpate_task_complete(self, task_id):
        """Updates a tasks status to "Complete" """
        try:
            query = "UPDATE tasks SET status = 'Complete', time_left = '', timestamp_expected_complete = ? WHERE task_id = ?"
            self.db_manager.execute_query(query, (datetime.now(), task_id))
        except Exception as e:
            print(f"Error updating the task time left: {e}")
            raise RuntimeError("Failed to update the task status")
