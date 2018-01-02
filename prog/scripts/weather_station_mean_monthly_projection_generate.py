import os
import glob
from ggplot import *
from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
from data.objects.objects import *
from prog.functions.plotting.plotting_tools import plot_knmi_scenarios
import pandas as pd

# this file will create monthly averages over a normal period (dependent on the data completeness

# get file paths for text files with weather data
file_paths = [os.path.join(minas_real_climate_data, i + 'CHUVA.txt') for i in stations_brazil]

# load files and perform analysis of average rainfall
data = pd.read_csv(file_paths[0], delimiter=';', skiprows=14)
print(data.head(5))
#print(data.columns)

# find the

# sort
