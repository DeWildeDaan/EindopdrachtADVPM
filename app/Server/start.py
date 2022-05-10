from pathlib import Path
import sys
sys.path[0] = str(Path(sys.path[0]).parent)
print(str(Path(sys.path[0])))

import threading
from tkinter import *
from Server.server import Server
from Server.gui_server import ServerWindow
from Server.Dataset import Dataset

def callback():
    """
    It prints the names of all active threads and then closes the server
    """
    print("Active threads:")
    for thread in threading.enumerate():
        print(f">Thread name is {thread.getName()}.")
    gui_server.afsluiten_server()
    root.destroy()


# It creates a window with a button that starts the server and initializes the dataset.
root = Tk()
dataset = Dataset()
root.geometry("600x500")
gui_server = ServerWindow(root, dataset=dataset)
root.protocol("WM_DELETE_WINDOW", callback)
root.mainloop()
