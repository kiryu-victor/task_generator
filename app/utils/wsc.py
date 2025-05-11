import asyncio
import websockets

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri

    async def connect(self):
        """Connect to the Webscoket server"""
        async with websockets.connect(self.uri) as websocket:
            print("Connected to WebSocket server")
            await self.listen(websocket)

    async def listen(self, websocket):
        """Listen for the messages comming from the server."""
        try:
            async for message in websocket:
                print(f"Received message: {message}")
                # Handle message
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")

# Run the client
if __name__ == "__main__":
    client = WebSocketClient("ws://localhost:8765")
    asyncio.run(client.connect())