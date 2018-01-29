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
thresholds_chosen = [2.22, 1.60, 2.22, 2.14]

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
    print('current threshold: ' + str(thresholds_chosen[j]))

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

    # figure out average number of consecutive dry days from data #

    # print(data.head())

    # reformat data into long format
    data = pd.melt(data.loc[:, data.columns != 'date'], id_vars=['gauge', 'month', 'year'],
                   var_name='day', value_name='pr')

    # make new year and day column numeric
    data['year'] = pd.to_numeric(data['year'])
    data['day'] = pd.to_numeric(data['day'])

    # drop weird dates
    data = exclude_weird_dates(data)

    # calculate rel for each year and divide by number of years
    data['wet_marker'] = np.where(data['pr'] >= pr_threshold, 0, 1)

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
    print('average number of consecutive dry days is ' + str(round(total_metric,2)))

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
                                                             thresholds_chosen[j])

    # get rid of unnecessary columns
    data_scaled = data_scaled.iloc[:, col_chosen_gauges_scaled]

    # reformat data into long format
    data_melted = pd.melt(data_scaled.loc[:, data_scaled.columns != 'date'], id_vars=['gauge', 'month', 'year'],
                          var_name='day', value_name='pr')

    # make new year and day column numeric
    data_melted['year'] = pd.to_numeric(data_melted['year'])
    data_melted['day'] = pd.to_numeric(data_melted['day'])

    # drop weird dates
    data_melted = exclude_weird_dates(data_melted)

    # calculate rle for each year and divide by number of years
    data_melted['wet_marker'] = np.where(data_melted['pr'] >= thresholds_chosen[j], 0, 1)

    # sort by month and year column
    data_melted.sort_values(['year', 'month', 'day'], ascending=[True, True, True], inplace=True)
    data_melted = data_melted.reset_index()
    data_melted = data_melted.drop('index', 1)

    # directory for output
    output_string = os.path.join(output_directory, stations_brazil[j] + '_long_form_scaled_' + metric + '.csv')
    data_melted.to_csv(output_string, index=False)

    # find number of consecutive dry days per year
    sum_days = 0
    for i in years_used:
        # isolate year
        data_temp_scaled = data_melted[data_melted['year'] == i]
        sum_days = sum_days + encode(data_temp_scaled['wet_marker'])

    total_metric_scaled = sum_days / num_years
    print('average number of scaled dry days is ' + str(round(total_metric_scaled,2)))

    #####################################################################################################

    # calculate percentage change in number of dry days
    percent_change = round(100 * ((total_metric_scaled / total_metric) - 1), 1)
    print('this is a change of ', percent_change, '%')

    #####################################################################################################
    # scale the amount of rain to match 1mm threshold #

    # calculate total precipitation for each month before adjusting and number of wet days
    data_scaled['total_pr_tgt'] = data_scaled.iloc[:, 2:33].sum(axis=1)
    data_scaled['num_days_pr'] = data_scaled.iloc[:, 2:33][data_scaled.iloc[:, 2:33] > 1].count(axis=1)

    # adjust according to difference in threshold and 1mm
    data_scaled.iloc[:, 2:33] = data_scaled.iloc[:, 2:33] - (thresholds_chosen[j] - 1)

    # make all the values below zero into zero
    num = data_scaled._get_numeric_data()
    num[num < 0] = 0

    # calculate new total precipitation
    data_scaled['total_pr_adj'] = data_scaled.iloc[:, 2:33].sum(axis=1)

    # calculate difference in old precipitation and new precipitation
    data_scaled['total_pr_diff'] = data_scaled['total_pr_tgt'] - data_scaled['total_pr_adj']

    # calculate number of days above threshold after adjustment
    data_scaled['num_days_pr_adj'] = data_scaled.iloc[:, 2:33][data_scaled.iloc[:, 2:33] > 1].count(axis=1)

    # apply precipitation difference evenly over the days which are over the threshold (1mm)
    data_scaled['pr_add_per_day'] = data_scaled['total_pr_diff'] / data_scaled['num_days_pr_adj']
    for day in range(1, 32):
        data_scaled[str(day)] = data_scaled.apply(
            lambda row: round(row[str(day)] + row['pr_add_per_day'],2) if row[str(day)] >= 1 else round(row[str(day)],   2),
            axis=1
        )

    # recalculate new total precipitation
    data_scaled['total_pr_readj'] = data_scaled.iloc[:, 2:33].sum(axis=1)

    # recalculate number of days above threshold after adjustment
    data_scaled['num_days_pr_readj'] = data_scaled.iloc[:, 2:33][data_scaled.iloc[:, 2:33] > 1].count(axis=1)

    # calculate difference in old precipitation and new precipitation
    data_scaled['total_pr_diff_again'] = round(data_scaled['total_pr_tgt'] - data_scaled['total_pr_readj'],2)

    # reformat data into long format
    data_melted = pd.melt(data_scaled.iloc[:, (0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,
                                               27,28,29,30,31,32,33,34)], id_vars=['gauge', 'month', 'year'],
                         var_name='day', value_name='pr')

    # make new year and day column numeric
    data_melted['year'] = pd.to_numeric(data_melted['year'])
    data_melted['day'] = pd.to_numeric(data_melted['day'])
    #
    # drop weird dates
    data_melted = exclude_weird_dates(data_melted)

    # calculate rle for each year and divide by number of years
    data_melted['wet_marker'] = np.where(data_melted['pr'] >= thresholds_chosen[j], 0, 1)

    # sort by month and year column
    data_melted.sort_values(['year', 'month', 'day'], ascending=[True, True, True], inplace=True)
    data_melted = data_melted.reset_index()
    data_melted = data_melted.drop('index', 1)

    # print(data_scaled.head())
    # print(data_melted.head())

    # find number of consecutive dry days per year
    sum_days = 0
    for i in years_used:
        # isolate year
        data_temp_scaled = data_melted[data_melted['year'] == i]
        sum_days = sum_days + encode(data_temp_scaled['wet_marker'])

    total_metric_scaled = sum_days / num_years
    print('average number of once-again scaled dry days is ' + str(round(total_metric_scaled, 2)))

    # calculate percentage change in number of dry days
    percent_change = round(100 * ((total_metric_scaled / total_metric) - 1), 1)
    print('this is a change of ', percent_change, '%')
    print('')

    # directory for output
    output_string_wide = os.path.join(output_directory, stations_brazil[j] + '_wide_form_scaled_post_adj_' + metric + '.csv')
    output_string_long = os.path.join(output_directory, stations_brazil[j] + '_long_form_scaled_post_adj_' + metric + '.csv')
    data_scaled.to_csv(output_string_wide, index=False)
    data_melted.to_csv(output_string_long, index=False)

