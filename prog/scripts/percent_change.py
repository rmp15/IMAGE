from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
import os
import glob
from ggplot import *

from data.objects.objects import *

# create locations for the files
file_paths = [os.path.join(minas_knmi_climate_data, i) for i in stations_brazil]

# create file paths with the desired variable
# need to generalise the variable instead of just pr
for i in range(len(file_paths)):
    for name in glob.glob(os.path.join(file_paths[i], 'tsicmip5_pr_*')):
        file_paths[i] = name

# calculate and plot mean values
for i in range(len(file_paths)):
    file_output = os.path.join(minas_knmi_climate_output, 'minas_brazil', stations_brazil[0])
    plot_knmi_scenarios(file_paths[0], file_output, years_past, years_future_1, years_future_2)
