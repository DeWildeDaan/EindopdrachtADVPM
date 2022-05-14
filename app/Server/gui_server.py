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
import customtkinter
from numpy import append

from Server.server import Server
from Server.clienthandler import ClientHandler
from Server.Dataset import Dataset


class ServerWindow(Frame):
    def __init__(self, master=None, dataset=None):
        """
        It creates a window, creates a queue, and creates a server.

        :param master: the root window
        :param dataset: a list of dictionaries, each dictionary contains the information of a message
        """
        Frame.__init__(self, master)
        self.__server_created = False
        self.master = master
        self.dataset = dataset
        self.init_window()
        self.init_messages_queue()
        self.init_server()
    
    @property
    def server_created(self):
        """
        It returns the value of the variable __server_created.
        :return: The server_created method is being returned.
        """
        return self.__server_created

    def init_server(self):
        """
        It creates a server object, which is a thread, and starts it
        """
        self.server = Server(socket.gethostname(), 9999,
                             self.messages_queue, self.dataset)

    def start_stop_server(self):
        """
        If the server is connected, close the server socket, otherwise initialize the server and start the
        server thread
        """
        if self.server.is_connected == True:
            self.server.close_server_socket()
            self.btn_text.set("Start server")
        else:
            if self.server_created == True:
                self.lstmain.delete(0, END)
                self.init_server()
                self.server.init_server()
                self.server.start()
            if self.__server_created == False:
                self.server.init_server()
                self.server.start()
                self.__server_created = True
            self.btn_text.set("Stop server")

    def afsluiten_server(self):
        """
        It closes the server socket and sends a message to the GUI to close the server
        """
        if self.server != None:
            self.server.close_server_socket()
            self.messages_queue.put("CLOSE_SERVER")

    def init_messages_queue(self):
        """
        It creates a queue and a thread that will print the messages from the queue
        """
        self.messages_queue = Queue()
        t = Thread(target=self.print_messsages_from_queue, name="Thread-queue")
        t.start()

    def print_messsages_from_queue(self):
        """
        It gets a message from the queue, and while the message is not "CLOSE_SERVER", it inserts the
        message into the listbox and then gets the next message from the queue
        """
        message = self.messages_queue.get()
        while not "CLOSE_SERVER" in message:
            self.lstmain.insert(END, message)
            self.messages_queue.task_done()
            message = self.messages_queue.get()

    def init_window(self):
        """
        It creates the window and the tabs.
        """
        self.master.title("Server")

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

        self.pack(fill=BOTH, expand=1)

        self.logging_window()
        self.clients_window()
        self.client_logs_window()
        self.commands_window()

    def logging_window(self):
        """
        It creates a listbox and a scrollbar, and a button.
        """
        customtkinter.CTkLabel(self.logging, text="Log-berichten server:").grid(row=0)
        self.scrollbar = Scrollbar(self.logging, orient=VERTICAL)
        self.lstmain = Listbox(
            self.logging, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstmain.yview)

        self.lstmain.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=1, sticky=N + S)

        self.btn_text = StringVar()
        self.btn_text.set("Start server")
        self.buttonServer = customtkinter.CTkButton(
            self.logging, textvariable=self.btn_text, command=self.start_stop_server)
        self.buttonServer.grid(row=3, column=0, columnspan=2, pady=(
            5, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self.logging, 1, weight=1)
        Grid.columnconfigure(self.logging, 0, weight=1)

    def clients_window(self):
        """
        It creates a window with a listbox and a button.
        """
        Label(self.clients, text="Online clients:").grid(row=0)
        self.scrollbar = Scrollbar(self.clients, orient=VERTICAL)
        self.lstclients = Listbox(
            self.clients, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstclients.yview)

        self.lstclients.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=1, sticky=N + S)

        self.btn_textClients = StringVar()
        self.btn_textClients.set("Refresh")
        self.buttonClients = customtkinter.CTkButton(
            self.clients, textvariable=self.btn_textClients, command=self.show_clients)
        self.buttonClients.grid(row=3, column=0, columnspan=2, pady=(
            5, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self.clients, 1, weight=1)
        Grid.columnconfigure(self.clients, 0, weight=1)

    def client_logs_window(self):
        """
        It creates a window with a combobox, a listbox, and a button.
        """
        self.cbo_clients = Combobox(
            self.clientlogs, postcommand=self.updatecbobox, state="readonly", width=40)
        self.cbo_clients.grid(row=2, column=0, sticky=E + W)
        customtkinter.CTkLabel(self.clientlogs, text="Logs per client:").grid(row=0)
        self.scrollbar1 = Scrollbar(self.clientlogs, orient=VERTICAL)
        self.lstlogs = Listbox(
            self.clientlogs, yscrollcommand=self.scrollbar1.set)
        self.scrollbar1.config(command=self.lstlogs.yview)

        self.lstlogs.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar1.grid(row=1, column=1, sticky=N + S)

        self.btn_textLogs = StringVar()
        self.btn_textLogs.set("Search")
        self.buttonLogs = customtkinter.CTkButton(
            self.clientlogs, textvariable=self.btn_textLogs, command=self.show_logs)
        self.buttonLogs.grid(row=3, column=0, columnspan=2, pady=(
            5, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self.clientlogs, 1, weight=1)
        Grid.columnconfigure(self.clientlogs, 0, weight=1)
        self.show_clients()

    def commands_window(self):
        """
        It creates a window with a listbox and a button. The button is supposed to refresh the listbox.
        """
        customtkinter.CTkLabel(self.commands, text="Command stats:").grid(row=0)
        self.scrollbar = Scrollbar(self.commands, orient=VERTICAL)
        self.lstCommands = Listbox(
            self.commands, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstCommands.yview)

        self.lstCommands.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=1, sticky=N + S)

        self.btn_textCommands = StringVar()
        self.btn_textCommands.set("Refresh")
        self.buttonCommands = customtkinter.CTkButton(
            self.commands, textvariable=self.btn_textCommands, command=self.show_command_stats)
        self.buttonCommands.grid(row=3, column=0, columnspan=2, pady=(
            5, 5), padx=(5, 5), sticky=N + S + E + W)

        Grid.rowconfigure(self.commands, 1, weight=1)
        Grid.columnconfigure(self.commands, 0, weight=1)
        self.show_command_stats()

    def updatecbobox(self):
        """
        It gets all the files in the directory, removes the .txt extension and adds them to the combobox.
        """
        location = os.path.join(os.path.dirname(__file__), f'../Server/logs/')
        files = os.listdir(location)
        users = []
        for f in files:
            size = len(f)
            f = f[:size - 4]
            users.append(f)
        self.cbo_clients['values'] = users

    def show_clients(self):
        """
        It deletes all the items in the listbox, then inserts all the clients in the ClientHandler.clients
        list
        """
        self.lstclients.delete(0, END)
        for c in ClientHandler.clients:
            self.lstclients.insert(END, c)

    def show_command_stats(self):
        """
        It reads a file, splits the first line, and then inserts the first line into a listbox.
        """
        self.lstCommands.delete(0, END)
        location = os.path.join(os.path.dirname(
            __file__), f'../Server/commands.txt')
        f = open(location, "r")
        firstline = f.readline().rstrip()
        firstline = firstline.split(',')
        f.close()
        self.lstCommands.insert(
            END, f'Searches on name: {Dataset.name_command}')
        self.lstCommands.insert(
            END, f'Searches on country&region: {Dataset.country_command}')
        self.lstCommands.insert(
            END, f'Searches on radius: {Dataset.radius_command}')
        self.lstCommands.insert(
            END, f'Searches on stats: {Dataset.stats_command}')
        self.lstCommands.insert(
            END, f'Searches on graphs: {Dataset.graph_command}')

    def show_logs(self):
        """
        It opens a file, reads the file, and inserts the contents of the file into a listbox.
        """
        self.lstlogs.delete(0, END)
        user = self.cbo_clients.get()
        location = os.path.join(os.path.dirname(
            __file__), f'../Server/logs/{user}.txt')
        f = open(location, "r")
        for x in f:
            self.lstlogs.insert(END, x.strip())
        f.close()
