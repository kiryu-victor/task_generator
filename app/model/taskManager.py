import asyncio
import json
import websockets

from model.taskModel import TaskModel

class TaskManager:
    def __init__(self, db_manager, websocket_server=None):
        self.db_manager = db_manager
        self.websocket_server = websocket_server

    def sort_tasks(self, column, ascending=True):
        """Sort the table by the name"""
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

        # Get DB column name
        db_column = column_mapping[column]

        # Order
        order = "ASC" if ascending else "DESC"

        # Query to get and sort the tasks
        query = f"SELECT * FROM tasks ORDER BY {db_column} {order}"
        result = self.db_manager.execute_query(query)

        return result

    # CRUD methods
    def create_task(self, task_model):
        """Add the task to the database"""
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
                        )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """
            self.db_manager.execute_query(query, task_model.to_tuple())
            
            # Notify the Webscoket clients
            if self.websocket_server:
                message = json.dumps({
                        "action": "create",
                        "task": task_model.to_tuple()
                })
                asyncio.create_task(self.websocket_server.broadcast(message))                
        except Exception as e:
            print(f"Error creating task: {e}")
            raise RuntimeError("Failed to create the task")

    def read_task(self, task_id):
        """Read a specified task"""
        try:
            query = "SELECT * FROM tasks WHERE task_id = ?"
            result = self.db_manager.execute_query(query, (task_id,))
            # return result
            if result:
                return TaskModel.from_tuple(result[0])
            return None
    
        except Exception as e:
            print(f"Error reading task: {e}")
            raise RuntimeError("Failed to read the task")

    def update_task(self, task_id, modified_fields_tuple):
        """Modify the task on the database"""
        try:
            # Query updating the selected task
            query = """
                    UPDATE tasks
                    SET machine = ?,
                        material = ?,
                        speed = ?
                    WHERE task_id = ?
                    """            
            self.db_manager.execute_query(query, modified_fields_tuple)

            task = self.read_task(task_id)
            # Notify websocket clients
            if self.websocket_server:
                message = json.dumps({
                        "action": "update",
                        "task_id": task_id,
                        "task": task.to_tuple(),
                })
                asyncio.create_task(self.websocket_server.broadcast(message))
        except Exception as e:
            print(f"Error updating task witd ID {task_id}: {e}")
            raise RuntimeError("Failed to update the task")

    def delete_task(self, task_id):
        """Delete the selected task on the database"""
        try:
            query = "DELETE FROM tasks WHERE task_id = ?"
            self.db_manager.execute_query(query, (task_id,))
            
            # Notify websocket clients
            if self.websocket_server:
                message = json.dumps({
                        "action": "delete",
                        "task_id": task_id,
                })
                asyncio.create_task(self.websocket_server.broadcast(message))
        except Exception as e:
            print(f"Error deleting task with ID {task_id}: {e}")
            raise RuntimeError("Failed to delete the task")

    # Other methods
    def get_all_tasks(self):
        """Get all the tasks from the table"""
        try:
            query = "SELECT * FROM tasks"
            result = self.db_manager.execute_query(query)
            return result
        except Exception as e:
            print(f"Error getting all the tasks: {e}")
            raise RuntimeError("Failed to fetch the tasks")
    
    def update_task_status(self, task_id, new_status):
        """Update the status of a task to a new one in the database"""
        try:
            query = "UPDATE task SET status = ? WHERE task_id = ?"
            self.db_manager.execute_query(query, (new_status, task_id))

            if self.websocket_server:
                message = json.dumps({
                        "action": "status_update",
                        "task_id": task_id,
                        "status": new_status
                })
                asyncio.create_task(self.websocket_server.broadcast(message))
        except Exception as e:
            print(f"Error udating status on task ID {task_id}: {e}")
            raise RuntimeError("Failed toupdating task status")