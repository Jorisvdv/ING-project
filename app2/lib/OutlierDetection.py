"""
This file contains a set of functions to calculate outliers on a given 1-D numerical array.

@author Antonio Samaniego
@file   OutlierDetection.py
@scope  public
"""

# third party dependencies
import os
import csv
import math
import numpy as np

# Set location of log folder relative to this script
OUT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logs/outliers'))


def moving_average(t, n=3):
    """
    Function to calculate moving/rolling average of a 1-dimensional array of numbers.

    Parameters
    ----------
        t: 1-dimensional array of numbers (e.g. int, float).
        n: Window length for moving average step calculation (e.g. n=5 means
            every average step is calculated with 5 elements). Default: n=3
    Returns
    -------
        Moving average of t
    """
    ret = np.cumsum(t)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

# Detects outliers based on std and moving average, and saves them on a .csv file


def detect_outliers(t, n=3, s=2, filename='outliers.csv'):
    """
    Function to detect outliers based on whether an element is s standard deviations (std)
    away from the corresponding rolling mean value. Results are both returned in a dict and
    saved into an output .csv file.

    Parameters
    ----------
        t: 1-dimensional array of numbers (e.g. int, float).
        n: Window length for moving average step calculation (e.g. n=5 means
            every average step is calculated with 5 elements). Default: n=3
        s: Number of std away from the rolling mean from which a value is
           considered to be an outlier. Default s=2
        filename: Output .csv filename. Default filename='outliers.csv'

    Returns
    -------
        outliers: dict containing {'timestamp': outlier_value}
    """
    if n == 1:
        print('Time series length is 1 (no possible outliers). No output file created.')
        return None

    mov_avg_t = moving_average(t, n=n)      # Moving/rolling average
    std_dev = np.std(t[0:len(mov_avg_t-1)])  # Std

    outliers = {}
    for idx, v in enumerate(t[1:]):
        # More than s stds from the corresponding set/window's rolling mean
        if v - (s * std_dev) > mov_avg_t[math.floor(idx % n)]:
            outliers[idx] = v

    # Save on output .csv file
    with open(OUT_DIR+filename, mode='w') as outlier_file:
        outlier_writer = csv.writer(outlier_file, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
        outlier_writer.writerow(['idx', 'value'])
        for k, v in outliers.items():
            outlier_writer.writerow([k, v])

    return outliers
