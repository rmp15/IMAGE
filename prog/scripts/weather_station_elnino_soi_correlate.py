import os
import glob
from ggplot import *
from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
from data.objects.objects import *
from prog.functions.plotting.plotting_tools import plot_knmi_scenarios
import pandas as pd
import numpy as np

# this file will correlate monthly averages for each weather station
# with El Nino and SOI variables
# get file paths for text files with weather data
file_paths = [os.path.join(minas_real_climate_data, i + 'CHUVA.txt') for i in stations_brazil]

j = 1

# START OF FUNCTION

# load files and perform analysis of average rainfall
data = pd.read_csv(file_paths[j], delimiter=';', skiprows=14,decimal=",")

# only take the data which is relevant
data = data.iloc[:, col_chosen_gauges]

# rename columns
data.columns = col_names_gauges

# split the data column into months and years
data['month'] = pd.to_numeric(data['date'].str.split('/').str[1])
data['year'] = pd.to_numeric(data['date'].str.split('/').str[2])

# sort by month and year column
data.sort_values(['year', 'month'], ascending=[True, True], inplace=True)

# load the chosen el nino/soi measure and correlate
metric = pd.read_csv('/Users/rmiparks/git/IMAGE/data/knmi/elnino/iersst_nino3.4a.txt',
                    skiprows=76, header=None, sep='\s+')

# rename column
metric.columns = ['date', 'value']

# month and year generate
metric['year'] = round(metric['date'].apply(np.floor))
metric['month'] = 1+round(12*(metric['date']-metric['year']))

# merge data and el nino values
dat_merged = pd.merge(data, metric, left_on=['year', 'month'], right_on=['year', 'month'])

# CALCULATE R^2 value

# plot by month over the time periods
g = ggplot(dat_merged, aes(x='value', y='total_pr')) + \
    geom_point() + \
    facet_wrap('month',scales='free') + \
    theme_bw()

g.save(filename=os.path.join(minas_knmi_climate_output,'minas_brazil',stations_brazil[0],'el_nino_plot.pdf'))

# END OF FUNCTION