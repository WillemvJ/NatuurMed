import pandas as pd
from SimulationStatus import DayData
def load_and_process_data(file_path):
    df = pd.read_excel(file_path)
    day_data_list = []

    for index, row in df.iterrows():
        is_workday = pd.isna(row['Remark'])
        demands = [row['CL20'], row['CL50'], row['CL100'], row['AD20'], row['AD50'], row['AD100']]
        day_data = DayData(
            day_number=row['DayNumber'],
            entry_date=row['EntryDate'],
            is_workday=is_workday,
            demands=demands
        )
        day_data_list.append(day_data)
    return day_data_list


if __name__ == "__main__":
    file_path = "natuurmed.xlsx"
    data_list = load_and_process_data(file_path)
    for day_data in data_list[:10]:
        print(day_data)
