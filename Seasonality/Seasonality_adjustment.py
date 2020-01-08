import numpy as np
import pandas as pd

# time = input("Enter time in seconds")
time_value_1 = 150000
time_value_2 = 20000
import os
print(os.getcwd())

filename = "Seasonality/seasonality_values.csv"
seasonality_df = pd.read_csv(filename, sep = ";")
max_time_seasonality = max(seasonality_df["time"].values)
def seasonality_scalar(seasonality_dataframe, timestamp):
    timestamp = timestamp % max_time_seasonality
    closest_time = abs(seasonality_dataframe["time"]-timestamp).values.argmin()
    return seasonality_dataframe["amount"][closest_time]

print(f"""Time: {time_value_1}, seasonality scalar {seasonality_scalar(seasonality_df, time_value_1)}""")
print(f"""Time: {time_value_2}, seasonality scalar {seasonality_scalar(seasonality_df, time_value_2)}""")
