import os
import glob
from ggplot import *
from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
from data.objects.objects import *
from prog.functions.plotting.plotting_tools import plot_knmi_scenarios_monthly_over_time
import pandas as pd
import numpy as np

# this file will create monthly averages over a normal period (dependent on the data completeness
# get file paths for text files with weather data
file_paths = [os.path.join(minas_real_climate_data, 'InmetData_' + i + '_DailyDatabase.txt')
              for i in weather_stations_brazil]

# which metric
metric = 'tas'

# NEED TO FIX LOOP BELOW AS WELL AS METHOD FOR DOING FOR DIFFERENT CLIMATE SCENARIO YEARS
j = 0

# do for each of the files paths
# for i in range(len(file_paths)):

# load files and perform analysis of average rainfall
data = pd.read_csv(file_paths[j], delimiter=';', skiprows=16, decimal=",")

# only take the data which is relevant
data = data.iloc[:, weather_station_chosen_gauges]

# rename columns
data.columns = weather_station_names

# split the data column into months and years
data['month'] = pd.to_numeric(data['date'].str.split('/').str[1])
data['year'] = pd.to_numeric(data['date'].str.split('/').str[2])

# sort by month and year column
data.sort_values(['year', 'month'], ascending=[True, True], inplace=True)

# load the absolute differences for each month from the knmi climate data (is it ok that it's from other stations?)
file_paths = [os.path.join(minas_knmi_climate_output, 'minas_brazil', i) for i in stations_brazil]

# only use one of the rain gauge station temp data (for now?)
file_path = os.path.join(file_paths[0], metric + '_mean_abs_diff_' +
        str(years_past[0]) + str(years_past[-1]) + '_' +
        str(years_future_1[0]) + str(years_future_1[-1]) + '_' +
        str(years_future_2[0]) + str(years_future_2[-1]) +
        '.csv')

print(file_path)

# load and apply percentage increase
file_output = os.path.join(minas_knmi_climate_output, 'minas_brazil', weather_stations_brazil[j])

# create strings to find the column names
year_string_1 = str(years_future_1[0]) + str(years_future_1[-1]) + '_to_' + \
                str(years_past[0]) + str(years_past[-1]) + '_diff'
year_string_2 = str(years_future_2[0]) + str(years_future_2[-1]) + '_to_' + \
                str(years_past[0]) + str(years_past[-1]) + '_diff'
year_strings = [year_string_1, year_string_2]

# apply scale factors to data's monthly values
for string in year_strings:
    knmi_scenarios_apply_absolute_change_yearly(metric, data, file_paths[j], file_output, string)



