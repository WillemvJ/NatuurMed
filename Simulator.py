from SimulationStatus import SimulationStatus, DayData


class Simulator:
    def __init__(self, config):
        self.config = config
        self.status = SimulationStatus(config)

    def compute_setup(self, current_product_id, new_product_id):
        if current_product_id == new_product_id:
            return 0  # No setup needed if the product is the same as what we produced previous day.
        elif self.config['product_type'][current_product_id] == self.config['product_type'][new_product_id]:
            return self.config['filling_line_minor_setup_in_minutes']  # Minor setup if the type is the same
        else:
            return self.config['filling_line_major_setup_in_minutes']  # Major setup if the type is different

    def can_produce(self, filling_line_id, product_id):
        return bool(self.config['capabilities_per_line'][filling_line_id][product_id])

    def get_production_quantities(self):
        # here, some logic is needed to determine what will be produced today on the two machines.
        #let's discuss this later- i.e. ignore for now.
        pass

    def process_day(self, day_data: DayData):
        self.status.day_number = day_data.day_number
        due_date = self.status.day_number + self.config['product_demand_lead-time']
        for index, demand in enumerate(day_data.demands):
            self.status.add_product_order(index, demand, due_date)
