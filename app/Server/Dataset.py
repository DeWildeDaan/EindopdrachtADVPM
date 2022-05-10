from itertools import count
from msilib.schema import Directory
import sys
import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import random
from math import sqrt
from Models.Restaurant import Restaurant
from Models.Location import Location
from Models.CountryInfo import CountryInfo


class Dataset:
    dataset = None
    name_command = 0
    country_command = 0
    radius_command = 0
    stats_command = 0
    graph_command = 0

    def __init__(self):
        """
        It reads in the dataset, and then converts all the strings in the dataset to lowercase.
        """
        self.get_command_stats()
        self.dataset = pd.read_csv(os.path.join(os.path.dirname(
            __file__), '../Server/tripadvisor_european_restaurants.csv'))
        self.dataset = self.dataset.applymap(
            lambda s: s.lower() if type(s) == str else s)

    def search_by_name(self, user, name):
        """
        It searches for a restaurant by name.

        :param user: The user who is requesting the restaurant
        :param name: the name of the restaurant
        :return: A restaurant object.
        """
        Dataset.name_command += 1
        self.log_command(
            user, f"{user.name} ({user.nickname}) performed a search by name: {name}.\n")
        df = self.dataset[self.dataset['restaurant_name'].str.contains(
            name.lower())].iloc[0]
        return Restaurant(df['restaurant_name'], df['address'], df['price_level'], df['avg_rating'])

    def search_by_country(self, user, country, region):
        """
        It takes in a user, country, and region, and returns a restaurant object

        :param user: The user who is requesting the restaurant
        :param country: The country the user wants to search in
        :param region: The region of the country you want to search in
        :return: A restaurant object
        """
        Dataset.country_command += 1
        self.log_command(
            user, f"{user.name} ({user.nickname}) performed a search by country and region: {region} in {country}.\n")
        df = self.dataset[self.dataset['country'].str.contains(
            country.lower()) & self.dataset['region'].str.contains(region.lower())]
        df = df.iloc[[random.randrange(len(df.index))]]
        df = df.iloc[0]
        return Restaurant(df['restaurant_name'], df['address'], df['price_level'], df['avg_rating'])

    def search_by_radius(self, user, location):
        """
        It searches the dataset for restaurants within a certain radius of a given location

        :param user: The user who is requesting the restaurant
        :param location: Location
        :return: A restaurant object
        """
        Dataset.radius_command += 1
        self.log_command(
            user, f"{user.name} ({user.nickname}) performed a search by location: {location.lat}, {location.long}.\n")
        restaurants = []
        df = self.dataset[self.dataset['country'].str.contains(
            location.country.lower())]
        index = 0

        for i, r in df.iterrows():
            a = location.lat - float(r['latitude'])
            b = location.long - float(r['longitude'])
            c = sqrt(a * a + b * b)
            if c < location.radius:
                restaurants.append(index)
            index = index + 1

        df = df.iloc[[restaurants[random.randrange(len(restaurants))]]].iloc[0]
        return Restaurant(df['restaurant_name'], df['address'], df['price_level'], df['avg_rating'])

    def return_stats(self, user):
        """
        It takes a user object and returns a list of CountryInfo objects

        :param user: The user who is requesting the statistics
        :return: A list of CountryInfo objects.
        """
        Dataset.stats_command += 1
        self.log_command(
            user, f"{user.name} ({user.nickname}) inquired statistics.\n")
        countrys = self.dataset['country'].unique().tolist()
        stats = []
        for c in countrys:
            df = self.dataset[self.dataset['country'] == c]
            stats.append(CountryInfo(
                c, df['country'].count(), round(df['avg_rating'].mean(), 2)))
        return sorted(stats)

    def return_graph(self, user, country):
        """
        It takes a user and a country as parameters, and returns a graph of the number of restaurants per
        province in that country.

        :param user: the user who requested the graph
        :param country: The country to be searched for
        """
        Dataset.graph_command += 1
        self.log_command(
            user, f"{user.name} ({user.nickname}) generated a graph on the country {country}.\n")
        df = self.dataset[self.dataset['country'].str.contains(
            country.lower())]
        plt.figure(figsize=(10, 5))
        plt.grid()
        plt.xticks(rotation=90)
        sns.countplot(data=df, x=df['province']).set(
            title=f'Restaurants from {country} per province')
        plt.savefig(os.path.join(os.path.dirname(__file__),
                    '../Server/images/graph.png'), bbox_inches='tight')

    def log_command(self, user, command):
        """
        It takes a user object and a command string and writes the command to a file

        :param user: The user object
        :param command: The command that the user typed in
        """
        self.log_command_stats()
        directory = os.path.join(os.path.dirname(
            __file__), f'../Server/logs/{user.name}-{user.nickname}-{user.email}.txt')
        print(directory)
        f = open(directory, "a")
        f.write(command)
        f.close()

    def log_command_stats(self):
        """
        It writes the number of times each command has been used to a text file
        """
        directory = os.path.join(os.path.dirname(
            __file__), f'../Server/commands.txt')
        f = open(directory, "w")
        f.write(f'{Dataset.name_command},{Dataset.country_command},{Dataset.radius_command},{Dataset.stats_command},{Dataset.graph_command}')
        f.close()

    def get_command_stats(self):
        """
        It reads a file and assigns the values to variables.
        """
        location = os.path.join(os.path.dirname(
            __file__), f'../Server/commands.txt')
        f = open(location, "r")
        firstline = f.readline().rstrip()
        firstline = firstline.split(',')
        f.close()
        Dataset.name_command = int(firstline[0])
        Dataset.country_command = int(firstline[1])
        Dataset.radius_command = int(firstline[2])
        Dataset.stats_command = int(firstline[3])
        Dataset.graph_command = int(firstline[4])
