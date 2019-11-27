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

    def __repr__(self):
        # Create a new string
        reprString = "<Item>"
        # Add the instance properties to the reprString
        reprString += "store:" + self.store + ","
        reprString += "brand:" + self.brand + ","
        reprString += "name:" + self.name + ","
        reprString += "price:" + self.price + ","
        reprString += "link:" + self.link + ","
        reprString += "ml:" + self.ml + ","
        reprString += "percent:" + self.percent + ","
        reprString += "stdDrinks:" + self.stdDrinks + ","
        reprString += "efficiency:" + str(self.efficiency)
        # Return the reprString
        return reprString

class ItemCollection:
    def __init__(self):
        self._lock = threading.Lock()
        self.collection = []
