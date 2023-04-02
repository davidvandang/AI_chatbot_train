import datetime

import numpy as np
import pandas as pd

data_folder_path = 'data'
year_folders = [str(year) for year in range(2017, 2023)]

set_column_type = {'rid': int, 'tpl': str, 'pta': datetime.datetime, 'ptd': datetime.datetime, 'wta': datetime.datetime,
                   'wtp': datetime.datetime, 'wtd': datetime.datetime
    , 'arr_et': datetime.datetime, 'arr_wet': datetime.datetime, 'arr_atRemoved': bool, 'pass_et': datetime.datetime,
                   'pass_wet': datetime.datetime, 'pass_atRemoved': bool
    , 'dep_et': datetime.datetime, 'dep_wet': datetime.datetime, 'dep_atRemoved': bool, 'arr_at': datetime.datetime,
                   'pass_at': datetime.datetime, 'dep_at': datetime.datetime
    , 'cr_code': int, 'lr_code': int}

# Create an empty list to store the DataFrames
data_frames = []

# Read all the files in by 'year' and 'month'
for year_folder in year_folders:
    year_folder_path = f"{data_folder_path}/{year_folder}"

    for month in range(1, 13):
        file_path = f"{year_folder_path}/WATRLMN_WEYMTH_OD_a51_{year_folder}_{month}_{month}.csv"

        # Check if the file exists before trying to read it
        try:
            temp_data = pd.read_csv(file_path)
            data_frames.append(temp_data)
        except FileNotFoundError:
            print(f"File not found: {file_path}")

# Put all DataFrames together using np.concatenate and convert the result back to a DataFrame
all_data = pd.DataFrame(np.concatenate(data_frames), columns=temp_data.columns)
all_data.reset_index(drop=True, inplace=True)
all_data = all_data.astype(set_column_type)

all_data.shape
