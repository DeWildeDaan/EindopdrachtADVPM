class Restaurant:
    def __init__(self, name, address, price_level, rating):
        self.name = name
        self.address = address
        self.price_level = price_level
        self.rating = rating

    def __str__(self):
        return f"{self.name} ({self.price_level}) is located at {self.address} and is rated {self.rating} on average."