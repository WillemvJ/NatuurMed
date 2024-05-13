import pandas as pd
from simulationstatus import DayData

# some basic functionality for processing the excel file. it may be useful to somehow process this, to remove all
# non-working-day days, and somehow deal with demand on those days.


def load_and_process_data(file_path):
    df = pd.read_excel(file_path)
    day_data_list = []
    next_working_day = [None] * len(df)  # Initialize with None

    # Validate day numbering
    expected_day = 1
    for day_number in df['DayNumber']:
        if day_number != expected_day:
            raise ValueError(f"Day numbering error: expected {expected_day}, but got {day_number}")
        expected_day += 1

    # Create DayData objects for each row
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
    file_path = "ProductDemand.xlsx"
    data_list = load_and_process_data(file_path)
    for day_data in data_list[:10]:
        print(day_data)
