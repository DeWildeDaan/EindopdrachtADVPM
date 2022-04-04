import numpy as np
import matplotlib.pyplot as plt
import logging
import threading
import pickle
from Models.Dataset import Dataset
from Models.Location import Location
from Models.CountryInfo import CountryInfo
class ClientHandler(threading.Thread):

    numbers_clienthandlers = 0
    clients = []

    def __init__(self, socketclient, messages_queue, dataset):
        threading.Thread.__init__(self)
        self.dataset = dataset
        self.socket_to_client = socketclient
        self.messages_queue = messages_queue
        self.id = ClientHandler.numbers_clienthandlers
        ClientHandler.numbers_clienthandlers += 1

        io_stream_client = self.socket_to_client.makefile(mode='rwb')
        self.user = pickle.load(io_stream_client)
        self.print_bericht_gui_server(f"{self.user.nickname} connected")
        self.clients.append(self.user)

    def run(self):
        io_stream_client = self.socket_to_client.makefile(mode='rwb')
        logging.info("Started & waiting...")
        command = pickle.load(io_stream_client)

        while command != "CLOSE":
            if command == "name":
                name = pickle.load(io_stream_client)
                pickle.dump(self.dataset.search_by_name(self.user, name), io_stream_client)
                io_stream_client.flush()
            if command == "country":
                country = pickle.load(io_stream_client)
                region = pickle.load(io_stream_client)
                pickle.dump(self.dataset.search_by_country(self.user, country, region), io_stream_client)
                io_stream_client.flush()
            if command == "radius":
                location = pickle.load(io_stream_client)
                pickle.dump(self.dataset.search_by_radius(self.user, location), io_stream_client)
                io_stream_client.flush()
            if command == "statistics":
                pickle.dump(self.dataset.return_stats(self.user), io_stream_client)
                io_stream_client.flush()
            if command == "graph":
                country = pickle.load(io_stream_client)
                pickle.dump(self.dataset.return_graph(self.user, country), io_stream_client)
                io_stream_client.flush()


            command = pickle.load(io_stream_client)

        self.print_bericht_gui_server(f"{self.user.nickname} disconnected")
        self.clients.remove(self.user)
        self.socket_to_client.close()
    
    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")