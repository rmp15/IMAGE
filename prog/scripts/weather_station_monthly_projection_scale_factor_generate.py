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
file_paths = [os.path.join(minas_real_climate_data, i + 'CHUVA.txt') for i in stations_brazil]

# which metric
metric = 'pr'

# NEED TO FIX LOOP BELOW AS WELL AS METHOD FOR DOING FOR DIFFERENT CLIMATE SCENARIO YEARS
j = 0

# do for each of the files paths
#for i in range(len(file_paths)):

# load files and perform analysis of average rainfall
data = pd.read_csv(file_paths[j], delimiter=';', skiprows=14,decimal=",")

# only take the data which is relevant
data = data.iloc[:, col_chosen_gauges]

# rename columns
data.columns = col_names_gauges

# split the data column into months and years
data['month'] = pd.to_numeric(data['date'].str.split('/').str[1])
data['year'] = pd.to_numeric(data['date'].str.split('/').str[2])

# remove duplicates
data = data.drop_duplicates(subset=['month', 'year'], keep='first')

# sort by month and year column
data.sort_values(['year', 'month'], ascending=[True, True], inplace=True)

# load the scale factors for each month from the knmi climate data
file_paths = [os.path.join(minas_knmi_climate_output, 'minas_brazil', i) for i in stations_brazil]

# for each file in each location, apply the percentage increase of each column value from the
# value in the first column
# create file paths with the desired variable
operator = pd.read_csv(
    os.path.join(minas_knmi_climate_output, 'minas_brazil', stations_brazil[j], metric + '_mean_scale_factors_' +
                 str(years_past[0]) + str(years_past[-1]) + '_' +
                 str(years_future_1[0]) + str(years_future_1[-1]) + '_' +
                 str(years_future_2[0]) + str(years_future_2[-1]) +
                 '.csv')).iloc[:, 6:8]

# load and apply percentage increase
file_output = os.path.join(minas_knmi_climate_output, 'minas_brazil', stations_brazil[j])

# create strings to find the column names
year_string_1 = str(years_future_1[0]) + str(years_future_1[-1]) + '_to_' + \
                str(years_past[0]) + str(years_past[-1]) + '_ratio'
year_string_2 = str(years_future_2[0]) + str(years_future_2[-1]) + '_to_' + \
                str(years_past[0]) + str(years_past[-1]) + '_ratio'
year_strings = [year_string_1,year_string_2]

# apply scale factors to data's monthly values
for string in year_strings:
    knmi_scenarios_apply_scale_factors_monthly(metric, data, operator, file_output, string)
