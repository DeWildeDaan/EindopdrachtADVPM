import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)
from Models.Restaurant import Restaurant
from Models.CountryInfo import CountryInfo
from Models.Location import Location
from Models.User import User
import json
import requests
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import *
from tkinter import WORD
import PIL.Image
from PIL import ImageTk, Image
import customtkinter
import tkinter as tk
import pickle
import socket
import logging
from msilib.schema import ListBox
from tabnanny import check
from urllib import response



class Window(Frame):
    def __init__(self, master=None):
        """
        It gets the IP address of the user and stores it in a variable.

        :param master: This represents the parent window.
        """
        Frame.__init__(self, master)
        self.master = master
        self.user = None
        self.init_window()
        self.__is_connected = False

        send_url = "http://api.ipstack.com/check?access_key=cdebf0737bdfa46c15cdfa66566b7223"
        geo_req = requests.get(send_url)
        self.geo_json = json.loads(geo_req.text)

    @property
    def is_connected(self):
        """
        It checks if the client is connected to the server.
        :return: The is_connected method is being returned.
        """
        return self.__is_connected

    def __del__(self):
        """
        It closes the connection to the database if it is open
        """
        self.close_connection()

    def clear_frame(self):
        """
        It destroys all the widgets in the frame and then forgets the frame
        """
        for widget in self.winfo_children():
            widget.destroy()
            self.pack_forget()

    def make_connection_server(self):
        """
        It makes a connection with the server and sends the user object to the server.
        """
        try:
            logging.info("Making connection with server...")
            host = socket.gethostname()
            port = 9999
            self.socket_to_server = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.socket_to_server.connect((host, port))
            self.in_out_server = self.socket_to_server.makefile(mode='rwb')
            logging.info("Open connection with server succesfully")
            pickle.dump(self.user, self.in_out_server)
            self.in_out_server.flush()
            self.__is_connected = True
        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Restaurants", "Something has gone wrong...")

    def close_connection(self):
        """
        It closes the connection with the server.
        """
        try:
            logging.info("Close connection with server...")
            pickle.dump("CLOSE", self.in_out_server)
            self.in_out_server.flush()
            self.socket_to_server.close()
        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Restaurants", "Something has gone wrong...")

    def init_window(self):
        """
        It creates a window with 3 entry fields and a button.
        """
        self.clear_frame()
        logging.debug("LOGIN WINDOW")
        self.master.title("Project ADV P&M")
        self.pack(fill=BOTH, expand=1)
        Grid.rowconfigure(self, 3, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

        # Labels
        customtkinter.CTkLabel(self, text="Full name:", pady=10).grid(row=0)
        customtkinter.CTkLabel(self, text="Nickname:", pady=10).grid(row=1)
        customtkinter.CTkLabel(self, text="E-mail:", pady=10).grid(row=2)

        # Entry's
        self.entry_name = customtkinter.CTkEntry(self, width=40)
        self.entry_name.grid(row=0, column=1, sticky=E + W, padx=(5, 5))

        self.entry_nickname = customtkinter.CTkEntry(self, width=40)
        self.entry_nickname.grid(row=1, column=1, sticky=E + W, padx=(5, 5))

        self.entry_email = customtkinter.CTkEntry(self, width=40)
        self.entry_email.grid(row=2, column=1, sticky=E + W, padx=(5, 5))

        # Buttons
        self.buttonLogin = customtkinter.CTkButton(
            self, text="Log in", command=lambda: self.login_check())
        self.buttonLogin.grid(row=3, column=0, columnspan=3, pady=(
            0, 5), padx=(5, 5), sticky=N + E + W)

    def command_window(self):
        """
        It creates a window with buttons that lead to other windows.
        """
        self.clear_frame()
        logging.debug("COMMAND WINDOW")
        self.pack(fill=BOTH, expand=1)
        Grid.rowconfigure(self, 4, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

        # Buttons
        self.buttonName = customtkinter.CTkButton(
            self, text="Search restaurant by name", command=lambda: self.name_window())
        self.buttonName.grid(row=0, column=0, columnspan=3, pady=(
            10, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonCountry = customtkinter.CTkButton(
            self, text="Random restaurant in country", command=lambda: self.country_window())
        self.buttonCountry.grid(row=1, column=0, columnspan=3, pady=(
            0, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonRadius = customtkinter.CTkButton(
            self, text="Random restaurant in radius", command=lambda: self.radius_window())
        self.buttonRadius.grid(row=2, column=0, columnspan=3, pady=(
            0, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonStatistics = customtkinter.CTkButton(
            self, text="Statistics per country", command=lambda: self.statistics_window())
        self.buttonStatistics.grid(row=3, column=0, columnspan=3, pady=(
            0, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonGraph = customtkinter.CTkButton(
            self, text="Restaurants per country", command=lambda: self.graph_window())
        self.buttonGraph.grid(row=4, column=0, columnspan=3, pady=(
            0, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonGraph = customtkinter.CTkButton(
            self, text="Log out", command=lambda: self.log_out())
        self.buttonGraph.grid(row=5, column=0, columnspan=3, pady=(
            0, 10), padx=(5, 5), sticky=E + W + S)

    def name_window(self):
        """
        It creates a window with a label, entry, and button.
        """
        self.clear_frame()
        logging.debug("SEARCH BY NAME WINDOW")
        self.pack(fill=BOTH, expand=1)
        Grid.rowconfigure(self, 4, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

        # Labels
        customtkinter.CTkLabel(
            self, text="Restaurant name:", pady=10).grid(row=0)
        customtkinter.CTkLabel(self, text="Result:", pady=10).grid(row=2)

        # Entry's
        self.entry_name = customtkinter.CTkEntry(self, width=40)
        self.entry_name.grid(row=0, column=1, sticky=E + W, padx=(5, 5))

        self.label_result = customtkinter.CTkLabel(
            self, width=40, wraplength=500)
        self.label_result.grid(row=3, column=0, columnspan=3, sticky=E + W)

        # Buttons
        self.buttonSearch = customtkinter.CTkButton(
            self, text="Search", command=lambda: self.search_by_name())
        self.buttonSearch.grid(row=4, column=1, pady=(
            0, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonBack = customtkinter.CTkButton(
            self, text="Back", command=lambda: self.command_window())
        self.buttonBack.grid(row=4, column=0, pady=(
            0, 10), padx=(5, 5), sticky=E + W + S)

    def country_window(self):
        """
        It creates a window with two entry boxes and a button. The button calls the function
        random_by_country()
        """
        self.clear_frame()
        logging.debug("RANDOM BY COUNTRY WINDOW")
        self.pack(fill=BOTH, expand=1)
        Grid.rowconfigure(self, 5, weight=1)
        Grid.columnconfigure(self, 1, weight=1)
        # Labels
        customtkinter.CTkLabel(self, text="Country:", pady=10).grid(row=0)
        customtkinter.CTkLabel(self, text="Region:", pady=10).grid(row=1)
        customtkinter.CTkLabel(self, text="Result:", pady=10).grid(row=2)

        # Entry's
        self.entry_country = customtkinter.CTkEntry(self, width=40)
        self.entry_country.grid(row=0, column=1, sticky=E + W, padx=(5, 5))

        self.entry_region = customtkinter.CTkEntry(self, width=40)
        self.entry_region.grid(row=1, column=1, sticky=E + W, padx=(5, 5))

        self.label_result = customtkinter.CTkLabel(
            self, width=40, wraplength=500)
        self.label_result.grid(row=3, column=0, columnspan=3, sticky=E + W)

        # Buttons
        self.buttonSearch = customtkinter.CTkButton(
            self, text="Search", command=lambda: self.random_by_country())
        self.buttonSearch.grid(row=4, column=1, pady=(
            0, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonBack = customtkinter.CTkButton(
            self, text="Back", command=lambda: self.command_window())
        self.buttonBack.grid(row=4, column=0, pady=(
            0, 10), padx=(5, 5), sticky=E + W + S)

    def radius_window(self):
        """
        It creates a window with a slider and a button. The slider is used to set the radius of the search
        and the button is used to execute the search.
        """
        self.clear_frame()
        logging.debug("RANDOM BY RADIUS WINDOW")
        self.pack(fill=BOTH, expand=1)
        Grid.rowconfigure(self, 5, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

        # Labels
        self.label_radius = customtkinter.CTkLabel(
            self, text="Radius (0 km):", pady=10)
        self.label_radius.grid(row=0)
        customtkinter.CTkLabel(self, text="Result:", pady=10).grid(row=2)

        # Entry's
        # self.slider = Scale(self, from_=0, to=20,
        #                     tickinterval=10, orient=HORIZONTAL)
        self.slider = customtkinter.CTkSlider(master=self,
                                              from_=0,
                                              to=20,
                                              number_of_steps=20,
                                              command=self.update_radius)
        self.slider.set(5)
        self.slider.grid(row=0, column=1, sticky=E + W, padx=(5, 5))

        self.label_result = customtkinter.CTkLabel(
            self, width=40, wraplength=500)
        self.label_result.grid(row=3, column=0, columnspan=3, sticky=E + W)

        # Buttons
        self.buttonSearch = customtkinter.CTkButton(
            self, text="Search", command=lambda: self.random_by_radius())
        self.buttonSearch.grid(row=4, column=1, pady=(
            0, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonBack = customtkinter.CTkButton(
            self, text="Back", command=lambda: self.command_window())
        self.buttonBack.grid(row=4, column=0, pady=(
            0, 10), padx=(5, 5), sticky=E + W + S)

    def statistics_window(self):
        """
        It creates a window with a listbox and a scrollbar.
        """
        self.clear_frame()
        logging.debug("STATISTICS WINDOW")
        self.pack(fill=BOTH, expand=1)
        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

        # Labels
        customtkinter.CTkLabel(self, text="Statistics per country:").grid(row=0, column=0)

        # Entry's
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.lstnumbers = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstnumbers.yview)

        self.lstnumbers.grid(row=1, column=0, columnspan=2,
                             padx=(5, 5), sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=1, sticky=N + S)

        # Buttons
        self.btn_text = StringVar()
        self.btn_text.set("Back")
        self.buttonServer = customtkinter.CTkButton(
            self, textvariable=self.btn_text, command=lambda: self.command_window())
        self.buttonServer.grid(row=3, column=0, columnspan=2, pady=(
            10, 0), padx=(5, 5), sticky=N + E + W)
        self.statistics()

    def graph_window(self):
        """
        It creates a window with a label, an entry, a button and a label.
        """
        self.clear_frame()
        logging.debug("GRAPH WINDOW")
        self.pack(fill=BOTH, expand=1)
        Grid.rowconfigure(self, 5, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

        # Labels
        customtkinter.CTkLabel(self, text="Country:", pady=10).grid(row=0)
        customtkinter.CTkLabel(self, text="Result:", pady=10).grid(row=2)

        self.lblimg = customtkinter.CTkLabel(self)
        self.lblimg.grid(row=4, column=0, columnspan=2, pady=(
            0, 5), padx=(5, 5), sticky=N + S + E + W)

        # Entry's
        self.entry_country = customtkinter.CTkEntry(self, width=40)
        self.entry_country.grid(row=0, column=1, sticky=E + W, padx=(5, 5))

        # Buttons
        self.buttonSearch = customtkinter.CTkButton(
            self, text="Search", command=lambda: self.graph())
        self.buttonSearch.grid(row=5, column=1, pady=(
            0, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonBack = customtkinter.CTkButton(
            self, text="Back", command=lambda: self.command_window())
        self.buttonBack.grid(row=5, column=0, pady=(
            0, 10), padx=(5, 5), sticky=E + W + S)

    def login_check(self):
        """
        If the name, nickname and email fields are not empty, create a user object and open the command
        window.
        """
        name = self.entry_name.get()
        nickname = self.entry_nickname.get()
        email = self.entry_email.get()
        check_count = 0
        if name == "":
            warn = "Name can't be empty!"
        else:
            check_count += 1
            logging.debug("Full name OK")
            if nickname == "":
                warn = "Nickname can't be empty!"
            else:
                check_count += 1
                logging.debug("Nickname OK")
                if email == "":
                    warn = "Email can't be empty!"
                else:
                    logging.debug("Email OK")
                    check_count += 1

        if check_count == 3:
            self.user = User(name.replace(" ", ""), nickname.replace(
                " ", ""), email.replace(" ", ""))
            logging.debug("User created")
            self.make_connection_server()
            if self.__is_connected:
                self.command_window()
        else:
            messagebox.showerror('', warn)

    def log_out(self):
        """
        It sets the is_connected variable to False, closes the connection, and then calls the init_window
        function.
        """
        self.__is_connected = False
        self.close_connection()
        self.init_window()

    def search_by_name(self):
        """
        It sends a string to the server, which then searches for a restaurant with that name and returns
        the result.
        """
        try:
            name = self.entry_name.get()

            pickle.dump("name", self.in_out_server)
            logging.debug(name)
            pickle.dump(name, self.in_out_server)
            self.in_out_server.flush()

            # resultaat afwachten
            response = pickle.load(self.in_out_server)
            logging.info('Got a response from server')
            logging.debug(response)
            self.label_result['text'] = f"{response}"

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Restaurants", "Something has gone wrong...")

    def random_by_country(self):
        """
        It sends a request to the server to get a random restaurant from a country and region.
        """
        try:
            country = self.entry_country.get()
            region = self.entry_region.get()

            pickle.dump("country", self.in_out_server)
            logging.debug(country)
            pickle.dump(country, self.in_out_server)
            pickle.dump(region, self.in_out_server)
            self.in_out_server.flush()

            # resultaat afwachten
            response = pickle.load(self.in_out_server)
            logging.info('Got a response from server')
            logging.debug(response)
            self.label_result['text'] = f"{response}"

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Restaurants", "Something has gone wrong...")

    def random_by_radius(self):
        """
        It sends a location object to the server, which then returns a restaurant object.
        """
        try:
            radius = self.slider.get()
            location = Location(
                self.geo_json['latitude'], self.geo_json['longitude'], radius, self.geo_json['country_name'])

            pickle.dump("radius", self.in_out_server)
            logging.debug(location)
            pickle.dump(location, self.in_out_server)
            self.in_out_server.flush()

            # resultaat afwachten
            response = pickle.load(self.in_out_server)
            logging.info('Got a response from server')
            logging.debug(response)
            self.label_result['text'] = f"{response}"

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Restaurants", "Something has gone wrong...")

    def statistics(self):
        """
        It sends a message to the server to get the statistics.
        """
        try:
            pickle.dump("statistics", self.in_out_server)
            self.in_out_server.flush()

            # resultaat afwachten
            response = pickle.load(self.in_out_server)
            logging.info('Got a response from server')
            logging.debug(response)
            for c in response:
                self.lstnumbers.insert(END, c)

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Restaurants", "Something has gone wrong...")

    def graph(self):
        """
        It sends a request to the server to get a graph of the number of restaurants in a country. The
        server sends the graph back to the client, which then displays it.
        """
        try:
            country = self.entry_country.get()

            pickle.dump("graph", self.in_out_server)
            logging.debug(country)
            pickle.dump(country, self.in_out_server)
            self.in_out_server.flush()

            # resultaat afwachten
            response = pickle.load(self.in_out_server)
            number_of_sends = int(response)

            with open('received_file', 'wb+') as f:
                for i in range(0, number_of_sends):
                    data = self.socket_to_server.recv(1024)
                    f.write(data)
            logging.info('Successfully got the image')
            fp = open("received_file", "rb")
            im = PIL.Image.open(fp)
            self.img = ImageTk.PhotoImage(PIL.Image.open(fp))
            self.lblimg['image'] = self.img
            width, height = im.size
            self.master.geometry("%dx%d" % (width, height+200))

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Restaurants", "Something has gone wrong...")

    def update_radius(self, radius):
        self.label_radius['text'] = f"Radius ({radius} km):"


logging.basicConfig(level=logging.DEBUG)
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")
root = customtkinter.CTk()
app = Window(root)
root.geometry("600x220")
root.mainloop()
