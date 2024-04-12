from collections import deque


class DayData:
    def __init__(self, day_number, entry_date, is_workday, demands):
        self.day_number = day_number
        self.entry_date = entry_date
        self.is_workday = is_workday
        self.demands = demands

    def __repr__(self):
        return (f"DayData(day_number={self.day_number}, entry_date={self.entry_date}, "
                f"is_workday={self.is_workday}, demands={self.demands})")


class CustomerOrder:
    def __init__(self, quantity, due_date):
        self.quantity = quantity
        self.due_date = due_date


class HerbExtractOrder:
    def __init__(self, quantity, delivery_date):
        self.quantity = quantity
        self.delivery_date = delivery_date

class UsedTankContainer:
    def __init__(self, quantity_left, economic_expiry_date):
        self.quantity_left = quantity_left
        self.economic_expiry_date = economic_expiry_date

class SimulationStatus:
    def __init__(self, config):
        # Initialize a deque for each product type
        self.open_customer_orders = [deque() for _ in config['product_name']]
        # Initialize a deque for each herb type
        self.open_extraction_orders = [deque() for _ in config['herb_available_months']]
        # Initialize herb inventory as a list of zeros
        self.herb_inventory = config['initial_herb_inventory'].copy()
        self.tank_container_inventory = [deque() for _ in range(2)]
        self.tank_containers_in_use = 0
        self.day_number = 0
        self.current_product_per_filling_machine = config['initial_product_per_filling_line']

    def add_product_order(self, product_index, quantity, due_date):
        self.open_customer_orders[product_index].append(CustomerOrder(quantity, due_date))

    def add_extraction_order(self, herb_id, quantity, delivery_date):
        self.open_extraction_orders[herb_id].append(HerbExtractOrder(quantity, delivery_date))
