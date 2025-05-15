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
    
    # Load both the main view and controller
    main_view = MainView(root)
    MainController(main_view, websocket_server)

    def on_close():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Shows all until the user terminates the program
    root.mainloop()
