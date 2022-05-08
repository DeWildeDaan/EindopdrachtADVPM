# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import imp
import os
import glob
import logging
from random import choices
import socket
from queue import Queue
from threading import Thread
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Combobox

from numpy import append

from Server.server import Server
from Server.clienthandler import ClientHandler
from Server.Dataset import Dataset


class ServerWindow(Frame):
    def __init__(self, master=None, dataset=None):
        Frame.__init__(self, master)
        self.master = master
        self.dataset = dataset
        self.init_window()
        self.init_messages_queue()
        self.init_server()

    def init_server(self):
        self.server = Server(socket.gethostname(), 9999,
                             self.messages_queue, self.dataset)

    def start_stop_server(self):
        if self.server.is_connected == True:
            self.server.close_server_socket()
            self.btn_text.set("Start server")
        else:
            self.server.init_server()
            self.server.start()  # thread!
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

        # Adding tabs
        self.tabControl = ttk.Notebook(self)
        self.logging = ttk.Frame(self.tabControl)
        self.clients = ttk.Frame(self.tabControl)
        self.clientlogs = ttk.Frame(self.tabControl)
        self.commands = ttk.Frame(self.tabControl)
        self.tabControl.add(self.logging, text='Logging window')
        self.tabControl.add(self.clients, text='Clients')
        self.tabControl.add(self.clientlogs, text='Client logs')
        self.tabControl.add(self.commands, text='Command stats')
        self.tabControl.pack(expand=1, fill=BOTH)

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # Creating all tabs
        self.logging_window()
        self.clients_window()
        self.client_logs_window()
        self.commands_window()

    # Different windows
    def logging_window(self):
        Label(self.logging, text="Log-berichten server:").grid(row=0)
        self.scrollbar = Scrollbar(self.logging, orient=VERTICAL)
        self.lstnumbers = Listbox(
            self.logging, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstnumbers.yview)

        self.lstnumbers.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=1, sticky=N + S)

        self.btn_text = StringVar()
        self.btn_text.set("Start server")
        self.buttonServer = Button(
            self.logging, textvariable=self.btn_text, command=self.start_stop_server)
        self.buttonServer.grid(row=3, column=0, columnspan=2, pady=(
            5, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self.logging, 1, weight=1)
        Grid.columnconfigure(self.logging, 0, weight=1)

    def clients_window(self):
        # Label(self.clients, text="Online clients:").grid(row=0)
        # self.show_clients()
        Label(self.clients, text="Online clients:").grid(row=0)
        self.scrollbar = Scrollbar(self.clients, orient=VERTICAL)
        self.lstclients = Listbox(
            self.clients, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstclients.yview)

        self.lstclients.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=1, sticky=N + S)

        self.btn_textClients = StringVar()
        self.btn_textClients.set("Refresh")
        self.buttonClients = Button(
            self.clients, textvariable=self.btn_textClients, command=self.show_clients)
        self.buttonClients.grid(row=3, column=0, columnspan=2, pady=(
            5, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self.clients, 1, weight=1)
        Grid.columnconfigure(self.clients, 0, weight=1)

    def client_logs_window(self):
        self.cbo_clients = Combobox(
            self.clientlogs, postcommand=self.updatecbobox, state="readonly", width=40)
        self.cbo_clients.grid(row=2, column=0, sticky=E + W)
        Label(self.clientlogs, text="Logs per client:").grid(row=0)
        self.scrollbar1 = Scrollbar(self.clientlogs, orient=VERTICAL)
        self.lstlogs = Listbox(
            self.clientlogs, yscrollcommand=self.scrollbar1.set)
        self.scrollbar1.config(command=self.lstlogs.yview)

        self.lstlogs.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar1.grid(row=1, column=1, sticky=N + S)

        self.btn_textLogs = StringVar()
        self.btn_textLogs.set("Search")
        self.buttonLogs = Button(
            self.clientlogs, textvariable=self.btn_textLogs, command=self.show_logs)
        self.buttonLogs.grid(row=3, column=0, columnspan=2, pady=(
            5, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self.clientlogs, 1, weight=1)
        Grid.columnconfigure(self.clientlogs, 0, weight=1)
        self.show_clients()

    def commands_window(self):
        Label(self.commands, text="Command stats:").grid(row=0)
        self.scrollbar = Scrollbar(self.commands, orient=VERTICAL)
        self.lstCommands = Listbox(
            self.commands, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstCommands.yview)

        self.lstCommands.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=1, sticky=N + S)

        self.btn_textCommands = StringVar()
        self.btn_textCommands.set("Refresh")
        self.buttonCommands = Button(
            self.commands, textvariable=self.btn_textCommands, command=self.show_command_stats)
        self.buttonCommands.grid(row=3, column=0, columnspan=2, pady=(
            5, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self.commands, 1, weight=1)
        Grid.columnconfigure(self.commands, 0, weight=1)
        self.show_command_stats()

    def updatecbobox(self):
        files = os.listdir(
            'C:/Users/daand/OneDrive - Hogeschool West-Vlaanderen/School/S4/Advanced Programming and Maths/EindopdrachtADVPM/app/Server/logs/')
        users = []
        for f in files:
            size = len(f)
            f = f[:size - 4]
            users.append(f)
        self.cbo_clients['values'] = users

    def show_clients(self):
        self.lstclients.delete(0, END)
        for c in ClientHandler.clients:
            self.lstclients.insert(END, c)

    def show_command_stats(self):
        self.lstCommands.delete(0, END)
        location = os.path.join(os.path.dirname(
            __file__), f'../Server/commands.txt')
        f = open(location, "r")
        firstline = f.readline().rstrip()
        firstline = firstline.split(',')
        f.close()
        # self.lstCommands.insert(END, f'Searches on name: {firstline[0]}')
        # self.lstCommands.insert(
        #     END, f'Searches on country&region: {firstline[1]}')
        # self.lstCommands.insert(END, f'Searches on radius: {firstline[2]}')
        # self.lstCommands.insert(END, f'Searches on stats: {firstline[3]}')
        # self.lstCommands.insert(END, f'Searches on graphs: {firstline[4]}')
        self.lstCommands.insert(END, f'Searches on name: {Dataset.name_command}')
        self.lstCommands.insert(
            END, f'Searches on country&region: {Dataset.country_command}')
        self.lstCommands.insert(END, f'Searches on radius: {Dataset.radius_command}')
        self.lstCommands.insert(END, f'Searches on stats: {Dataset.stats_command}')
        self.lstCommands.insert(END, f'Searches on graphs: {Dataset.graph_command}')

    def show_logs(self):
        self.lstlogs.delete(0, END)
        user = self.cbo_clients.get()
        location = os.path.join(os.path.dirname(
            __file__), f'../Server/logs/{user}.txt')
        f = open(location, "r")
        for x in f:
            self.lstlogs.insert(END, x.strip())
        f.close()
