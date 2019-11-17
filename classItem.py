import threading

class Item:
    # todo expand for alcohol content
    def __init__(self, store, brand, name, price):
        self.store = store
        self.brand = brand
        self.name = name
        self.price = price

class ItemCollection:
    def __init__(self):
        self._lock = threading.Lock()
        self.collection = []

