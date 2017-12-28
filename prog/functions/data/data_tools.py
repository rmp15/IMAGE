from data.objects.objects import *
import pandas as pd
import numpy as np

def read_knmi_txt(data):
    """loads txt file and defines the separator"""

    df = pd.read_csv(data, skiprows=4, delimiter='\s+')
    df = df.iloc[:, 0:13]
    df.columns = header_knmi_raw

    return df


def years_list(start, end):
    """takes a start and end year and makes
    a list of all the years between inclusively
    """

    years = list(range(start, end+1))

    return years


def isolate_years(data, column, period):
    """takes a dataframe and isolates
    by a list of years in a specified column
    """

    df = data[data[column].isin(period)]

    return df


def column_mean(data, col_start, col_end):
    """takes a dataframe and takes the mean
    of each column in the chosen range
    """

    df = pd.DataFrame(np.mean(data.iloc[:, col_start:col_end]))
    df.columns = [metric]

    return df

