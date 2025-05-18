import asyncio
import websockets
import json
import threading

from websockets.protocol import OPEN

from model.taskManager import TaskManager
from model.taskModel import TaskModel
from utils.database import DatabaseManager

WS_HOST = '127.0.0.1'
WS_PORT = 8765

class WebSocketServer:
    """
    WebSocket server for handling task operations and broadcasting state.
    Handles connections, receives operations from clients, updates DB,
    broadcasts the updated state of the DB.
    """
    def __init__(self, db_path='tasks.db'):
        # Connected clients
        self.clients = set()
        self.db_manager = DatabaseManager(db_path)
        self.task_manager = TaskManager(self.db_manager)

    async def handler(self, websocket):
        # New client connects
        self.clients.add(websocket)
        # Print the remote address and port
        if hasattr(websocket, 'remote_address') and websocket.remote_address:
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
        action = data.get('action')
        params = data.get('params', {})
        if action == 'create':
            # Convert params dict to TaskModel
            task_model = TaskModel(**params)
            self.task_manager.create_task(task_model)
        elif action == 'update':
            self.task_manager.update_task(params)
        elif action == 'delete':
            self.task_manager.delete_task(params['task_id'])

    async def send_state(self, websocket):
        """
        Send the current state (all tasks) to a client.
        This exists aside of 'broadcast_state' as it is used only
        when a new connection happens, getting the current state.
        """
        tasks = self.task_manager.read_all_tasks()
        message = json.dumps(
                {
                    'type': 'state',
                    'tasks': tasks
                }
        )
        await websocket.send(message)

    async def broadcast_state(self):
        """
        Broadcast the current state to all connected clients.
        """
        tasks = self.task_manager.read_all_tasks()
        message = json.dumps(
                {
                    'type': 'state',
                    'tasks': tasks
                }
        )
        await asyncio.gather(
                *(
                    client.send(message)
                    for client in self.clients
                    if getattr(client, 'protocol', None)
                            and client.protocol.state == OPEN
                )
        )

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

class WebSocketClient:
    """
    WebSocket client for sending operations and receiving state updates.
    Connects to server, sends operations for the server to process,
    receives state updates from the server.
    """
    def __init__(self, on_state_callback, host=WS_HOST, port=WS_PORT):
        self.uri = f'ws://{host}:{port}'
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
                if data.get('type') == 'state':
                    self.on_state_callback(data['tasks'])
        except Exception as e:
            print(f"WebSocket receive error: {e}")

    def send(self, action, params):
        # Send an operation to the server
        message = json.dumps({'action': action, 'params': params})
        asyncio.run_coroutine_threadsafe(self.ws.send(message), self.loop)

    def close(self):
        # Close the websocket connection
        if self.ws:
            asyncio.run_coroutine_threadsafe(self.ws.close(), self.loop)
