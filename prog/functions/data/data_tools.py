from data.objects.objects import *
import pandas as pd
import numpy as np
from ggplot import *
import os

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

    return df


def data_prep_knmi_scenarios(metric, input, output, years1, years2, years3):
    """takes the dataframes of the different periods and outputs
    them together
    """

    # only take the first 13 columns of the file (year and 12 months)
    # need to fix to loop over the different locations
    data = read_knmi_txt(input)

    # take subset of data for period in the past and periods in the future
    data_past = isolate_years(data, 'Year', years1)
    data_future_1 = isolate_years(data, 'Year', years2)
    data_future_2 = isolate_years(data, 'Year', years3)

    # find mean values of parameter for each month
    df_avg_past = column_mean(data_past, 1, 13)
    df_avg_future_1 = column_mean(data_future_1, 1, 13)
    df_avg_future_2 = column_mean(data_future_2, 1, 13)

    # merge 3 time periods
    result = pd.concat([df_avg_past, df_avg_future_1, df_avg_future_2], axis=1)

    # rename columns (need to fix)
    result.columns = [years1[0], years2[0], years3[0]]

    if output:
        # create recursive directory
        output_path = output
        recursive_directory(output_path)

        result.to_csv(os.path.join(output_path, metric + '_mean_' + str(years1[0]) + '_' + str(years2[0]) + '_' + str(years3[0]) + '.csv'))
    else:
        return result


def recursive_directory(path):
    os.makedirs(path, exist_ok=1)

