import os
import glob
from ggplot import *
from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
from data.objects.objects import *
from prog.functions.plotting.plotting_tools import plot_knmi_scenarios_monthly_over_time

# this script
# generates statistics for a time period for yearly data from a rain gauge

# create locations for the files
file_paths = [os.path.join(minas_real_climate_data, i + 'CHUVA.txt') for i in stations_brazil]

# loop over each
for j in range(len(file_paths)):

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

    # remove duplicates
    data = data.drop_duplicates(subset=['month', 'year'], keep='first')

    # test to only include months from chosen years with not many missing values
    data = data[data['year'].isin(years_past)]

    # calculate total value of variable and then divide by number of years
    num_years = years_past[-1] - years_past[0] + 1
    data['new_num_days_pr'] = data.iloc[:, 4:35][data.iloc[:, 4:35] >= pr_threshold].count(axis=1)
    total_metric = data[str('new_num_days_' + metric)].sum() / num_years
    print(round(total_metric, 2))

    print(data.head())
