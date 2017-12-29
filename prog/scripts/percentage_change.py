import os
import glob
from ggplot import *
from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
from data.objects.objects import *
from prog.functions.plotting.plotting_tools import plot_knmi_scenarios

# create locations for the files
file_paths = [os.path.join(minas_knmi_climate_data, i) for i in stations_brazil]

# this script
# gets a particular dataframe for a particular metric for the time periods
# calculates percentage increase from base period (assumes the first period)
# outputs as a dataframe

# create locations for the files
file_paths = [os.path.join(minas_knmi_climate_data, i) for i in stations_brazil]

# for each file in each location, calculate the percentage increase of each column from the
# value in the first column

