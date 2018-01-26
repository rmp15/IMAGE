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
threshold_chosen = 1

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
    data = data.iloc[:, col_chosen_gauges_long_prep]

    # rename columns
    data.columns = col_names_gauges_long_prep

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

    #####################################################################################################

    print('calculating consecutive dry days')

    # figure out average number of consecutive dry days from data

    #print(data.head())

    # reformat data into long format
    data = pd.melt(data.loc[:, data.columns != 'date'], id_vars=['gauge', 'month', 'year'],
                   var_name ='day', value_name='pr')

    # make new year and day column numeric
    data['year'] = pd.to_numeric(data['year'])
    data['day'] = pd.to_numeric(data['day'])

    # drop weird dates
    data = exclude_weird_dates(data)

    # calculate rel for each year and divide by number of years
    data['wet_marker'] = np.where(data['pr'] >=pr_threshold, 0, 1)

    # sort by month and year column
    data.sort_values(['year', 'month', 'day'], ascending=[True, True, True], inplace=True)
    data = data.reset_index()

    # directory for output
    data = data.drop('index', 1)
    output_directory = os.path.join(minas_knmi_climate_output, 'minas_brazil', stations_brazil[j])
    output_string = os.path.join(output_directory, stations_brazil[j] + '_long_form_' + metric + '.csv')
    data.to_csv(output_string, index=False)

    # find number of consecutive dry days per year
    sum_days = 0
    for i in years_used:
        # isolate year
        data_temp = data[data['year'] == i]
        sum_days = sum_days + encode(data_temp['wet_marker'])

    total_metric = sum_days / num_years
    print('average number of dry days is ' + str(total_metric))

    #####################################################################################################

    # figure out average number of consecutive dry days from scaled data

    print('loading scale factors')

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
    data_scaled = knmi_scenarios_apply_scale_factors_monthly(metric, data, operator, file_output, year_string,
                                                             threshold_chosen)

    # get rid of unnecessary columns
    data_scaled = data_scaled.iloc[:, col_chosen_gauges_scaled]

    # reformat data into long format
    data_scaled = pd.melt(data_scaled.loc[:, data_scaled.columns != 'date'], id_vars=['gauge', 'month', 'year'],
                         var_name='day', value_name='pr')

    # make new year and day column numeric
    data_scaled['year'] = pd.to_numeric(data_scaled['year'])
    data_scaled['day'] = pd.to_numeric(data_scaled['day'])

    # drop weird dates
    data_scaled = exclude_weird_dates(data_scaled)

    # calculate rle for each year and divide by number of years
    data_scaled['wet_marker'] = np.where(data_scaled['pr'] >= threshold_chosen , 0, 1)

    # sort by month and year column
    data_scaled.sort_values(['year', 'month', 'day'], ascending=[True, True, True], inplace=True)
    data_scaled = data_scaled.reset_index()
    data_scaled = data_scaled.drop('index', 1)

    # directory for output
    output_directory = os.path.join(minas_knmi_climate_output, 'minas_brazil', stations_brazil[j])
    output_string = os.path.join(output_directory, stations_brazil[j] + '_long_form_scaled_' + metric + '.csv')
    data_scaled.to_csv(output_string, index=False)

    # find number of consecutive dry days per year
    sum_days = 0
    for i in years_used:
        # isolate year
        data_temp_scaled = data_scaled[data_scaled['year'] == i]
        sum_days = sum_days + encode(data_temp_scaled['wet_marker'])

    total_metric_scaled = sum_days / num_years
    print('average number of scaled dry days is ' + str(total_metric_scaled))

    #####################################################################################################

    # calculate percentage change in number of dry days
    percent_change = round(100*((total_metric_scaled / total_metric)-1), 1)
    print(percent_change)

