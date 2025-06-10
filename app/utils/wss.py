import asyncio
from datetime import datetime
import websockets
import json
import threading

from websockets.protocol import OPEN

from model.taskManager import TaskManager
from model.taskModel import TaskModel
from utils.database import DatabaseManager

WS_HOST = "127.0.0.1"
WS_PORT = 8765

class WebSocketServer:
    """
    WebSocket server for handling task operations and broadcasting state.
    Handles connections, receives operations from clients, updates DB,
    broadcasts the updated state of the DB.
    """
    def __init__(self, db_path="tasks.db"):
        # Connected clients
        self.clients = set()
        self.db_manager = DatabaseManager(db_path)
        self.task_manager = TaskManager(self.db_manager)

        self.machines_tasks_dict = {}
        

    async def handler(self, websocket):
        # New client connects
        self.clients.add(websocket)
        # Print the remote address and port
        if hasattr(websocket, "remote_address") and websocket.remote_address:
            print(f"Client connected from {websocket.remote_address}")
        else:
            print("Client connected (address unknown)")
        try:
            # Send current state to new client
            await self.send_state(websocket)
            # Listen for messages from this client
            async for message in websocket:
                await self.process_message(message)
                await self.broadcast_state()
        except Exception as e:
            print(f"WebSocket handler error: {e}")
        finally:
            print()
            self.clients.remove(websocket)

    
    async def process_message(self, message):
        """
        Process a message from a client: create, update, or delete a task.
        Depending on the action, a different query is prepared.
        The query is filled with the params.
        """
        data = json.loads(message)
        action = data.get("action")
        params = data.get("params", {})
        if action == "create":
            # Convert params dict to TaskModel
            task_model = TaskModel(**params)
            self.task_manager.create_task(task_model)
        elif action == "update":
            self.task_manager.update_task(params)
        elif action == "delete":
            self.task_manager.delete_task(params["task_id"])

    async def send_state(self, websocket):
        """
        Send the current state (all tasks) to a client.
        This exists aside of "broadcast_state" as it is used only
        when a new connection happens, getting the current state.
        """
        tasks = self.task_manager.read_all_tasks()
        message = json.dumps(
                {
                    "type": "state",
                    "tasks": tasks
                }
        )

        self.create_machine_queues_dict()
        self.start_tasks_in_progress()
        self.start_tasks_on_idle_machines()
        await websocket.send(message)


    async def broadcast_state(self):
        """
        Broadcast the current state to all connected clients.
        """
        tasks = self.task_manager.read_all_tasks()
        message = json.dumps(
                {
                    "type": "state",
                    "tasks": tasks
                }
        )
        await asyncio.gather(
                *(
                    client.send(message)
                    for client in self.clients
                    if getattr(client, "protocol", None)
                            and client.protocol.state == OPEN
                )
        )

        self.create_machine_queues_dict()
        self.start_tasks_on_idle_machines()
        


    def run(self):
        """
        Start the WebSocket server (blocking call).
        Should be run in a background thread if used with a GUI.
        """
        async def start():
            server = await websockets.serve(self.handler, WS_HOST, WS_PORT)
            print(f"WebSocket server started on ws://{WS_HOST}:{WS_PORT}")
            
            await server.wait_closed()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start())
        loop.run_forever()

    def create_machine_queues_dict(self):
        """
        Creates a dictionary with machines are keys
        and "On queue" tasks in a list for each machine. 
        """
        tasks = self.task_manager.read_all_tasks()
        machines_tasks = {}
        for task in tasks:
            machine = task[2]
            task_id = task[0]
            status = task[5]
            if machine not in machines_tasks:
                machines_tasks[machine] = []
            if status == "On queue":
                machines_tasks[machine].append(task_id)
        self.machines_tasks_dict = machines_tasks

    def start_tasks_on_idle_machines(self):
        """Starts the first task (by order) on an idle machine."""
        idle_machines = self.search_idle_machines()
        for m in idle_machines:
            if self.machines_tasks_dict.get(m, []) != []:
                task = self.pop_first_task_id(m)
                self.start_task(task)
            else:
                print(f"The machine {m} is empty.")

    def start_tasks_in_progress(self):
        """Starts the tasks that are "In progress" when the server launches."""
        tasks = self.search_running_machines()
        for t in tasks:
            self.start_task(t[0])



    def search_idle_machines(self):
        """Returns a list of machines that have no ongoing tasks."""
        tasks = self.task_manager.read_all_tasks()
        machines = set(task[2] for task in tasks)
        busy_machines = set()
        for task in tasks:
            status = task[5]
            if status == "In progress":
                busy_machines.add(task[2])
        idle_machines = list(machines - busy_machines)
        return idle_machines

    def search_running_machines(self):
        """Searchs the machines with ongoing tasks."""
        tasks = self.task_manager.read_all_tasks()
        started_tasks = []
        for t in tasks:
            if t[5] == "In progress":
                started_tasks.append(t)
        return started_tasks

    def pop_first_task_id(self, machine):
        """Returns the task_id of the first task on the queue and unqueues it."""
        tasks = self.machines_tasks_dict
        return tasks[machine].pop(0)
    
    def start_task(self, task_id):
        """
        Starts a task by updating its:
        - time left, status, timestamp_expected_complete
        Calls the completion function with a timer.
        """
        task = self.task_manager.read_task(task_id)
        time_left = int(task.time_left)
                
        self.task_manager.update_task_start_parameters(time_left, task_id)
        
        # Use create_task instead of asyncio.run to avoid event loop errors
        asyncio.create_task(self._call_complete_task(task, time_left))
        # Notify all clients of the new state
        asyncio.create_task(self.broadcast_state())

    async def _call_complete_task(self, task, time):
        """Completes a task after a given time and update timers."""
        await asyncio.sleep(time)
        self.update_tasks_timers()
        self.complete_task(task)
        self.update_tasks_timers()
        
    def complete_task(self, task):
        """For completion, updates tasks
        - status (Complete), time_left(""), timestamp_expected_complete(now)"""
        self.task_manager.udpate_task_complete(task.task_id)
        # Notify all clients of the new state
        asyncio.create_task(self.broadcast_state())


    def update_tasks_timers(self):
        """Refreshes tasks to show the remaining time at that point in time."""
        tasks = self.task_manager.read_all_tasks()
        for task in tasks:
            if task[5] == "In progress":
                task_id = task[0]
                now = datetime.now()
                time_expected = task[7]
                new_time_left = datetime.strptime(time_expected, "%Y-%m-%d %H:%M:%S.%f") - now
                int_new_time_left = int(new_time_left.total_seconds())
                self.task_manager.update_task_time_left(task_id, int_new_time_left)



class WebSocketClient:
    """
    WebSocket client for sending operations and receiving state updates.
    Connects to server, sends operations for the server to process,
    receives state updates from the server.
    """
    def __init__(self, on_state_callback, host=WS_HOST, port=WS_PORT):
        self.uri = f"ws://{host}:{port}"
        # Function to call with new state
        self.on_state_callback = on_state_callback
        self.loop = asyncio.new_event_loop()
        threading.Thread(
                target=self.loop.run_forever,
                daemon=True
                ).start()
        # Client's connection to the server
        self.ws = None
        self.connect()

    def connect(self):
        # Start connection in the background
        asyncio.run_coroutine_threadsafe(self._connect(), self.loop)

    async def _connect(self):
        try:
            self.ws = await websockets.connect(self.uri)
            asyncio.create_task(self.receive())
        except Exception as e:
            print(f"WebSocket connection failed: {e}")

    async def receive(self):
        # Listen for messages from the server
        try:
            async for message in self.ws:
                data = json.loads(message)
                if data.get("type") == "state":
                    self.on_state_callback(data["tasks"])
        except Exception as e:
            print(f"WebSocket receive error: {e}")

    def send(self, action, params):
        # Send an operation to the server
        message = json.dumps({"action": action, "params": params})
        asyncio.run_coroutine_threadsafe(self.ws.send(message), self.loop)

    def close(self):
        # Close the websocket connection
        if self.ws:
            asyncio.run_coroutine_threadsafe(self.ws.close(), self.loop)