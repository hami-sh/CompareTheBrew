import threading


class Item:
    # todo expand for alcohol content
    def __init__(self, store: str, brand: str, name: str, type: str,
                 price: float, link: str, ml: int, percent: str,
                 std_drinks: int, numb_items: int, efficiency: float,
                 image: str, promotion: bool, old_price: float):
        self.store = store
        self.brand = brand
        self.name = name
        self.price = price
        self.type = type
        self.link = link
        self.ml = ml
        self.percent = percent
        self.std_drinks = std_drinks
        self.numb_items = numb_items
        self.efficiency = efficiency
        self.image = image
        self.promotion = promotion
        self.old_price = old_price

    def __lt__(self, other):
        return self.efficiency < other.efficiency

    def __str__(self):
        # Create a new string
        repr_string = f"{self.store}, {self.brand}, {self.name}, " \
            f"${self.price}," \
            f"{self.type}, {self.link}, {self.ml}mL, {self.percent}, " \
            f"{self.std_drinks}, {self.numb_items}, {self.efficiency}, " \
            f"{self.image}, {self.promotion}, ${self.old_price}"
        return repr_string


class ItemCollection:
    def __init__(self):
        self._lock = threading.Lock()
        self.collection = []
