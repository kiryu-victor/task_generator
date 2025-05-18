import sqlite3


class DatabaseManager:
    def __init__(self, db_path="tasks.db"):
        self.db_path = db_path
        self.initialize_database()


    def initialize_database(self):
        """Create the file for the database. Initializes it if needed."""
        try:
            query = """
                    CREATE TABLE IF NOT EXISTS tasks (
                        task_id TEXT PRIMARY_KEY,
                        timestamp_start DATETIME,
                        machine TEXT,
                        material TEXT,
                        speed INTEGER,
                        status TEXT,
                        time_left INTEGER,
                        expected_time DATETIME
                    )
                """
            
            self.execute_query(query)
        except Exception as e:
            print(f"Error initializing schema: {e}")
            raise RuntimeError("Failed to initialize DB schema")
    
    
    def execute_query(self, query, params=()):
        """Execute a query with n amount of params."""
        with sqlite3.connect(
                self.db_path,
                detect_types= sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        ) as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            # Returns a list
            return cursor.fetchall()