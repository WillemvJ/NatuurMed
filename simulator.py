from simulationstatus import SimulationStatus, DayData


class Simulator:
    def __init__(self, config):
        self.config = config
        self.status = SimulationStatus(config)

    def compute_setup(self, current_product_id, new_product_id):
        if current_product_id == new_product_id:
            return 0  # No setup needed if the product is the same as what we produced previous day.
        elif self.config['product_type'][current_product_id] == self.config['product_type'][new_product_id]:
            return self.config['filling_line_minor_setup_in_minutes']  # Minor setup if the product_type is the same
        else:
            return self.config['filling_line_major_setup_in_minutes']  # Major setup if the type is different

    def can_produce(self, filling_line_id, product_id):
        return bool(self.config['capabilities_per_line'][filling_line_id][product_id])

    def set_production_quantities(self):
        # Basic heuristic - assign CL20, CL100 orders to filling line 0, and AD orders + CL50 to filling line 1.
        # rotate between these order types.
        #if raw material is not available, continue to other products if their material is available,
        #or pass to next day
        #[CL20,Cl50],[CL50,AD20,AD50,AD100]
        order_types = [[0,2],[1,3,4,5]]
        for filling_line in range(2):
            # the list of products through which we rotate for the current filling line:
            rotation_for_line = order_types[filling_line]
            current_product = self.status.current_product_per_filling_line[filling_line]
            current_index = rotation_for_line.index(current_product)
            # compute the time remaining for production in this period, taking into account any remaining setup time
            # from previous day:
            time_remaining = 8 * 60 - self.status.remaining_setup_time_per_filling_line_from_previous_day[filling_line]
            open_orders = self.status.open_customer_orders[current_product]
            if open_orders:
                #open_orders is a deque
                first_order = open_orders[0]
                first_order.


    def add_demand_orders(self, day_demand_data: DayData):
        # compute leadtime, assuming only working days are included in the data (need to work on this)
        due_date = self.status.day_number + self.config['product_demand_lead-time']
        for index, demand in enumerate(day_demand_data.demands):
            self.status.add_product_order(index, demand, due_date)
    def simulate_day(self, day_demand_data: DayData):
        self.status.day_number = day_demand_data.day_number
        self.add_demand_orders(day_demand_data)
