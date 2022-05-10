import numpy as np
import matplotlib.pyplot as plt
import logging
import threading
import pickle
import os
import math
from Server.Dataset import Dataset
from Models.Location import Location
from Models.CountryInfo import CountryInfo


class ClientHandler(threading.Thread):

    numbers_clienthandlers = 0
    clients = []

    def __init__(self, socketclient, messages_queue, dataset):
        """
        It creates a new ClientHandler object, which is a thread, and adds it to the list of clients.

        :param socketclient: the socket that is connected to the client
        :param messages_queue: a queue that contains all the messages that need to be sent to the clients
        :param dataset: a list of objects
        """
        threading.Thread.__init__(self)
        self.dataset = dataset
        self.socket_to_client = socketclient
        self.messages_queue = messages_queue
        self.id = ClientHandler.numbers_clienthandlers
        ClientHandler.numbers_clienthandlers += 1

        self.io_stream_client = self.socket_to_client.makefile(mode='rwb')
        self.user = pickle.load(self.io_stream_client)
        self.print_bericht_gui_server(f"{self.user.nickname} connected")

        self.clients.append(self.user)

    def run(self):
        """
        It receives a command from the client, and depending on the command, it will either send back a
        list of objects, or a graph
        """
        logging.info("Started & waiting...")
        command = pickle.load(self.io_stream_client)

        while command != "CLOSE":
            if command == "name":
                name = pickle.load(self.io_stream_client)
                pickle.dump(self.dataset.search_by_name(
                    self.user, name), self.io_stream_client)
                self.io_stream_client.flush()
                self.print_bericht_gui_server(
                    f"{self.user} searched for a restaurant.")
            if command == "country":
                country = pickle.load(self.io_stream_client)
                region = pickle.load(self.io_stream_client)
                pickle.dump(self.dataset.search_by_country(
                    self.user, country, region), self.io_stream_client)
                self.io_stream_client.flush()
                self.print_bericht_gui_server(
                    f"{self.user} searched for a random restaurant in a country.")
            if command == "radius":
                location = pickle.load(self.io_stream_client)
                pickle.dump(self.dataset.search_by_radius(
                    self.user, location), self.io_stream_client)
                self.io_stream_client.flush()
                self.print_bericht_gui_server(
                    f"{self.user} searched for a random restaurant in a radius.")
            if command == "statistics":
                pickle.dump(self.dataset.return_stats(
                    self.user), self.io_stream_client)
                self.io_stream_client.flush()
                self.print_bericht_gui_server(
                    f"{self.user} searched for restaurant statistics.")
            if command == "graph":
                country = pickle.load(self.io_stream_client)
                self.dataset.return_graph(self.user, country)
                filename = os.path.join(os.path.dirname(__file__), f'../Server/images/graph.png')
                f = open(filename, 'rb')
                size_in_bytes = os.path.getsize(filename)
                number = math.ceil(size_in_bytes / 1024)

                pickle.dump("%d" % number, self.io_stream_client)
                self.io_stream_client.flush()
                l = f.read(1024)
                while (l):
                    self.socket_to_client.send(l)
                    l = f.read(1024)
                self.print_bericht_gui_server(
                    f"{self.user} searched for a graph of {country}.")

            command = pickle.load(self.io_stream_client)

        self.print_bericht_gui_server(f"{self.user.nickname} disconnected")
        self.clients.remove(self.user)
        self.socket_to_client.close()

    def print_bericht_gui_server(self, message):
        """
        The function is called by the client and the message is put in a queue. 

        The queue is then read by the GUI and the message is printed in the GUI

        :param message: The message to be sent to the client
        """
        self.messages_queue.put(f"CLH {self.id}:> {message}")
