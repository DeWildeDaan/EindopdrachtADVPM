# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import imp
import os
import logging
import socket
from queue import Queue
from threading import Thread
from tkinter import *
import tkinter as tk
from tkinter.ttk import Combobox

from Server.server import Server
from Server.clienthandler import ClientHandler
from Models.Dataset import Dataset


class ServerWindow(Frame):
    def __init__(self, master=None, dataset=None):
        Frame.__init__(self, master)
        self.master = master
        self.dataset = dataset
        self.init_window()
        self.init_messages_queue()
        self.init_server()

    def init_server(self):
        self.server = Server(socket.gethostname(), 9999, self.messages_queue, self.dataset)

    def start_stop_server(self):
        if self.server.is_connected == True:
            self.server.close_server_socket()
            self.btn_text.set("Start server")
        else:
            self.server.init_server()
            self.server.start()             #thread!
            self.btn_text.set("Stop server")
    
    def afsluiten_server(self):
        if self.server != None:
            self.server.close_server_socket()
            self.messages_queue.put("CLOSE_SERVER")
    
    # QUEUE
    def init_messages_queue(self):
        self.messages_queue = Queue()
        t = Thread(target=self.print_messsages_from_queue, name="Thread-queue")
        t.start()

    def print_messsages_from_queue(self):
        message = self.messages_queue.get()
        while not "CLOSE_SERVER" in message:
            self.lstnumbers.insert(END, message)
            self.messages_queue.task_done()
            message = self.messages_queue.get()


    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Server")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        Label(self, text="Log-berichten server:").grid(row=0)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.lstnumbers = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstnumbers.yview)

        self.lstnumbers.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=1, sticky=N + S)

        self.btn_text = StringVar()
        self.btn_text.set("Start server")
        self.buttonServer = Button(self, textvariable=self.btn_text, command=self.start_stop_server)
        self.buttonServer.grid(row=3, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
        
        self.test = Button(self, text='Clients', command=self.clients_window)
        self.test.grid(row=4, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)

        self.test = Button(self, text='Logs', command=self.logs_window)
        self.test.grid(row=5, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)

        self.test = Button(self, text='Commands', command=self.commands_window)
        self.test.grid(row=6, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
         
        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

    
    def clients_window(self):
        self.newwindowc = Toplevel(self.master)
        self.newwindowc.title("Online clients")
        self.newwindowc.geometry("200x200")
        Label(self.newwindowc, text ="Online clients:").grid(row=0)
        self.show_clients()
    
    def logs_window(self):
        self.newwindowl = Toplevel(self.master)
        self.newwindowl.title("Logs per client")
        self.newwindowl.geometry("300x300")
        Label(self.newwindowl, text='Logs per client:').grid(row=0)
        choices = tuple()
        for c in ClientHandler.clients:
            choices = (choices, c.name)
        # self.entry_wegdek.grid(row=2, column=1, sticky=E + W)
        self.cbo_clients = Combobox(self.newwindowl, state="readonly", width=40)
        self.cbo_clients['values'] = choices
        self.cbo_clients.grid(row=2, column=0, sticky=E + W)

        self.scrollbar1 = Scrollbar(self.newwindowl, orient=VERTICAL)
        self.lstlogs = Listbox(self.newwindowl, yscrollcommand=self.scrollbar1.set)
        self.scrollbar1.config(command=self.lstlogs.yview)

        self.lstlogs.grid(row=3, column=0, columnspan=2, sticky=N + S + E + W)
        self.scrollbar1.grid(row=3, column=0, sticky=N + S)

        self.buttonServer = Button(self.newwindowl, text="Search", command=self.show_logs)
        self.buttonServer.grid(row=4, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)

    def commands_window(self):
        self.newwindowcm = Toplevel(self.master)
        self.newwindowcm.title("Commands")
        self.newwindowcm.geometry("200x200")
        Label(self.newwindowcm, text='Commands:').grid(row=0)
        Label(self.newwindowcm, text=f'Searches on name: {Dataset.name_command}').grid(row=1)
        Label(self.newwindowcm, text=f'Searches on country&region: {Dataset.country_command}').grid(row=2)
        Label(self.newwindowcm, text=f'Searches on radius: {Dataset.radius_command}').grid(row=3)
        Label(self.newwindowcm, text=f'Search on stats: {Dataset.stats_command}').grid(row=4)
        Label(self.newwindowcm, text=f'Search on graphs: {Dataset.graph_command}').grid(row=5)

    def show_clients(self):
        index = 1
        for c in ClientHandler.clients:
            i = Label(self.newwindowc, text=c)
            i.grid(row=index, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky=N + S + E + W)
            index+=1
    
    def show_logs(self):
        user = self.cbo_clients.get()
        for c in ClientHandler.clients:
            if c.name == user:
                client = c
        filename = f"{client.name}-{client.nickname}-{client.email}.txt"
        directory = 'c:/Users/daand/OneDrive - Hogeschool West-Vlaanderen/School/S4/Advanced Programming and Maths/EindopdrachtADVPM/app/logs/'
        location = os.path.join(directory, filename)
        print(location)
        f = open(location, "r")
        for x in f:
            self.lstlogs.insert(END, x.strip())
        f.close()
    
    