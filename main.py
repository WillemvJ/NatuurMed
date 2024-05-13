from dataloader import load_and_process_data
from settings import config
from simulator import Simulator



if __name__ == "__main__":
    file_path = 'ProductDemand.xlsx'
    day_data_list = load_and_process_data(file_path)
    # config defined in settings.py
    simulator = Simulator(config)
    # this setup ensures that the simulator processes the demand
    # one by one, and does not have access to
    # future demands when processing the current.
    for day in day_data_list:
        simulator.simulate_day(day)
