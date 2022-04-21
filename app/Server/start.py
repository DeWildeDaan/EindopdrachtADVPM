import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)
print(str(Path(sys.path[0]).parent))

import threading
from tkinter import *
from Server.gui_server import ServerWindow
from Models.Dataset import Dataset

def callback():
    # test
    # threads overlopen
    print("Active threads:")
    for thread in threading.enumerate():
        print(f">Thread name is {thread.getName()}.")
    gui_server.afsluiten_server()
    root.destroy()

root = Tk()
dataset = Dataset()
root.geometry("600x500")
gui_server = ServerWindow(root, dataset)
root.protocol("WM_DELETE_WINDOW", callback)
root.mainloop()
