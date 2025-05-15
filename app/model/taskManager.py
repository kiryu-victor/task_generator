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
                        expected_time
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

    def update_task(self, modified_fields_tuple):
        """
        Modifies the task on the DB.
        Requires a tuple with the values of the fields that are modified.
        """
        try:
            query = """
                    UPDATE tasks
                    SET machine = ?,
                        material = ?,
                        speed = ?
                    WHERE task_id = ?
                    """
            self.db_manager.execute_query(query, modified_fields_tuple)
        except Exception as e:
            print(f"Error udpating task: {e}")
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

    def update_task_status(self, task_id, new_status):
        """Updates a task status on the DB."""
        try:
            query = "UPDATE task SET status = ? WHERE taks_id = ?"
            self.db_manager.execute_query(query, (new_status, task_id))
        except Exception as e:
            print(f"Error udpating the task status: {e}")
            raise RuntimeError("Failed to update the task status")


    # Other functions
    def sort_tasks(self, column, ascending=True):
        """Sort the table by the selected column."""
        # Columns mapped to their indices
        column_mapping = {
            "Task ID": "task_id",
            "Time": "timestamp_start",
            "Machine": "machine",
            "Material": "material",
            "Speed": "speed",
            "Status": "status",
            "Time left": "time_left"
        }
        
        if column not in column_mapping:
            raise ValueError(f"Invalid column name: {column}")

        # Get the column name
        db_column = column_mapping[column]

        # Order
        order = "ASC" if ascending else "DESC"

        # Get the SELECT sorted
        query = f"SELECT * FROM tasks ORDER BY {db_column} {order}"
        result = self.db_manager.execute_query(query)

        return result