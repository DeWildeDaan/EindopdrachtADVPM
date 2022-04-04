from msilib.schema import ListBox
import sys
from pathlib import Path
from tabnanny import check
sys.path[0] = str(Path(sys.path[0]).parent)
# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import logging
import socket
import pickle
import tkinter as tk
from tkinter import WORD
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import requests
import json

from Models.User import User
from Models.Location import Location
from Models.CountryInfo import CountryInfo
from Models.Restaurant import Restaurant



class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.user = None
        self.init_window()

        send_url = "http://api.ipstack.com/check?access_key=cdebf0737bdfa46c15cdfa66566b7223"
        geo_req = requests.get(send_url)
        self.geo_json = json.loads(geo_req.text)
    
    def __del__(self):
        self.close_connection()
    
    def clearFrame(self):
        for widget in self.winfo_children():
            widget.destroy()
            self.pack_forget()

    def makeConnnectionWithServer(self):
        try:
            logging.info("Making connection with server...")
            # get local machine name
            host = socket.gethostname()
            port = 9999
            self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connection to hostname on the port.
            self.socket_to_server.connect((host, port))
            self.in_out_server = self.socket_to_server.makefile(mode='rwb')
            logging.info("Open connection with server succesfully")

            pickle.dump(self.user, self.in_out_server)
            self.in_out_server.flush()
        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")

    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            pickle.dump("CLOSE", self.in_out_server)
            self.in_out_server.flush()
            self.socket_to_server.close()
        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Sommen", "Something has gone wrong...")



    # Display init_window (Login screen)
    def init_window(self):
        logging.debug("LOGIN WINDOW")
        self.master.title("Project ADV P&M")
        self.pack(fill=BOTH, expand=1)
        Grid.rowconfigure(self, 3, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

        # Labels
        Label(self, text="Full name:", pady=10).grid(row=0)
        Label(self, text="Nickname:", pady=10).grid(row=1)
        Label(self, text="E-mail:", pady=10).grid(row=2)
        
        # Entry's
        self.entry_name = Entry(self, width=40)
        self.entry_name.grid(row=0, column=1, sticky=E + W, padx=(5, 5))

        self.entry_nickname = Entry(self, width=40)
        self.entry_nickname.grid(row=1, column=1, sticky=E + W, padx=(5, 5))

        self.entry_email = Entry(self, width=40)
        self.entry_email.grid(row=2, column=1, sticky=E + W, padx=(5, 5))

        # Buttons
        self.buttonLogin = Button(self, text="Log in", command=lambda:self.login_check())
        self.buttonLogin.grid(row=3, column=0, columnspan=3, pady=(0, 5), padx=(5, 5), sticky=N + E + W)

    # Display commands window
    def command_window(self):
        self.clearFrame()
        logging.debug("COMMAND WINDOW")
        self.pack(fill=BOTH, expand=1)
        Grid.rowconfigure(self, 4, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

        # Buttons
        self.buttonName = Button(self, text="Search restaurant by name", command=lambda:self.name_window())
        self.buttonName.grid(row=0, column=0, columnspan=3,pady=(10, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonCountry = Button(self, text="Random restaurant in country", command=lambda:self.country_window())
        self.buttonCountry.grid(row=1, column=0, columnspan=3,pady=(0, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonRadius = Button(self, text="Random restaurant in radius", command=lambda:self.radius_window())
        self.buttonRadius.grid(row=2, column=0, columnspan=3,pady=(0, 10), padx=(5, 5), sticky=E + W + S)
        
        self.buttonStatistics = Button(self, text="Statistics per country", command=lambda:self.statistics_window())
        self.buttonStatistics.grid(row=3, column=0, columnspan=3,pady=(0, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonGraph = Button(self, text="Restaurants per country", command=lambda:self.graph_window())
        self.buttonGraph.grid(row=4, column=0, columnspan=3,pady=(0, 10), padx=(5, 5), sticky=E + W + S)
        
    # Display search by name window
    def name_window(self):
        self.clearFrame()
        logging.debug("SEARCH BY NAME WINDOW")
        self.pack(fill=BOTH, expand=1)
        Grid.rowconfigure(self, 4, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

        # Labels
        Label(self, text="Restaurant name:", pady=10).grid(row=0)
        Label(self, text="Result:", pady=10).grid(row=2)

        # Entry's
        self.entry_name = Entry(self, width=40)
        self.entry_name.grid(row=0, column=1, sticky=E + W, padx=(5, 5))

        self.label_result = Label(self, width=40, wraplength=500)
        self.label_result.grid(row=3, column=0, columnspan=3, sticky=E + W)

        # Buttons
        self.buttonSearch = Button(self, text="Search", command=lambda:self.search_by_name())
        self.buttonSearch.grid(row=4, column=1,pady=(0, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonBack = Button(self, text="Back", command=lambda:self.command_window())
        self.buttonBack.grid(row=4, column=0,pady=(0, 10), padx=(5, 5), sticky=E + W + S)
        
    # Display search random by country&region window
    def country_window(self):
        self.clearFrame()
        logging.debug("RANDOM BY COUNTRY WINDOW")
        self.pack(fill=BOTH, expand=1)
        Grid.rowconfigure(self, 5, weight=1)
        Grid.columnconfigure(self, 1, weight=1)
        # Labels
        Label(self, text="Country:", pady=10).grid(row=0)
        Label(self, text="Region:", pady=10).grid(row=1)
        Label(self, text="Result:", pady=10).grid(row=2)

        # Entry's
        self.entry_country = Entry(self, width=40)
        self.entry_country.grid(row=0, column=1, sticky=E + W, padx=(5, 5))

        self.entry_region = Entry(self, width=40)
        self.entry_region.grid(row=1, column=1, sticky=E + W, padx=(5, 5))

        self.label_result = Label(self, width=40, wraplength=500)
        self.label_result.grid(row=3, column=0, columnspan=3, sticky=E + W)

        # Buttons
        self.buttonSearch = Button(self, text="Search", command=lambda:self.random_by_country())
        self.buttonSearch.grid(row=4, column=1,pady=(0, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonBack = Button(self, text="Back", command=lambda:self.command_window())
        self.buttonBack.grid(row=4, column=0,pady=(0, 10), padx=(5, 5), sticky=E + W + S)
    
    # Display search random by coordinates and radius window
    def radius_window(self):
        self.clearFrame()
        logging.debug("RANDOM BY RADIUS WINDOW")
        self.pack(fill=BOTH, expand=1)
        Grid.rowconfigure(self, 5, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

        # Labels
        Label(self, text="Radius (in km):", pady=10).grid(row=0)
        Label(self, text="Result:", pady=10).grid(row=2)

        # Entry's
        self.slider = Scale(self, from_=0, to=20,tickinterval=10, orient=HORIZONTAL)
        self.slider.set(5)
        self.slider.grid(row=0, column=1, sticky=E + W, padx=(5, 5))

        self.label_result = Label(self, width=40, wraplength=500)
        self.label_result.grid(row=3, column=0, columnspan=3, sticky=E + W)

        # Buttons
        self.buttonSearch = Button(self, text="Search", command=lambda:self.random_by_radius())
        self.buttonSearch.grid(row=4, column=1,pady=(0, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonBack = Button(self, text="Back", command=lambda:self.command_window())
        self.buttonBack.grid(row=4, column=0,pady=(0, 10), padx=(5, 5), sticky=E + W + S)
    
    # Display statistics window
    def statistics_window(self):
        self.clearFrame()
        logging.debug("STATISTICS WINDOW")
        self.pack(fill=BOTH, expand=1)
        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        

        # Labels
        Label(self, text="Statistics per country:").grid(row=0, column=0)

        # Entry's
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.lstnumbers = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstnumbers.yview)

        self.lstnumbers.grid(row=1, column=0, columnspan=2, padx=(5, 5), sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=1, sticky=N + S)
        
        # Buttons
        self.btn_text = StringVar()
        self.btn_text.set("Back")
        self.buttonServer = Button(self, textvariable=self.btn_text, command=lambda:self.command_window())
        self.buttonServer.grid(row=3, column=0, columnspan=2, pady=(10, 0), padx=(5, 5), sticky=N + E + W)
        
        self.statistics()

    # Display graph window
    def graph_window(self):
        self.clearFrame()
        logging.debug("GRAPH WINDOW")
        self.pack(fill=BOTH, expand=1)
        Grid.rowconfigure(self, 5, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

        # Labels
        Label(self, text="Country:", pady=10).grid(row=0)
        Label(self, text="Result:", pady=10).grid(row=2)

        # Entry's
        self.entry_country = Entry(self, width=40)
        self.entry_country.grid(row=0, column=1, sticky=E + W, padx=(5, 5))

        self.label_result = Label(self, width=40, wraplength=500)
        self.label_result.grid(row=3, column=1, sticky=E + W)

        # Buttons
        self.buttonSearch = Button(self, text="Search", command=lambda:self.graph())
        self.buttonSearch.grid(row=4, column=1,pady=(0, 10), padx=(5, 5), sticky=E + W + S)

        self.buttonBack = Button(self, text="Back", command=lambda:self.command_window())
        self.buttonBack.grid(row=4, column=0,pady=(0, 10), padx=(5, 5), sticky=E + W + S)



    def login_check(self):
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
            self.user = User(name, nickname, email)
            logging.debug("User created")
            self.command_window()
            self.makeConnnectionWithServer()
        else:
            messagebox.showerror('', warn)

    def search_by_name(self):
        try:
            name = self.entry_name.get()

            pickle.dump("name", self.in_out_server)
            #self.in_out_server.flush()
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
            messagebox.showinfo("Sommen", "Something has gone wrong...")
    
    def random_by_country(self):
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
            messagebox.showinfo("Sommen", "Something has gone wrong...")

    def random_by_radius(self):
        try:
            radius = self.slider.get()
            location = Location(self.geo_json['latitude'], self.geo_json['longitude'], radius, self.geo_json['country_name'])

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
            messagebox.showinfo("Sommen", "Something has gone wrong...")

    def statistics(self):
        try:
            pickle.dump("statistics", self.in_out_server)
            self.in_out_server.flush()

            # resultaat afwachten
            response = pickle.load(self.in_out_server)
            logging.info('Got a response from server')
            logging.debug(response)
            for c in response:
                #print(c)
                self.lstnumbers.insert(END, c)

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Sommen", "Something has gone wrong...")

    def graph(self):
        try:
            country = self.entry_country.get()

            pickle.dump("graph", self.in_out_server)
            logging.debug(country)
            pickle.dump(country, self.in_out_server)
            self.in_out_server.flush()

            # resultaat afwachten
            response = pickle.load(self.in_out_server)
            logging.info('Got a response from server')
            logging.debug(response)
            self.label_result['text'] = f"{response}"

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")
            messagebox.showinfo("Sommen", "Something has gone wrong...")


logging.basicConfig(level=logging.DEBUG)

root = Tk()
app = Window(root)
root.geometry("600x200")
root.mainloop()
