from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
import os
import glob
from ggplot import *

from data.objects.objects import *

# create locations for the files
file_paths = [os.path.join(minas_knmi_climate_data, i) for i in stations_brazil]

for metric in metrics:

    # create file paths with the desired variable
    for i in range(len(file_paths)):
        for name in glob.glob(os.path.join(file_paths[i], 'tsicmip5_' + metric + '_*')):
            file_paths[i] = name

    # calculate and plot mean values
    for i in range(len(file_paths)):
        file_output = os.path.join(minas_knmi_climate_output, 'minas_brazil', stations_brazil[i])
        plot_knmi_scenarios(metric, file_paths[i], file_output, years_past, years_future_1, years_future_2)


