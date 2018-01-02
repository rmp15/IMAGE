import os
import glob
from ggplot import *
from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
from data.objects.objects import *
from prog.functions.plotting.plotting_tools import plot_knmi_scenarios
import pandas as pd
import numpy as np

# this file will create monthly averages over a normal period (dependent on the data completeness
# get file paths for text files with weather data
file_paths = [os.path.join(minas_real_climate_data, i + 'CHUVA.txt') for i in stations_brazil]

j=3

# do for each of the files paths
#for i in range(len(file_paths)):

# load files and perform analysis of average rainfall
data = pd.read_csv(file_paths[j], delimiter=';', skiprows=14,decimal=",")#,columns = col_names)

# only take the data which is relevant
data = data.iloc[:, col_chosen_gauges]

# rename columns
data.columns = col_names_gauges

# split the data column into months and years
data['month'] = pd.to_numeric(data['date'].str.split('/').str[1])
data['year'] = pd.to_numeric(data['date'].str.split('/').str[2])

# sort by month and year column
data.sort_values(['year', 'month'], ascending=[True, True], inplace=True)

# load the scale factors for each month from the knmi climate data
file_paths = [os.path.join(minas_knmi_climate_output, 'minas_brazil', i) for i in stations_brazil]

# for each file in each location, apply the percentage increase of each column value from the
#value in the first column
# create file paths with the desired variable
for name in glob.glob(os.path.join(file_paths[j], metric + '_mean_scale_factors_' + str(year_past_start) + '_' +
        str(year_future_start_1) + '_' + str(year_future_start_2) + '*')):
    file_paths[j] = name
    # load and apply percentage increase
    file_output = os.path.join(minas_knmi_climate_output, 'minas_brazil', stations_brazil[0])
    year_string = str(str(years_future_2[0]) +'_' + str(years_past[0]))
    knmi_scenarios_apply_scale_factors(metric, data, file_paths[j], file_output, year_string)

