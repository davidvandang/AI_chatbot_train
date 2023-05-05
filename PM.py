#!/usr/bin/env python
# coding: utf-8



import numpy as np
import pandas as pd
import glob
import os
from datetime import datetime, time, date

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error



path = 'data'
all_files = glob.glob(os.path.join(path, "*.csv"))

df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)




print(df)


# drop every train which does not have any data in arr_at (recorded actual time of arrival)
df_ar = df.dropna(axis=0, subset=['arr_at'])
print(df_ar)


# Keeping only columns: rid, tpl, pta, ptd, arr_at, dep_at

df_ar = df_ar.drop(columns=['arr_et', 'dep_et', 'wta', 'wtp', 'wtd', 'arr_wet', 'arr_atRemoved', 'pass_et', 'pass_wet', 'pass_atRemoved', 'dep_wet',
                           'dep_atRemoved', 'pass_at', 'cr_code', 'lr_code'])
df_ar.reset_index()
print(df_ar)


df_ar.isnull().sum()


# Convert the columns into datetime
df_ar['pta'] = pd.to_datetime(df_ar['pta'], format='%H:%M')
df_ar['ptd'] = pd.to_datetime(df_ar['ptd'], format='%H:%M')
df_ar['arr_at'] = pd.to_datetime(df_ar['arr_at'], format='%H:%M')
df_ar['dep_at'] = pd.to_datetime(df_ar['dep_at'], format='%H:%M')

print(df_ar.dtypes)
 



# Convert the columns into time
df_ar['pta'] = df_ar['pta'].dt.time
df_ar['ptd'] = df_ar['ptd'].dt.time
df_ar['arr_at'] = df_ar['arr_at'].dt.time
df_ar['dep_at'] = df_ar['dep_at'].dt.time

print(df_ar.dtypes)


# If pta is null this means the train came on time, so replace pta with arr_at
df_ar['pta'].fillna(df_ar['arr_at'], inplace=True)

print(df_ar.isnull().sum())
print(df_ar)




# Convert rid into a str
df_ar['rid'] = df['rid'].astype(str)

# Add date column derived from rid
df_ar['date'] = df_ar['rid'].str[:8]


# The delay time for arrival and depature
def delay_time(actual, planned):
    actual_times = df_ar[actual].apply(lambda x: datetime.combine(date.min, x)if not pd.isnull(x) else x)
    planned_times = df_ar[planned].apply(lambda x: datetime.combine(date.min, x)if not pd.isnull(x) else x)
    delay_time_difference = (actual_times - planned_times).apply(lambda x: x.total_seconds() / 60)
    return delay_time_difference


# Add columns arr_delay and dep_delay
df_ar['arr_delay'] = delay_time('arr_at','pta')
df_ar['dep_delay'] = delay_time('dep_at','ptd')


# Termmination column, which shows if there a null in ptd/dep_at = the train has terminated
df_ar['termination'] = ((df_ar['ptd'].isnull()) | (df_ar['dep_at'].isnull())).astype(int)


# Start column, shows if there is a null in arr_at/pta = the train has started here
#df_ar['start'] = ((df_ar['pta'].isnull()) | (df_ar['arr_at'].isnull())).astype(int)

print(df_ar)


# Make a model for each train station
number_stations = df_ar['tpl'].nunique()
name_stations = df_ar['tpl'].unique()

print("Number of unique stations:", number_stations)
print("Name of unique stations:", name_stations)
counts = df_ar['tpl'].value_counts()
print(counts)


# Convert columns pta, ptd, arr_at, dep_at into int
for col in ['pta', 'ptd', 'arr_at', 'dep_at']:
    df_ar[col+'_int'] = df_ar[col].apply(lambda x: int(x.strftime('%H%M%S')) if pd.notnull(x) else x)

# Encode tpl column
from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
df_ar['tpl_encoded']= label_encoder.fit_transform(df_ar['tpl'])

name_stations = df_ar['tpl'].unique()
print("Name of unique stations:", name_stations)

print(df_ar)


# Random Forest Classifier for arrival 
stationModels = {}

# Get the count of occurrences of each station
station_counts = df_ar['tpl'].value_counts()

# Make a model for each train station with more than 1 mention
name_stations = station_counts[station_counts > 1].index

def train_model():
    for station in name_stations:
        
        station_df = df_ar[df_ar['tpl'] == station]

        # If termination is 1 (true), then use the columns without null
        if (station_df[station_df['termination'] == 1].any):
            X = station_df[['rid', 'tpl_encoded', 'pta_int', 'arr_at_int', 'date', 'termination']]
            
        else:
            X = station_df[['rid', 'tpl_encoded', 'pta_int', 'ptd_int', 'arr_at_int', 'dep_at_int', 'date', 'termination']]
                           
        # Preprocessing data
        y = station_df['arr_delay']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)   

        # Create the model
        clf = RandomForestRegressor()
        clf.fit(X_train, y_train)

        stationModels[station] = clf
        
    return stationModels

# Train the models
stationModels = train_model()

# Evaluate the models
for station, (model, X_train, X_test, y_train, y_test) in stationModels.items():
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    print(f"RMSE for {station}: {np.round(rmse, 2)}")

def prediction_arrival_time_delay(current_station, actual_departure_time, delay_time, destination):
    # Train model
    stationModels = train_model()

    # Find route
    route = df_ar[(df_ar['tpl'] == current_station) & (df_ar['dep_at'] == actual_departure_time)].sort_values(by=['arr_at'])

    # If there are no matching rows for the current station and departure time, return None
    if route.empty:
        return None

    # Current stop is the only row in the route
    current_stop = route.iloc[0]

    # Find the index of the current stop in the original df_ar DataFrame
    current_stop_index = df_ar.index[df_ar['rid'] == current_stop['rid']][0]

    # Select all rows from df_ar starting from current_stop_index
    remaining_stops = df_ar.loc[current_stop_index:]

    # Convert delay_time to timedelta
    delay_time = pd.to_timedelta(delay_time, unit='m')

    predicted_arrival_time = None

    # Iterate through the next stop from current_stop until destination
    for _, stop in remaining_stops.iterrows():
        # arrival time + delay for each stop
        stop['arr_at'] = pd.to_datetime(stop['arr_at']) + delay_time

        # destination reached, break loop
        if stop['tpl'] == destination:
            predicted_arrival_time = stop['arr_at']
            break

    return predicted_arrival_time

current_station = "WOKING"
departure_time = "09:59"  # Example: departure time from Southampton
delay_time = 10  # 10-minute delay
destination = "SOTON"

test_1 = prediction_arrival_time_delay(current_station,departure_time, delay_time, destination)
print (test_1)




