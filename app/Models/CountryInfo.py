class CountryInfo:
    def __init__(self, name, total_restaurants, avg_rating):
        self.name = name
        self.total_restaurants = total_restaurants
        self.avg_rating = avg_rating

    def __str__(self):
        return f"{self.name} has {self.total_restaurants} restaurants with an average rating of {self.avg_rating}"
    
    def __eq__(self, other):
        return (self.total_restaurants == other.total_restaurants)
    
    def __lt__(self, other):
        return ((self.total_restaurants) < (other.total_restaurants))