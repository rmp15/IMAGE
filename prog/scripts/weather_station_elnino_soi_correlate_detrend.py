import os
import glob
from ggplot import *
from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
from data.objects.objects import *
from prog.functions.plotting.plotting_tools import plot_knmi_scenarios_monthly_over_time
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from scipy.stats import linregress

# this file will correlate detrended monthly averages for each weather station
# with El Nino and SOI variables

# output file for r values for each station
df_master = pd.DataFrame(columns=r_names)
for i in elninos:

    df_submaster = pd.DataFrame(columns=r_names)

    for j in stations_brazil:

        # get file paths for text files with weather data
        file_path = os.path.join(minas_real_climate_data, j + 'CHUVA.txt')

        # load files and perform analysis of average rainfall
        data = pd.read_csv(file_path, delimiter=';', skiprows=14, decimal=",")

        # only take the data which is relevant
        data = data.iloc[:, col_chosen_gauges]

        # rename columns
        data.columns = col_names_gauges

        # split the data column into months and years
        data['month'] = pd.to_numeric(data['date'].str.split('/').str[1])
        data['year'] = pd.to_numeric(data['date'].str.split('/').str[2])

        # sort by month and year column
        data.sort_values(['year', 'month'], ascending=[True, True], inplace=True)

        # load the chosen el nino/soi measure and correlate
        metric = pd.read_csv(os.path.join(knmi_elnino, 'iersst_' + i + '.txt'),
                             skiprows=76, header=None, sep='\s+')

        # rename column
        metric.columns = ['date', 'value']

        # month and year generate
        metric['year'] = round(metric['date'].apply(np.floor))
        metric['month'] = 1 + round(12 * (metric['date'] - metric['year']))

        # merge data and el nino values
        dat_merged = pd.merge(data, metric, left_on=['year', 'month'], right_on=['year', 'month'])

        # calculate correlation value per month
        df = pd.DataFrame(columns=r_names)
        for k in month_numbers:

            # filter results for correct month and years
            temp_df = dat_merged[dat_merged.month == k]
            #temp_df = temp_df[dat_merged['year'].isin(years_past)]

            # reset the index and make it a column
            temp_df = temp_df.reset_index()
            temp_df['index'] = temp_df.index

            # detrend the data FIX
            # x = temp_df['index']
            # y = temp_df['total_pr']
            # not_nan_ind = ~np.isnan(dat_merged['total_pr'])
            # m, b, r_val, p_val, std_err = linregress(x[not_nan_ind], y[not_nan_ind])
            # temp_df['total_pr_detrend'] = temp_df['total_pr'] - (m*temp_df['index'] + b)

            #print(temp_df.head())

            r_value = temp_df['value'].corr(temp_df['total_pr'],)
            r_value_2 = pearsonr(temp_df['value'],temp_df['total_pr'])
            print(i, j, k, r_value_2)
            df_append = pd.DataFrame([[j, i, k, r_value]], columns=r_names)
            df = df.append(df_append)

        # plot by month over the time periods
        g = ggplot(dat_merged, aes(x='value', y='total_pr')) + \
            geom_point() + \
            facet_wrap('month', scales='free') + \
            theme_bw()

        g.save(filename=os.path.join(minas_knmi_climate_output, 'minas_brazil', j, j + '_' + i + '_plot.pdf'))

        df_submaster = df_submaster.append(df)

    df_master = df_master.append(df_submaster)

# save correlation coefficients for all values
output_string = os.path.join(minas_knmi_climate_output,'minas_brazil', 'elnino_r_squared_values_detrended.csv')
df_master.sort_values(['r_value'], ascending=[True], inplace=True)
df_master.to_csv(output_string)

# plot the correlation coefficients by for each station by month
g = ggplot(df_master, aes(x='month', y='r_value', color='station')) + \
    geom_point() + \
    facet_wrap('elnino_metric')
    #geom_abline(a=0,b=0, type='dashed')

g.save(filename=os.path.join(minas_knmi_climate_output, 'minas_brazil', 'values_r_by_station_nino_metric_plot.pdf'))

pearsonr