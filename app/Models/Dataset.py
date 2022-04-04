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
        #pass
        self.dataset = pd.read_csv('tripadvisor_european_restaurants.csv')
        self.dataset = self.dataset.applymap(lambda s:s.lower() if type(s) == str else s)
    
    def search_by_name(self, user, name):
        Dataset.name_command +=1
        self.log_command(user, f"{user.name} ({user.nickname}) performed a search by name: {name}.\n")
        df = self.dataset[self.dataset['restaurant_name'].str.contains(name.lower())].iloc[0]
        return Restaurant(df['restaurant_name'], df['address'], df['price_level'], df['avg_rating'])

    def search_by_country(self, user, country, region):
        Dataset.country_command+=1
        self.log_command(user, f"{user.name} ({user.nickname}) performed a search by country and region: {region} in {country}.\n")
        df = self.dataset[self.dataset['country'].str.contains(country.lower()) & self.dataset['region'].str.contains(region.lower())]
        df = df.iloc[[random.randrange(len(df.index))]]
        df = df.iloc[0]
        return Restaurant(df['restaurant_name'], df['address'], df['price_level'], df['avg_rating'])

    def search_by_radius(self, user, location):
        Dataset.radius_command+=1
        self.log_command(user, f"{user.name} ({user.nickname}) performed a search by location: {location.lat}, {location.long}.\n")
        restaurants = []
        df = self.dataset[self.dataset['country'].str.contains(location.country.lower())]
        index = 0

        for i, r in df.iterrows():
            a = location.lat - float(r['latitude'])
            b = location.long - float(r['longitude'])
            c = sqrt(a * a  +  b * b)
            if c<location.radius:
                restaurants.append(index)
            index = index + 1

        df = df.iloc[[restaurants[random.randrange(len(restaurants))]]].iloc[0]
        return Restaurant(df['restaurant_name'], df['address'], df['price_level'], df['avg_rating'])

    def return_stats(self, user):
        Dataset.stats_command+=1
        self.log_command(user, f"{user.name} ({user.nickname}) inquired statistics.\n")
        countrys = self.dataset['country'].unique().tolist()
        stats = []
        for c in countrys:
            df = self.dataset[self.dataset['country'] == c]
            stats.append(CountryInfo(c, df['country'].count(), round(df['avg_rating'].mean(), 2)))
        return sorted(stats)

    def return_graph(self, user, country):
        Dataset.graph_command+=1
        self.log_command(user, f"{user.name} ({user.nickname}) generated a graph on the country {country}.\n")
        return f"graph {country.lower()}"

    def log_command(self, user, command):
        filename = f"{user.name}-{user.nickname}-{user.email}.txt"
        directory = '/app/logs/'
        location = os.path.join(directory, filename)
        print(location)
        f = open(location, "w")
        f.write(command)
        f.close()