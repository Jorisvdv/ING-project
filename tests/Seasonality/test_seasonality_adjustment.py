import pytest

import numpy as np
import pandas as pd
import os

from .Seasonality.Seasonality_adjustment import Seasonality

print(os.getcwd())

def test_time_values():

    filename = "/Seasonality/seasonality_values.csv"
    time_value_1 = 150000
    expected_1 = 0.9
    time_value_2 = 20000
    expected_2 = 0.16

    season = Seasonality(filename)

    actual_1 = season.scale(time_value_1)
    assert actual_1 == expected_1 #"Expected {0}, got {1}".format(expected_1,actual_1)

    actual_2 = season.scale(time_value_2)
    assert actual_2 == expected_2 #f"Expected {expected_2}, got {actual_2}"


# # Test values
# # time = input("Enter time in seconds")
# time_value_1 = 150000
# time_value_2 = 20000
# filename = "Seasonality/seasonality_values.csv"
# print(f"""Time: {time_value_1}, seasonality scalar {season.scale(time_value_1)}""")
# print(f"""Time: {time_value_2}, seasonality scalar {season.scale(time_value_2)}""")
#
#
# 601200
