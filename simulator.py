from simulationstatus import SimulationStatus, DayData
from dataloader import load_and_process_data
from settings import configuration
from plotting_utils import visualize_order_deltas

class Simulator:
    def __init__(self, config):
        self.config = config
        self.status = SimulationStatus(config)

    def compute_setup(self, current_product_id, new_product_id):
        if current_product_id == new_product_id:
            return 0  # No setup needed if the product is the same as what we produced previous day.
        elif self.config['product_mix_type'][current_product_id] == self.config['product_mix_type'][new_product_id]:
            return self.config['filling_line_minor_setup_in_minutes']  # Minor setup if the product_type is the same
        else:
            return self.config['filling_line_major_setup_in_minutes']  # Major setup if the type is different

    def can_produce(self, filling_line_id, product_id):
        return bool(self.config['capabilities_per_line'][filling_line_id][product_id])

    def produce_at_filling_line(self):
        # Basic heuristic - assign CL20, CL50, CL100 orders to filling line 0, and AD orders to filling line 1.
        # rotate between these order types.
        # if raw material is not available, continue to other products if their material is available,
        # or pass to next day
        # [CL20,Cl50,CL100],[AD20,AD50,AD100]
        order_types = [[0, 1, 2], [3, 4, 5]]
        for filling_line in range(2):
            # the list of products through which we rotate for the current filling line:
            rotation_for_line = order_types[filling_line]
            current_product = self.status.current_product_per_filling_line[filling_line]
            # time remaining for this filling line for this day is 8 * 60 minutes, minus any time needed to complete
            # unfinished tasks from previous day:
            time_remaining = 8 * 60 - self.status.utilized_time_per_filling_line_from_previous_day[filling_line]
            product_types_produced = 0
            # we want to consider production for each product in the cycle at most once, hence the second condition
            # if time is up, we stop early, hence first condition
            while time_remaining > 0 and product_types_produced < len(rotation_for_line):
                bottle_type = self.config['product_bottle_type'][current_product]
                production_per_hour = self.config['production_volumes_per_line'][filling_line][bottle_type]
                open_orders = self.status.open_customer_orders[current_product]
                while open_orders and time_remaining > 0:
                    # type 0 - CL or 1 - AD
                    mix_type = self.config['product_mix_type'][current_product]
                    # since we don't place any orders for mix, the mix will quickly deplete. to avoid this
                    # for now we will not consume any mix while producing filled products.
                    # however, to consume mix, commenting out the following lines should do the trick.
                    # volume per product in ml * order (in thousands)  = amount of mix in kg/l
                    # mix_amount_required_in_liter = self.config['product_volume'][current_product] * open_orders[0].quantity
                    # if mix_amount_required_in_liter > self.status.remaining_mix_inventory[mix_type]:
                        # we cannot produce this product, because not enough of the right mix is available
                        # move to next product.
                    #    break
                    # self.status.remove_mix(mix_type,mix_amount_required_in_liter)
                    time_remaining -= open_orders[0].quantity * 1000 / production_per_hour
                    completed_order = open_orders.popleft()
                    if time_remaining > 0:
                        completed_order.delivery_date = self.status.day_number
                    else:
                        # this happens if we don't have time for finishing this order today - it will be completed next
                        # day:
                        completed_order.delivery_date = self.status.day_number + 1
                    # so this order is completed (either today or tomorrow), so we append it as delivered:
                    self.status.closed_customer_orders[current_product].append(completed_order)
                product_types_produced += 1
                if time_remaining > 0:
                    # so we managed to complete all open orders for this product type, and
                    # will rotate to the next product:
                    next_index = (rotation_for_line.index(current_product) + 1) % len(rotation_for_line)
                    next_product = rotation_for_line[next_index]
                    time_remaining -= self.compute_setup(current_product, next_product)
                    self.status.current_product_per_filling_line[filling_line] = next_product
                    current_product = next_product
                if time_remaining < 0:
                    # so suppose we have <0 time remaining. That means we have used more time than is available.
                    # that means some tasks remain for the next day, and they should be subtracted from available
                    # processing time for next day.
                    self.status.utilized_time_per_filling_line_from_previous_day[filling_line] = - time_remaining



    def add_demand_orders(self, day_demand_data: DayData):
        # compute leadtime, assuming only working days are included in the data (need to work on this)
        due_date = self.status.day_number + self.config['product_demand_lead-time']
        for index, demand in enumerate(day_demand_data.demands):
            if demand > 0:
                self.status.add_product_order(index, demand, self.status.day_number, due_date)
            # print(demand)

    def close_overdue_orders(self):
        current_day = self.status.day_number
        overdue_threshold = 20  # Orders overdue by more than 10 days are removed

        # Iterate over all products in the open customer orders
        for product_id, order_deque in enumerate(self.status.open_customer_orders):
            # Check if there are orders and the oldest order is overdue
            while order_deque and (current_day - order_deque[0].due_date > overdue_threshold):
                overdue_order = order_deque.popleft()  # Remove the overdue order from the deque
                overdue_order.delivery_date = None  # Set delivery date to None to indicate cancellation
                # Append the overdue order to the closed customer orders
                self.status.closed_customer_orders[product_id].append(overdue_order)

    def simulate_day(self, day_demand_data: DayData):
        self.status.day_number = day_demand_data.day_number
        self.add_demand_orders(day_demand_data)
        self.close_overdue_orders()
        if day_demand_data.is_workday:
            self.produce_at_filling_line()


if __name__ == "__main__":
    file_path = 'ProductDemandComplete.xlsx'
    day_data_list = load_and_process_data(file_path)
    # config defined in settings.py
    simulator = Simulator(configuration)
    # this setup ensures that the simulator processes the demand
    # one by one, and does not have access to
    # future demands when processing the current.
    for day in day_data_list[:]:
        simulator.simulate_day(day)
    # an example visualization.
    # NOTE - overdue orders are set at a delta of 100.
    # NOTE - currently, no mix is being produced, and hence a lot of orders are never delivered
    visualize_order_deltas(simulator.status.closed_customer_orders, configuration)
