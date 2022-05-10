import logging
import socket
import threading
import pickle
import pandas as pd
import multiprocessing

from Server.clienthandler import ClientHandler

logging.basicConfig(level=logging.INFO)


class Server(threading.Thread):

    def __init__(self, host, port, messages_queue, dataset):
        """
        The above function is a constructor for the class. It initializes the threading.Thread class, and
        sets the host, port, messages_queue, and dataset variables.

        :param host: the IP address of the server
        :param port: The port number that the server will listen on
        :param messages_queue: A queue that contains the messages that the server will send to the client
        :param dataset: a list of dictionaries, each dictionary contains a set of key-value pairs
        """
        threading.Thread.__init__(self, name="Thread-Server")
        self.dataset = dataset
        self.__is_connected = False
        self.host = host
        self.port = port
        self.messages_queue = messages_queue

    @property
    def is_connected(self):
        """
        It checks if the client is connected to the server.
        :return: The is_connected method is being returned.
        """
        return self.__is_connected

    def init_server(self):
        """
        It creates a socket object and binds it to the host and port.
        """
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(5)
        self.__is_connected = True
        self.print_bericht_gui_server("SERVER STARTED")

    def close_server_socket(self):
        """
        It closes the server socket if it is not None
        """
        if self.serversocket is not None:
            self.serversocket.close()

    def run(self):
        """
        It creates a new thread for each client that connects to the server
        """
        number_received_message = 0
        try:
            while True:
                self.print_bericht_gui_server("waiting for a new client...")
                socket_to_client, addr = self.serversocket.accept()
                self.print_bericht_gui_server(f"Got a connection from {addr}")
                clh = ClientHandler(
                    socket_to_client, self.messages_queue, self.dataset)
                clh.start()
                self.print_bericht_gui_server(
                    f"Current Thread count: {threading.active_count()}.")

        except Exception as ex:
            self.print_bericht_gui_server("Serversocket afgesloten")

    def print_bericht_gui_server(self, message):
        """
        It takes a message, puts it in a queue, and then calls a function that prints the message

        :param message: The message to be sent to the client
        """
        self.messages_queue.put(f"Server:> {message}")
