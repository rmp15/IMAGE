import os
import glob
from ggplot import *
from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
from data.objects.objects import *
from prog.functions.plotting.plotting_tools import plot_knmi_scenarios_monthly

# this script
# gets a particular dataframe for a particular yearly metric for the time periods
# calculates percentage increase from base period (assumes the first period)
# outputs as a dataframe

# create locations for the files
file_paths = [os.path.join(minas_knmi_climate_output,'minas_brazil', i) for i in stations_brazil]

# for each file in each location, calculate the percentage increase of each column value from the
# value in the first column
def plug_in_metric(metric):
    for i in range(len(file_paths)):
        # create file paths with the desired variable
        print(os.path.join(file_paths[i],'*'))
        for name in glob.glob(os.path.join(file_paths[i], metric + '_yearly_mean_' + '*')):
            file_paths[i] = name

            # calculate and plot mean values
            file_output = os.path.join(minas_knmi_climate_output, 'minas_brazil', stations_brazil[i])
            knmi_scenarios_scale_factors_yearly(metric, file_paths[i], file_output, years_past, years_future_1, years_future_2)

# run function
metric_temp = 'r1mm'
plug_in_metric(metric_temp)

