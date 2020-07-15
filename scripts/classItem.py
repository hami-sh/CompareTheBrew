import threading

class Item:
    # todo expand for alcohol content
    def __init__(self, store, brand, name, type, price, link, ml, percent, std_drinks, numb_items, efficiency, image, promotion, old_price):
        self.store = store
        self.brand = brand
        self.name = name
        self.price = price
        self.type = type
        self.link = link
        self.ml = ml
        self.percent = percent
        self.stdDrinks = std_drinks
        self.numb_items = numb_items
        self.efficiency = efficiency
        self.image = image
        self.promotion = promotion
        self.old_price = old_price

    def __lt__(self, other):
        return self.efficiency < other.efficiency

    def __repr__(self):
        # Create a new string
        reprString = ""
        # Add the instance properties to the reprString
        reprString += self.store + ","
        reprString += self.brand + ","
        reprString += self.name + ","
        reprString += self.type + ","
        reprString += str(self.percent) + ","
        reprString += str(self.ml) + ","
        reprString += str(self.numb_items) + ","
        reprString += str(self.stdDrinks) + ","
        reprString += str(self.price) + ","
        reprString += str(self.efficiency) + ","
        reprString += self.link + ","
        reprString += self.image
        return reprString

class ItemCollection:
    def __init__(self):
        self._lock = threading.Lock()
        self.collection = []
