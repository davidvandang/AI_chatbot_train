import numpy as np
import pandas as pd
import glob
import os
from datetime import datetime, time, date

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn import preprocessing

class TrainDelayPredictor:
    def __init__(self, path='data'):
        self.path = path
        self.df = None
        self.number_stations = None
        self.name_stations = None
        self.label_encoder = preprocessing.LabelEncoder()
        self.stationModels = {}

    def load_data(self):
        # Fetch all CSV files and concatenate them into a dataframe
        all_files = glob.glob(os.path.join(self.path, "*.csv"))
        self.df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
        # print(self.df)
    def clean_data(self):
        # Remove rows where 'arr_at' is missing (NaN)
        self.df.dropna(axis=0, subset=['arr_at'], inplace=True)
        # Drop irrelevant columns
        columns_to_drop = ['arr_et', 'dep_et', 'wta', 'wtp', 'wtd', 'arr_wet', 'arr_atRemoved', 'pass_et', 'pass_wet',
                           'pass_atRemoved', 'dep_wet', 'dep_atRemoved', 'pass_at', 'cr_code', 'lr_code']
        self.df.drop(columns=columns_to_drop, inplace=True)
        # Reset index after dropping rows
        self.df.reset_index(drop=True, inplace=True)
        # Convert necessary columns into datetime format
        self.convert_columns_to_datetime()

    def convert_columns_to_datetime(self):
        # Convert to datetime and then extract time only
        for col in ['pta', 'ptd', 'arr_at', 'dep_at']:
            self.df[col] = pd.to_datetime(self.df[col], format='%H:%M').dt.time
        # If 'pta' is missing, consider the train came on time, hence replace 'pta' with 'arr_at'
        self.df['pta'].fillna(self.df['arr_at'], inplace=True)

    def preprocess_data(self):
        # Convert 'rid' into a str
        self.df['rid'] = self.df['rid'].astype(str)
        # Add 'date' column derived from 'rid'
        self.df['date'] = self.df['rid'].str[:8]
        # Add columns 'arr_delay' and 'dep_delay' to store delay times
        self.df['arr_delay'] = self.delay_time('arr_at','pta')
        self.df['dep_delay'] = self.delay_time('dep_at','ptd')
        # Add 'termination' column, which shows if there a null in 'ptd'/'dep_at' = the train has terminated
        self.df['termination'] = ((self.df['ptd'].isnull()) | (self.df['dep_at'].isnull())).astype(int)
        # Count number of unique stations and list their names
        self.number_stations = self.df['tpl'].nunique()
        self.name_stations = self.df['tpl'].unique()
        # Convert time columns to int for model training
        for col in ['pta', 'ptd', 'arr_at', 'dep_at']:
            self.df[col+'_int'] = self.df[col].apply(lambda x: int(x.strftime('%H%M%S')) if pd.notnull(x) else x)
        # Encode 'tpl' column
        self.df['tpl_encoded']= self.label_encoder.fit_transform(self.df['tpl'])

    def delay_time(self, actual, planned):
        # Calculate delay time
        actual_times = self.df[actual].apply(lambda x: datetime.combine(date.min, x)if not pd.isnull(x) else x)
        planned_times = self.df[planned].apply(lambda x: datetime.combine(date.min, x)if not pd.isnull(x) else x)
        delay_time_difference = (actual_times - planned_times).apply(lambda x: x.total_seconds() / 60)
        return delay_time_difference

    def train_model(self):
        # Get the count of occurrences of each station
        station_counts = self.df['tpl'].value_counts()
        # Make a model for each train station with more than 1 mention
        name_stations = station_counts[station_counts > 1].index
        for station in name_stations:
            station_df = self.df[self.df['tpl'] == station]
            if (station_df[station_df['termination'] == 1].any):
                X = station_df[['rid', 'tpl_encoded', 'pta_int', 'arr_at_int', 'date', 'termination']]
            else:
                X = station_df[['rid', 'tpl_encoded', 'pta_int', 'ptd_int', 'arr_at_int', 'dep_at_int', 'date', 'termination']]
            y = station_df['arr_delay']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
            clf = RandomForestRegressor()
            clf.fit(X_train, y_train)
            self.stationModels[station] = (clf, X_train, X_test, y_train, y_test)

    def evaluate_models(self, station):
        model, X_train, X_test, y_train, y_test = self.stationModels[station]
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        print(f"RMSE for {station}: {np.round(rmse, 2)}")

predictor = TrainDelayPredictor()
predictor.load_data()
predictor.clean_data()
predictor.preprocess_data()
predictor.train_model()
predictor.evaluate_models("WOKING")