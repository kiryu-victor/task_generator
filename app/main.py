from datetime import datetime
import time
import socket
import threading

import tkinter as tk

from controller.mainController import MainController
from utils.wss import WebSocketServer, WebSocketClient
from view.mainView import MainView

if __name__ == "__main__":
    root = tk.Tk()
    main_view = MainView(root)

    # Callback to update the main view when new state arrives from server
    def update_view_from_server(tasks):
        main_view.populate_table(tasks)

    # Try to connect as a client.
    # If it fails, start server, then connect as client.
    def is_server_running(host='localhost', port=8765):
        try:
            # Create a connection after 0.1s
            with socket.create_connection((host, port), timeout=0.1):
                return True
        except Exception:
            return False

    if not is_server_running():
        # Start server in another thread if there is no server running
        server = WebSocketServer()
        threading.Thread(
                target=server.run,
                daemon=True
        ).start()
        # Wait for the server to start
        time.sleep(0.5)

    # Start client
    ws_client = WebSocketClient(update_view_from_server)

    # Instantiate MainController, passing ws_client for downstream use
    controller = MainController(main_view, ws_client)

    def on_close():
        """Gather all ongoing tasks and their actual time_left BEFORE the server closes."""
        tasks_to_save = []
        for item in main_view.tree.get_children():
            values = list(main_view.tree.item(item, "values"))
            try:
                if values[5] == "In progress":
                    time_left = int(
                            (
                                datetime.strptime(values[7], "%Y-%m-%d %H:%M:%S.%f")
                                - datetime.now()
                            ).total_seconds()
                            )
                    tasks_to_save.append({
                        "task_id": values[0],
                        "time_left": time_left
                    })
            except Exception:
                continue
        if tasks_to_save:
            ws_client.send("save_time_left", {"tasks": tasks_to_save})
            time.sleep(1)
        # Close the websocket connection
        ws_client.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Shows all until the user terminates the program
    root.mainloop()