import numpy as np
import pandas as pd

data_folder_path = 'data'
year_folders = [str(year) for year in range(2017, 2023)]


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
print(all_data.shape)
# print(all_data.head())

# Check for null values
print(all_data.isnull().sum())

