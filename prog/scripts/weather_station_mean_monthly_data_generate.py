import os
import glob
from ggplot import *
from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
from data.objects.objects import *
from prog.functions.plotting.plotting_tools import plot_knmi_scenarios

# this file will create monthly averages over a normal period (dependent on the data completeness
# the intention is to then scale these values by the values found in the knmi values
# per month