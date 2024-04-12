from DataLoader import load_and_process_data
from settings import config
from Simulator import Simulator


file_path = 'natuurmed.xlsx'
day_data_list = load_and_process_data(file_path)
#print first 10 days of data
#for day_data in day_data_list[:10]:
#    print(day_data)

simulator = Simulator(config)

for day in day_data_list:
    simulator.process_day(day)


print(simulator)