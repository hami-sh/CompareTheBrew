import threading

class Item:
    # todo expand for alcohol content
    def __init__(self, store, brand, name, type, price, link, ml, percent, stdDrinks, efficiency, image):
        self.store = store
        self.brand = brand
        self.name = name
        self.price = price
        self.type = type
        self.link = link
        self.ml = ml
        self.percent = percent
        self.stdDrinks = stdDrinks
        self.efficiency = efficiency
        self.image = image

    def __lt__(self, other):
        return self.efficiency < other.efficiency

    def __repr__(self):
        # Create a new string
        reprString = "<Item>"
        # Add the instance properties to the reprString
        reprString += self.store + ","
        reprString += self.brand + ","
        reprString += self.name + ","
        reprString += str(self.price) + ","
        reprString += self.type + ","
        reprString += self.link + ","
        reprString += str(self.ml) + ","
        reprString += str(self.percent) + ","
        reprString += str(self.stdDrinks) + ","
        reprString += str(self.efficiency) + ","
        reprString += self.image
        return reprString

class ItemCollection:
    def __init__(self):
        self._lock = threading.Lock()
        self.collection = []
