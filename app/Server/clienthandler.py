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
        #io_stream_client = self.socket_to_client.makefile(mode='rwb')
        logging.info("Started & waiting...")
        command = pickle.load(self.io_stream_client)

        while command != "CLOSE":
            if command == "name":
                name = pickle.load(self.io_stream_client)
                pickle.dump(self.dataset.search_by_name(self.user, name), self.io_stream_client)
                self.io_stream_client.flush()
            if command == "country":
                country = pickle.load(self.io_stream_client)
                region = pickle.load(self.io_stream_client)
                pickle.dump(self.dataset.search_by_country(self.user, country, region), self.io_stream_client)
                self.io_stream_client.flush()
            if command == "radius":
                location = pickle.load(self.io_stream_client)
                pickle.dump(self.dataset.search_by_radius(self.user, location), self.io_stream_client)
                self.io_stream_client.flush()
            if command == "statistics":
                pickle.dump(self.dataset.return_stats(self.user), self.io_stream_client)
                self.io_stream_client.flush()
            if command == "graph":
                country = pickle.load(self.io_stream_client)
                self.dataset.return_graph(self.user, country)
               
                filename = "c:/Users/daand/OneDrive - Hogeschool West-Vlaanderen/School/S4/Advanced Programming and Maths/EindopdrachtADVPM/app/Server/images/graph.png"
                f = open(filename, 'rb')
                #bepaal de bestandsgrootte
                size_in_bytes = os.path.getsize(filename)
                #bereken hoeveel keer 1024 bytes verstuurd zullen worden
                number = math.ceil(size_in_bytes / 1024)

                #voorbereiding: ik geef dit aantal door aan de cliënt zodat hij weet hoeveel keer
                #hij het readcommando zal moeten doen (om zo de afbeelding volledig binnen te halen)
                pickle.dump("%d" % number, self.io_stream_client)
                self.io_stream_client.flush()
                #volgende stap: het effectief versturen van de afbeelding
                l = f.read(1024)
                while (l):
                    self.socket_to_client.send(l)
                    # volgende 1024 bytes inlezen
                    l = f.read(1024)


            command = pickle.load(self.io_stream_client)

        self.print_bericht_gui_server(f"{self.user.nickname} disconnected")
        self.clients.remove(self.user)
        self.socket_to_client.close()
    
    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")