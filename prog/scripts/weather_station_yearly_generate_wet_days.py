import os
import glob
from ggplot import *
from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
from data.objects.objects import *
from prog.functions.plotting.plotting_tools import plot_knmi_scenarios_monthly_over_time

# this script
# generates statistics for a time period for yearly data from a rain gauge

# which metric
metric = 'pr'

# threshold for dry days
thresholds_chosen = [1.29, 1.55, 1.29, 1.28]

# which years
years_chosen = years_past
years_used = [years for years in years_chosen if years not in years_skip]
num_years = len(years_used)

# create locations for the files
file_paths = [os.path.join(minas_real_climate_data, i + 'CHUVA.txt') for i in stations_brazil]

# loop over each weather station
for j in range(len(file_paths)):

    ######################################################################################################

    # prepare data

    print('weather station: ' + str(stations_brazil[j]))

    # load files and perform analysis of average rainfall
    data = pd.read_csv(file_paths[j], delimiter=';', skiprows=14, decimal=",")

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

    # test to only include chosen years with no gaps from gap analysis
    data = data[data['year'].isin(years_chosen)]
    data = data[-data['year'].isin(years_skip)]

    ######################################################################################################

    # figure out average number of wet days from data

    # calculate total value of variable and then divide by number of years
    data['new_num_days_pr'] = data.iloc[:, 4:35][data.iloc[:, 4:35] >= pr_threshold].count(axis=1)
    total_metric = data[str('new_num_days_' + metric)].sum() / num_years
    print('average number of wet days per year in ' + str(years_chosen[0]) + '-' + str(years_chosen[-1]) +
          ' is ' + str(round(total_metric, 2)))

    #####################################################################################################

    # figure out average number of wet days from scaled data

    print('loading scale factors')

    operator = pd.read_csv(os.path.join(minas_knmi_climate_output, 'minas_brazil', stations_brazil[j], metric +
                                        '_mean_scale_factors_' +
                                        str(years_past[0]) + str(years_past[-1]) + '_' +  # change to general once fixed
                                        str(years_future_1[0]) + str(years_future_1[-1]) + '_' +
                                        str(years_future_2[0]) + str(years_future_2[-1]) +
                                        '.csv')).iloc[:, 6:8]

    print('applying scale factors to data for ' + str(years_chosen[0]) + '-' + str(years_chosen[-1]))

    # load and apply percentage increase
    file_output = os.path.join(minas_knmi_climate_output, 'minas_brazil', stations_brazil[j])

    # create strings to find the column names
    year_string = str(years_future_2[0]) + str(years_future_2[-1]) + '_to_' + \
                    str(years_past[0]) + str(years_past[-1]) + '_ratio'

    # apply scale factors to data's monthly values
    data_scaled = knmi_scenarios_apply_scale_factors_monthly(metric, data, operator, file_output, year_string, thresholds_chosen[j])

    # calculate total value of variable and then divide by number of years
    data_scaled['new_num_days_' + metric] = data_scaled.iloc[:, 4:35][data_scaled.iloc[:, 4:35] >= thresholds_chosen[j]].count(axis=1)
    total_metric_scaled = data_scaled[str('new_num_days_' + metric)].sum() / num_years
    print('average number of wet days per year in ' + str(years_chosen[0]) + '-' + str(years_chosen[-1]) +
          ' scaled by ' + str(years_future_2[0]) + '-' + str(years_future_2[-1]) +
          ' is ' + str(round(total_metric_scaled, 2)))

    #####################################################################################################

    # calculate percentage change in precipitation
    percent_change = round(100*((total_metric_scaled / total_metric)-1),1)
    print(percent_change)

