from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
import os
import glob
from ggplot import *

from data.objects.objects import *

# create locations for the files
from prog.functions.plotting.plotting_tools import plot_knmi_scenarios

file_paths = [os.path.join(minas_knmi_climate_data, i) for i in stations_brazil]

# for each file in each location, create a graph and table of how the variables are changing over the time periods
for i in range(len(file_paths)):
    # create file paths with the desired variable
    for metric in metrics:
        for name in glob.glob(os.path.join(file_paths[i], 'tsicmip5_' + metric + '_*')):
            file_paths[i] = name

        # calculate and plot mean values
        file_output = os.path.join(minas_knmi_climate_output, 'minas_brazil', stations_brazil[i])
        plot_knmi_scenarios(metric, file_paths[i], file_output, years_past, years_future_1, years_future_2)
