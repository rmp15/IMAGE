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

# only take the first 13 columns of the file (year and 12 months)
# need to fix to loop over the different locations
data = read_knmi_txt(file_paths[2])

# take subset of data for period in the past and periods in the future
data_past = isolate_years(data, 'Year', years_past)
data_future_1 = isolate_years(data, 'Year', years_future_1)
data_future_2 = isolate_years(data, 'Year', years_future_2)

# find mean values of parameter for each month
df_avg_past = column_mean(data_past, 1, 13)
df_avg_future_1 = column_mean(data_future_1, 1, 13)
df_avg_future_2 = column_mean(data_future_2, 1, 13)

# merge 3 time periods
result = pd.concat([df_avg_past, df_avg_future_1, df_avg_future_2], axis=1)

# rename columns (need to fix)
result.columns = [1, 2, 3]

# reshape data frame for plotting purposes
result = result.unstack().reset_index()

# rename columns (need to fix)
result.columns = ['time', 'month', 'value']

print(result)

# plot by month over the time periods
g = ggplot(result, aes(x='time', y='value', color='month')) +\
    geom_line() +\
    theme_bw()

print(g)