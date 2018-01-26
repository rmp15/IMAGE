from data.objects.objects import *
import pandas as pd
import numpy as np
from ggplot import *
import os

def read_knmi_txt(data, skiprows, columns):
    """loads txt file and defines the separator"""

    # how many rows to skip
    if skiprows:
        skiprows = skiprows
    else:
        skiprows=4

    df = pd.read_csv(data, skiprows=skiprows, delimiter='\s+')
    df = df.iloc[:, 0:13]

    # defining the column names
    if columns:
        df.columns = columns
    else:
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

# leap year and wrong dates test functions
def is_leap_and_29Feb(s):
    return (s['year'] % 4 == 0) & \
           ((s['year'] % 100 != 0) | (s['year'] % 400 == 0)) & \
           (s['month'] == 2) & (s['day'] == 29)


def exclude_weird_dates(data):
    # imaginary dates exclude
    data = data[(data['month'] != 2) | (data['day'] != 31)]
    data = data[(data['month'] != 2) | (data['day'] != 30)]
    data = data[(data['month'] != 4) | (data['day'] != 31)]
    data = data[(data['month'] != 6) | (data['day'] != 31)]
    data = data[(data['month'] != 9) | (data['day'] != 31)]
    data = data[(data['month'] != 11) | (data['day'] != 31)]

    # find dates which are legitimate 29th February dates
    mask = is_leap_and_29Feb(data)

    # legitimate 29th February dates
    data_leap = data.loc[mask]

    # take 29th February from main data
    data = data[(data['month'] != 2) | (data['day'] != 29)]

    # reattach legitimate 29th Februarys
    data = data.append(data_leap)

    return data


def encode(input_string):
    count = 1
    prev = ''
    lst = []
    for character in input_string:
        if character != prev:
            if prev:
                entry = (count)
                lst.append(entry)
                #print lst
            count = 1
            prev = character
        else:
            count += 1
    else:
        entry = (count)
        lst.append(entry)
    return max(lst)

def data_prep_knmi_scenarios_monthly(metric, input, output, years1, years2, years3):
    """takes the dataframes of the different periods and outputs
    them together
    """

    # only take the first 13 columns of the file (year and 12 months)
    # need to fix to loop over the different locations
    data = read_knmi_txt(input, skiprows=4, columns=header_knmi_raw)

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

    # rename columns
    result.columns = [str(years1[0]) + '_' + str(years1[-1]),
                      str(years2[0]) + '_' + str(years2[-1]),
                      str(years3[0]) + '_' + str(years3[-1])]

    if output:
        # create recursive directory
        output_path = output
        recursive_directory(output_path)

        result.to_csv(os.path.join(output_path, metric + '_mean_' +
                                   str(years1[0]) + str(years1[-1]) + '_' +
                                   str(years2[0]) + str(years2[-1]) + '_' +
                                   str(years3[0]) + str(years3[-1]) + '.csv'))
    else:
        return result


def data_prep_knmi_scenarios_yearly(metric, input, output, years1, years2, years3):
    """takes the dataframes of the different periods and outputs
    them together
    """

    # only take the first 13 columns of the file (year and 12 months)
    # need to fix to loop over the different locations
    columns = ['year', 'value']
    data = read_knmi_txt(input, skiprows=100, columns=columns)

    # take subset of data for period in the past and periods in the future
    data_past = isolate_years(data, 'year', years1)
    data_future_1 = isolate_years(data, 'year', years2)
    data_future_2 = isolate_years(data, 'year', years3)

    # find mean values of parameter for each month
    df_avg_past = column_mean(data_past, 1, 2)
    df_avg_future_1 = column_mean(data_future_1, 1, 2)
    df_avg_future_2 = column_mean(data_future_2, 1, 2)

    # merge 3 time periods
    result = pd.concat([df_avg_past, df_avg_future_1, df_avg_future_2], axis=1)

    # rename columns (need to fix)
    result.columns = [str(years1[0]) + '_' + str(years1[-1]),
                      str(years2[0]) + '_' + str(years2[-1]),
                      str(years3[0]) + '_' + str(years3[-1])]
    print(result)

    if output:
        # create recursive directory
        output_path = output
        recursive_directory(output_path)

        result.to_csv(os.path.join(output_path, metric + '_yearly_mean_' +
                                   str(years1[0]) + str(years1[-1]) + '_' +
                                   str(years2[0]) + str(years2[-1]) + '_' +
                                   str(years3[0]) + str(years3[-1]) + '.csv'))
    else:
        return result


def knmi_scenarios_scale_factors_monthly(metric, input, output, years1, years2, years3):
    """takes a dataframe and calculates percentage differences of the columns
    """

    # only take the first 13 columns of the file (year and 12 months)
    # need to fix to loop over the different locations
    data = pd.read_csv(input)
    # ratio differences
    data[str(years2[0]) + str(years2[-1]) + '_to_' + str(years1[0]) + str(years1[-1]) + '_ratio'] = \
        data[str(years2[0]) + '_' + str(years2[-1])] / data[str(years1[0]) + '_' + str(years1[-1])]
    data[str(years3[0]) + str(years3[-1]) + '_to_' + str(years1[0]) + str(years1[-1]) + '_ratio'] = \
        data[str(years3[0]) + '_' + str(years3[-1])] / data[str(years1[0]) + '_' + str(years1[-1])]
    # percentage differences
    data[str(years2[0]) + str(years2[-1]) + '_to_' + str(years1[0]) + str(years1[-1]) + '_percdelta'] = \
        round(100*(data[str(years2[0]) + '_' + str(years2[-1])] / data[str(years1[0]) + '_' + str(years1[-1])]) - 100, 1)
    data[str(years3[0]) + str(years3[-1]) + '_to_' + str(years1[0]) + str(years1[-1]) + '_percdelta'] = \
        round(100*(data[str(years3[0]) + '_' + str(years3[-1])] / data[str(years1[0]) + '_' + str(years1[-1])]) - 100, 1)

    print(data)

    if output:
        # create recursive directory
        output_path = output
        recursive_directory(output_path)

        data.to_csv(os.path.join(output_path, metric + '_mean_scale_factors_' +
                                 str(years1[0]) + str(years1[-1]) + '_' +
                                 str(years2[0]) + str(years2[-1]) + '_' +
                                 str(years3[0]) + str(years3[-1]) + '.csv'))
    else:
        return data


def knmi_scenarios_scale_factors_yearly(metric, input, output, years1, years2, years3):
    """takes a dataframe and calculates percentage differences of the columns
    """

    # only take the first 2 columns (year and value
    data = pd.read_csv(input)
    # ratio differences
    data[str(years2[0]) + str(years2[-1]) + '_to_' + str(years1[0]) + str(years1[-1]) + '_ratio'] = \
        data[str(years2[0]) + '_' + str(years2[-1])] / data[str(years1[0]) + '_' + str(years1[-1])]
    data[str(years3[0]) + str(years3[-1]) + '_to_' + str(years1[0]) + str(years1[-1]) + '_ratio'] = \
        data[str(years3[0]) + '_' + str(years3[-1])] / data[str(years1[0]) + '_' + str(years1[-1])]
    # percentage differences
    data[str(years2[0]) + str(years2[-1]) + '_to_' + str(years1[0]) + str(years1[-1]) + '_percdelta'] = \
        round(100*(data[str(years2[0]) + '_' + str(years2[-1])] / data[str(years1[0]) + '_' + str(years1[-1])]) - 100, 1)
    data[str(years3[0]) + str(years3[-1]) + '_to_' + str(years1[0]) + str(years1[-1]) + '_percdelta'] = \
        round(100*(data[str(years3[0]) + '_' + str(years3[-1])] / data[str(years1[0]) + '_' + str(years1[-1])]) - 100, 1)

    print(data)

    if output:
        # create recursive directory
        output_path = output
        recursive_directory(output_path)

        data.to_csv(os.path.join(output_path, metric + '_yearly_mean_scale_factors_' +
                                            str(years1[0]) + str(years1[-1]) + '_' +
                                            str(years2[0]) + str(years2[-1]) + '_' +
                                            str(years3[0]) + str(years3[-1]) + '.csv'))
    else:
        return data


def knmi_scenarios_absolute_change_monthly(metric, input, output, years1, years2, years3):
    """takes a dataframe and calculates absolute change of the columns
    """

    # only take the first 13 columns of the file (year and 12 months)
    # need to fix to loop over the different locations
    data = pd.read_csv(input)
    # ratio differences
    data[str(years2[0]) + str(years2[-1]) + '_to_' + str(years1[0]) + str(years1[-1]) + '_diff'] = \
        data[str(years2[0]) + '_' + str(years2[-1])] - data[str(years1[0]) + '_' + str(years1[-1])]
    data[str(years3[0]) + str(years3[-1]) + '_to_' + str(years1[0]) + str(years1[-1]) + '_diff'] = \
        data[str(years3[0]) + '_' + str(years3[-1])] - data[str(years1[0]) + '_' + str(years1[-1])]
    # percentage differences

    print(data)

    if output:
        # create recursive directory
        output_path = output
        recursive_directory(output_path)

        data.to_csv(os.path.join(output_path, metric + '_mean_abs_diff_' +
                                 str(years1[0]) + str(years1[-1]) + '_' +
                                 str(years2[0]) + str(years2[-1]) + '_' +
                                 str(years3[0]) + str(years3[-1]) + '.csv'))
    else:
        return data


def recursive_directory(path):
    """creates a file directory allowing for recursive creation
    """
    os.makedirs(path, exist_ok=1)


def knmi_scenarios_apply_scale_factors_monthly(metric, subject, operator, output, future_years, threshold):
    """takes a dataframe and applies percentage difference of climate scenarios
    """

    subject = subject
    subject['num_days_pr'] = subject.iloc[:, 4:35][subject.iloc[:, 4:35] > threshold].count(axis=1)

    # add month number to operator
    operator['month'] = operator.index + 1

    # merge subject and operator and re-sort
    data_merged = pd.merge(subject, operator)
    data_merged.sort_values(['year', 'month'], ascending=[True, True], inplace=True)
    data_merged = data_merged.reset_index(drop=True)

    # apply scale factor to monthly values from desired scale factor
    data_merged.iloc[:, 4:35] = data_merged.iloc[:, 4:35].multiply(data_merged[future_years], axis='index')

    # recalculate statistics based on new values
    # total number of wet days
    data_merged['total_pr_scenario'] = data_merged.iloc[:, 4:35].sum(axis=1)
    data_merged['num_days_pr_scenario'] = data_merged.iloc[:, 4:35][data_merged.iloc[:, 4:35] > threshold].count(axis=1)

    # output data
    # create recursive directory
    output_path = output
    recursive_directory(output_path)
    # output to directory
    data_merged.to_csv(os.path.join(output_path, metric + '_real_values_scaled_' + future_years + '.csv'))

    # make output of function an object
    return data_merged


def knmi_scenarios_apply_absolute_change_monthly(metric, subject, operator, output, future_years):
    """takes a dataframe and applies percentage difference of climate scenarios
    """

    subject = subject
    subject['num_days_pr'] = subject.iloc[:, 4:35][subject.iloc[:, 4:35] > pr_threshold].count(axis=1)
    operator = pd.read_csv(operator).iloc[:, 6:8]

    # add month number to operator
    operator['month'] = operator.index + 1

    # merge subject and operator and re-sort
    data_merged = pd.merge(subject, operator)
    data_merged.sort_values(['year', 'month'], ascending=[True, True], inplace=True)
    data_merged = data_merged.reset_index(drop=True)

    # apply scale factor to monthly values from desired scale factor
    data_merged.iloc[:, 4:35] = data_merged.iloc[:, 4:35].multiply(data_merged[future_years], axis='index')

    # recalculate statistics based on new values
    # total number of wet days
    data_merged['total_pr_scenario'] = data_merged.iloc[:, 4:35].sum(axis=1)

    print(data_merged.head())

    data_merged['num_days_pr_scenario'] = data_merged.iloc[:, 4:35][data_merged.iloc[:, 4:35] > pr_threshold].count(axis=1)

    # output data
    if output:
        # create recursive directory
        output_path = output
        recursive_directory(output_path)
        # output to directory
        data_merged.to_csv(os.path.join(output_path, metric + '_real_values_scaled_' + future_years + '.csv'))
    else:
        return data_merged


def knmi_scenarios_apply_absolute_change_yearly(metric, subject, operator, output, future_years):
    """takes a dataframe and applies percentage difference of climate scenarios
    """
    # load subject
    subject = subject

    # load operator
    operator = pd.read_csv(operator).iloc[:, (6, 7)]

    # add month number to operator
    operator['month'] = operator.index + 1

    # merge subject and operator and re-sort
    data_merged = pd.merge(subject, operator)

    data_merged.sort_values(['year', 'month'], ascending=[True, True], inplace=True)
    data_merged = data_merged.reset_index(drop=True)

    for column in range(4, 5+1):

        # make sure columns are numeric
        data_merged.iloc[:, column] = pd.to_numeric(data_merged.iloc[:, column])

        # apply absolute difference to monthly values from desired scale factor
        data_merged[data_merged.columns.values[column] + future_years] = \
            data_merged.iloc[:, column] + data_merged[future_years]

    # output data
    if output:
        # create recursive directory
        output_path = output
        recursive_directory(output_path)
        # output to directory
        data_merged.to_csv(os.path.join(output_path, metric + '_real_values_abs_diff_' + future_years + '.csv'))
    else:
        return data_merged


def knmi_scenarios_apply_scale_factors_yearly(metric, subject, operator, output):
    """takes a dataframe and applies percentage difference of climate scenarios
    """

    subject = subject
    subject.columns = ['num_days_pr']

    operator = pd.read_csv(operator)

    print(operator)

    # fix this to automate names!
    subject['num_days_pr_2030'] = subject['num_days_pr'] * pd.to_numeric(operator.iloc[0, 5])
    subject['num_days_pr_2040'] = subject['num_days_pr'] * pd.to_numeric(operator.iloc[0, 6])

    # output data
    if output:
        # create recursive directory
        output_path = output
        recursive_directory(output_path)
        # output to directory
        subject.to_csv(os.path.join(output_path, metric + '_real_values_yearly_scaled_to_2030_2040.csv'))
    else:
        return subject


