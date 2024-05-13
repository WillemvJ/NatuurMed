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
        self.delivery_date = None


class HerbExtractOrder:
    def __init__(self, quantity, completion_date):
        self.quantity = quantity
        self.delivery_date = completion_date


class MixTankContainerInUse:
    def __init__(self, quantity_left, economic_expiry_date):
        self.quantity_left = quantity_left
        self.economic_expiry_date = economic_expiry_date


# when initialized, this corresponds to the situation in the system on day 0
# it is updated everyday to keep track of everything in the system.
class SimulationStatus:
    def __init__(self, config):
        # Initialize a deque for each product type
        self.open_customer_orders = [deque() for _ in config['product_name']]
        # Initialize a deque for each herb type
        self.open_extraction_orders = [deque() for _ in config['herb_available_months']]
        # Initialize herb inventory
        self.herb_inventory = config['initial_herb_inventory'].copy()
        # updated later, initialize at 0
        self.remaining_mix_inventory = [0,0]

        self.mix_storage_container_inventory = [deque() for _ in range(2)]
        self.mix_storage_containers_in_use = 0
        self.day_number = 0
        self.current_product_per_filling_line = config['initial_product_per_filling_line']
        self.remaining_setup_time_per_filling_line_from_previous_day = [0, 0]
        # Initialize tank containers based on configuration so if initially we have
        # num_initial_mix_storage_containers = [2,2], then we have 2 containers of 5000 each of CL, and 2 of AD. note
        # that calling add_mix_container updates the lists of mix_storage_container_inventory, as well as the
        # mix_storage_container_in_use as well as the remaining mix inventory.
        for mix_type in range(len(config['num_initial_mix_storage_containers'])):
            for _ in range(config['num_initial_mix_storage_containers'][mix_type]):
                self.add_mix_container(
                    mix_type,
                    initial_quantity=5000,
                    expiry_date=config['mix_expiry_days']
                )
            # we expect each initial container to correspond to 5000 in initial inventory:
            if self.remaining_mix_inventory[mix_type] != 5000 * config['num_initial_mix_storage_containers'][mix_type]:
                raise RuntimeError("Something went wrong")

    def remove_mix(self, mix_type, amount):
        if mix_type not in [0, 1]:
            raise ValueError("Invalid mix type. Mix type must be either 0 or 1.")
        if amount <= 0:
            raise ValueError("Amount to remove must be positive.")
        if self.remaining_mix_inventory[mix_type] < amount:
            return False
        # if we reach this point, then there is sufficient mix available in the containers to withdraw the needed amount.

        # in total, we want to remove this much mix
        mix_to_remove_remaining = amount
        # iterate over the tank_containers one by one, and remove the mix.
        # If the container is empties, make it available again for filling,
        # by decreasing the number of containers in use
        while mix_to_remove_remaining > 0 and self.mix_storage_container_inventory[mix_type]:
            first_tank = self.mix_storage_container_inventory[mix_type][0]
            if first_tank.quantity_left >= mix_to_remove_remaining:
                first_tank.quantity_left -= mix_to_remove_remaining
                self.remaining_mix_inventory[mix_type] -= mix_to_remove_remaining
                if first_tank.quantity_left == 0:
                    self.mix_storage_container_inventory[mix_type].popleft()
                    self.mix_storage_containers_in_use -= 1
                mix_to_remove_remaining = 0
            else:
                mix_to_remove_remaining -= first_tank.quantity_left
                self.remaining_mix_inventory[mix_type] -= first_tank.quantity_left
                self.mix_storage_container_inventory[mix_type].popleft()
                self.mix_storage_containers_in_use -= 1
        return True

    def add_mix_container(self, mix_type, initial_quantity, expiry_date):
        if mix_type not in [0, 1]:
            raise ValueError("Mix type must be 0 or 1.")
        if initial_quantity > 5000 or initial_quantity <= 0:
            raise ValueError("Initial quantity for a mix container must be in (0,5000].")
        # Create and append a new tank container
        new_container = MixTankContainerInUse(quantity_left=initial_quantity, economic_expiry_date=expiry_date)
        self.mix_storage_container_inventory[mix_type].append(new_container)
        self.remaining_mix_inventory[mix_type] += initial_quantity
        self.mix_storage_containers_in_use += 1

    def add_product_order(self, product_index, quantity, due_date):
        self.open_customer_orders[product_index].append(CustomerOrder(quantity, due_date))

    def add_extraction_order(self, herb_id, quantity, completion_date):
        self.open_extraction_orders[herb_id].append(HerbExtractOrder(quantity, completion_date))

