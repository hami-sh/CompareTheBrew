import threading

class Item:
    # todo expand for alcohol content
    def __init__(self, store, brand, name, price, link, ml, percent, stdDrinks, efficiency):
        self.store = store
        self.brand = brand
        self.name = name
        self.price = price
        self.link = link
        self.ml = ml
        self.percent = percent
        self.stdDrinks = stdDrinks
        self.efficiency = efficiency

    def __lt__(self, other):
        return self.efficiency < other.efficiency

class ItemCollection:
    def __init__(self):
        self._lock = threading.Lock()
        self.collection = []

