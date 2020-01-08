class Seasonality(object):
    """ Seasonality adjust the maximum transaction rate according to a specified .csv
    file containing a scaler for certain time stamps
    requires pandas as pd and numpy as np
    """
    def __init__(self, seasonality_file, envoirment = None):
        self.seasonality_file = seasonality_file
        self.env = envoirment

        # Import seasonality .csv file
        self.seasonality_df = pd.read_csv(self.seasonality_file , sep = ";")

        # Find highest time value in seasonality seasonality_dataframe
        self.max_time_seasonality = max(self.seasonality_df["time"].values)

    def scale(self, timestamp = None):
        """ Return scalar to adjust amount of messages, use timestamp if given,
        otherwise call envoirment to determine current time
        """

        # If no timestamp is given, use Simpy envoirment to get time
        if timestamp is None:
            if self.env is None:
                raise BaseException("No timestamp or envoirment specified")
            timestamp = self.env.now

        # Loop if timestamp is larger than max seasonality time
        timestamp = timestamp % self.max_time_seasonality
        # Find time value closest to timestamp
        closest_time = abs(self.seasonality_df["time"]-timestamp).values.argmin()
        # Return scaler value correspoding to closest_time
        return self.seasonality_df["scaler_value"][closest_time]
