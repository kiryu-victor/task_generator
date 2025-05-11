import asyncio
import websockets

class WebSocketServer:
    def __init__(self):
        # Set of clients
        self.clients = set()
        self.server = None

    # Registration
    async def register(self, websocket):
        """Register a new client."""
        self.clients.add(websocket)
        print(f"Cliente connected: {websocket.remote_address}")
    
    async def unregister(self, websocket):
        """Unregister a new client."""
        self.clients.remove(websocket)
        print(f"Cliente disconnected: {websocket.remote_address}")

    # Broadcasting and getting messages
    async def broadcast(self, message):
        """Sends a message to all the connected clients"""
        # Check if there are any connected clients
        if self.clients:
            tasks = []
            # Iterate over all connected clients
            for client in self.clients:
                try:
                    # Create an asynchronous task to send the message to the client
                    tasks.append(asyncio.create_task(client.send(message)))
                except Exception as e:
                    # Handle any exceptions that occur while sending the message
                    print(f"Error sending message to client {client.remote_address} : {e}")
            # Wait for all tasks to complete
            await asyncio.wait(tasks)

    async def handle_client(self, websocket):
        """Get messages from a client"""
        await self.register(websocket)
        try:
            async for message in websocket:
                print(f"Received message from {websocket.remote_address}: {message}")
                await self.broadcast(message)
        except websockets.exceptions.ConnectionClosed:
            print(f"Connection closed: {websocket.remote_address}")
        finally:
            await self.unregister(websocket)

    async def start_server(self):
        """Start the server"""
        server = await websockets.serve(self.handle_client, "localhost", 8765)
        print("Websocket server started on ws://localhost:8765")
        await server.wait_closed()

    async def stop_server(self):
        """Stop the server"""
        print("Stopping the Websocket server")
        int = 1
        for client in list(self.clients):
            await client.close()
            print(f"paso {int}")
            int = int + 1
        self.clients.clear()

# Run the server
if __name__ == "__main__":
    server = WebSocketServer()
    asyncio.run(server.start_server())