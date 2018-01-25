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

# this file will correlate monthly averages for each weather station
# with KNMI model values

# output file for plot for each station
#for j in stations_brazil:
j=stations_brazil[0]

# get file paths for text files with weather data and climate data
file_path = os.path.join(minas_real_climate_data, j + 'CHUVA.txt')
file_path_pr = os.path.join(minas_knmi_climate_data, j,
                            'tsicmip5_pr_Amon_modmean_rcp85_-43.730364E_-18.415389N_n_su_+++.txt')

# load files and perform analysis of average rainfall
data_real = pd.read_csv(file_path, delimiter=';', skiprows=14, decimal=",")

# load precipitation knmi data
data_knmi = read_knmi_txt(file_path_pr, skiprows=4, columns=header_knmi_raw)

# only take the data which is relevant
data_real = data_real.iloc[:, col_chosen_gauges]

# rename columns
data_real.columns = col_names_gauges
data_knmi.columns = ['year', ' 1', '2', '3', '4', '5', '6', '7', '8', '9', '12', '11', '12']

# split the data column into months and years
data_real['month'] = pd.to_numeric(data_real['date'].str.split('/').str[1])
data_real['year'] = pd.to_numeric(data_real['date'].str.split('/').str[2])

# remove duplicates
data_real = data_real.drop_duplicates(subset=['month', 'year'], keep='first')

# sort by month and year column
data_real.sort_values(['year', 'month'], ascending=[True, True], inplace=True)

print(data_real.head())
print(data_knmi.head())

#
#     # rename column
#     metric.columns = ['date', 'value']
#
#     # month and year generate
#     metric['year'] = round(metric['date'].apply(np.floor))
#     metric['month'] = 1 + round(12 * (metric['date'] - metric['year']))
#
#     # merge data and el nino values
#     dat_merged = pd.merge(data, metric, left_on=['year', 'month'], right_on=['year', 'month'])
#
#     # calculate correlation value per month
#     df = pd.DataFrame(columns=r_names)
#     for k in month_numbers:
#
#         # isolate month
#         temp_df = dat_merged[dat_merged.month == k]
#
#         # drop months which have certain number of days missing and also the total precipitation
#         day_months_long = [1, 3, 5, 7, 8, 10, 12]
#         day_months_medium = [4, 6, 8, 11]
#         day_months_short = [2]
#
#         # filter depending on length of month
#         if k in day_months_long:
#             temp_df = temp_df.dropna(axis=0, thresh=threshold_drop_days)
#         if k in day_months_medium:
#             temp_df = temp_df.dropna(axis=0, thresh=threshold_drop_days + 1)
#         if k in day_months_short:
#             temp_df = temp_df.dropna(axis=0, thresh=threshold_drop_days + 3)
#
#         # total precipitation record must be complete
#         temp_df = temp_df[np.isfinite(temp_df['total_pr'])]
#
#         # record number of days actually used for regression
#         n = temp_df.shape[0]
#
#         #r_value = temp_df['value'].corr(temp_df['total_pr'],)
#         #r_value_2 = pearsonr(temp_df['value'],temp_df['total_pr'])
#         slope, intercept, r_value_3, p_value, std_err = linregress(temp_df['value'], temp_df['total_pr'])
#         print(i, j, k, r_value_3, p_value)
#         df_append = pd.DataFrame([[j, i, k, n, r_value_3, p_value]], columns=r_names)
#         df_append['sig'] = np.where(df_append['p_value'] <= 0.05, 1, 0)
#         print(df_append)
#         df = df.append(df_append)
#
#     # plot by month over the time periods
#     g = ggplot(dat_merged, aes(x='value', y='total_pr')) + \
#         geom_point() + \
#         facet_wrap('month', scales='free') + \
#         theme_bw()
#
#     g.save(filename=os.path.join(minas_knmi_climate_output, 'minas_brazil', j, j + '_' + i + '_plot.pdf'))
#
#
#
# # save correlation coefficients for all values
# output_string = os.path.join(minas_knmi_climate_output,'minas_brazil', 'elnino_r_squared_values.csv')
# df_master.sort_values(['r_value'], ascending=[True], inplace=True)
# df_master.to_csv(output_string)
#
# # plot the correlation coefficients by for each station by month
# g = ggplot(df_master, aes(x='month', y='r_value', color='station')) + \
#     geom_point() + \
#     facet_wrap('elnino_metric')
#     #geom_abline(a=0,b=0, type='dashed')
#
# h = ggplot(df_master, aes(x='month', y='r_value', color='station',alpha='sig')) + \
#     geom_point() + \
#     facet_wrap('elnino_metric') + \
#     ggtitle('p<0.05')
#     #geom_abline(a=0,b=0, type='dashed')
#
# g.save(filename=os.path.join(minas_knmi_climate_output, 'minas_brazil', 'values_r_by_station_nino_metric_plot.pdf'))
# h.save(filename=os.path.join(minas_knmi_climate_output, 'minas_brazil', 'values_r_by_station_nino_metric_sig_plot.pdf'))