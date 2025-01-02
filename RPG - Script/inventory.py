from items import Items

class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item):
        # If the item already exists, increase its quantity
        if item.name in self.items:
            self.items[item.name].increase_quantity(item.quantity)
        else:
            self.items[item.name] = Items(item.name, item.effect, item.quantity, item.description)

    def remove_item(self, item_name, quantity):
        # If the item exists and the quantity is sufficient
        if item_name in self.items and self.items[item_name].quantity >= quantity:
            self.items[item_name].decrease_quantity(quantity)
            if self.items[item_name].quantity == 0:
                del self.items[item_name]
        else:
            print(f"Item {item_name} not found or insufficient quantity.")

    def view_inventory(self):
        # Show each item with its name, quantity, and description
        return {item: str(self.items[item]) for item in self.items}

