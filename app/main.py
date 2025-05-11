from controller.mainController import MainController
from view.mainView import MainView
from utils.wss import WebSocketServer

import tkinter as tk
import asyncio

# Websocket server instance
websocket_server = WebSocketServer()

async def start_websocket_server():
    """Start the server to listen for connetions"""
    await websocket_server.start_server()

async def run_tkinter(root):
    """Main loop for the GUI"""
    while True:
        try:
            # Refresh the GUI
            root.update()
            await asyncio.sleep(0.01)
        # If the window is close, exit the loop
        except tk.TclError:
            break

async def main():
    # Main app window
    root = tk.Tk()
    main_view = MainView(root)
    MainController(main_view, websocket_server)

    close_event = asyncio.Event()

    async def on_close():
        print("Shutting down...")
        # Disconnect al clients
        await websocket_server.stop_server()
        root.destroy()
        close_event.set()

    root.protocol(
            "WM_DELETE_WINDOW",
            lambda: asyncio.create_task(on_close())
    )

    # Tasks references
    server_task = asyncio.create_task(start_websocket_server())
    tk_task = asyncio.create_task(run_tkinter(root))
    # Shutdown signal
    await close_event.wait()
    # Cleanup tasks
    server_task.cancel()
    tk_task.cancel()

    # Start both Websocket and Tkinter main loop
    await asyncio.gather(
            # Call both coroutines
            server_task,
            tk_task,
            return_exceptions=True
    )

if __name__ == "__main__":
    # Start the wss in another thread
    asyncio.run(main())