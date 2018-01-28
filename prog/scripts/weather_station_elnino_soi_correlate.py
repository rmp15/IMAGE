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

# this file will correlate various averages for each weather station
# with El Nino and SOI variables

# output file for r values for each station
df_month_master = pd.DataFrame(columns=r_names_month)
df_season_master = pd.DataFrame(columns=r_names_season)
df_year_master = pd.DataFrame(columns=r_names_year)
for i in elninos:

    df_submaster = pd.DataFrame(columns=r_names_month)
    df_season_submaster = pd.DataFrame(columns=r_names_season)

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

        # remove duplicates
        data = data.drop_duplicates(subset=['month', 'year'], keep='first')

        #######################################################################################################

        # load the chosen el nino/soi measure
        metric = pd.read_csv(os.path.join(knmi_elnino, 'iersst_' + i + '.txt'),
                             skiprows=76, header=None, sep='\s+')

        # rename column
        metric.columns = ['date', 'value']

        # month and year generate
        metric['year'] = round(metric['date'].apply(np.floor))
        metric['month'] = 1 + round(12 * (metric['date'] - metric['year']))

        # attach season marker
        metric = pd.merge(metric, df_season, left_on=['month'], right_on=['month'])

        #######################################################################################################

        # merge data and el nino values
        dat_merged = pd.merge(data, metric, left_on=['year', 'month'], right_on=['year', 'month'])

        # sort by month and year column
        dat_merged.sort_values(['year', 'month'], ascending=[True, True], inplace=True)

        #######################################################################################################

        # seasonal analysis

        print(j + ' ' + ' ' + i + ' seasonal analysis of el nino metrics')

        df = pd.DataFrame(columns=r_names_season)

        # calculate correlation value per season
        for season in seasons:

            print('season :' + season)

            # isolate season
            dat_seasons = dat_merged[dat_merged.season == season]
            metric_isolate = metric[metric.season == season]

            # filter missing data depending on length of month
            for month in month_numbers:
                if month in day_months_long:
                    dat_seasons = dat_seasons.dropna(axis=0, thresh=threshold_drop_days)
                if month in day_months_medium:
                    dat_seasons = dat_seasons.dropna(axis=0, thresh=threshold_drop_days + 1)
                if month in day_months_short:
                    dat_seasons = dat_seasons.dropna(axis=0, thresh=threshold_drop_days + 3)

            # sum rainfall per year per season and count the number of months in count
            dat_grouped = dat_seasons.groupby(['season', 'year'])
            dat_grouped = dat_grouped['total_pr'].agg(['mean', 'count'])
            dat_grouped.columns = ['pr_mean', 'month_count']

            # drop if number of months is fewer than threshold
            dat_grouped = dat_grouped[dat_grouped['month_count'] > threshold_drop_months]

            # average el nino per year per season
            dat_season_elnino = metric_isolate.groupby(['season', 'year'])
            dat_season_elnino = dat_season_elnino['value'].agg(['mean'])
            dat_season_elnino.columns = ['metric_mean']

            # merge data and el nino values
            dat_grouped = pd.merge(dat_grouped, dat_season_elnino, left_index=True, right_index=True)

            # calculate correlation
            slope, intercept, r_value, p_value, std_err = linregress(dat_grouped['pr_mean'], dat_grouped['metric_mean'])
            #print(i, j, season, r_value, p_value)

            # record number of seasons actually used for regression
            n = dat_grouped.shape[0]

            # create data frame to append to main list
            df_append_season = pd.DataFrame([[j, i, season, n, r_value, p_value]], columns=r_names_season)
            df_append_season['sig'] = np.where(df_append_season['p_value'] <= 0.05, 1, 0)
            df = df.append(df_append_season)

        df_season_submaster = df_season_submaster.append(df)

            #######################################################################################################

        # yearly analysis by month
        # WORKING HERE
        # WORKING HERE

            ######################################################################################################

        # monthly analysis

        print(j + ' ' + ' ' + i + ' monthly analysis of el nino metrics')


        df = pd.DataFrame(columns=r_names_month)
        for k in month_numbers:

            print('month :' + str(k))

            # isolate month
            temp_df = dat_merged[dat_merged.month == k]

            # filter depending on length of month
            if k in day_months_long:
                temp_df = temp_df.dropna(axis=0, thresh=threshold_drop_days)
            if k in day_months_medium:
                temp_df = temp_df.dropna(axis=0, thresh=threshold_drop_days + 1)
            if k in day_months_short:
                temp_df = temp_df.dropna(axis=0, thresh=threshold_drop_days + 3)

            # total precipitation record must be complete
            temp_df = temp_df[np.isfinite(temp_df['total_pr'])]

            # record number of months actually used for regression
            n = temp_df.shape[0]

            # calculate correlation
            slope, intercept, r_value_3, p_value, std_err = linregress(temp_df['value'], temp_df['total_pr'])
            #print(i, j, k, r_value_3, p_value)
            df_append = pd.DataFrame([[j, i, k, n, r_value_3, p_value]], columns=r_names_month)
            df_append['sig'] = np.where(df_append['p_value'] <= 0.05, 1, 0)
            df = df.append(df_append)

        df_submaster = df_submaster.append(df)

    df_month_master = df_month_master.append(df_submaster)
    df_season_master = df_season_master.append(df_season_submaster)

######################################################################################################

# save results
print('plotting and saving results')

# create directory to save output
output_directory = os.path.join(minas_knmi_climate_output, 'minas_brazil', 'elnino')
recursive_directory(output_directory)

print(df_month_master.head())
print(df_season_master.head())

# remove soi
df_month_master = df_month_master[df_month_master.elnino_metric != 'soi_a']
df_season_master = df_season_master[df_season_master.elnino_metric != 'soi_a']

# plot the correlation coefficients by for each station by month
df_season_master['season'] = pd.factorize(df_season_master.season)[0]

g = ggplot(df_season_master, aes(x='season', y='r_value', color='station')) + \
    geom_point() + \
    scale_x_continuous(breaks=[0, 1], labels=["wet", "dry"]) + \
    scale_color_manual(guide=False) + \
    facet_wrap('elnino_metric')

h = ggplot(df_season_master, aes(x='season', y='r_value', color='station', alpha='sig')) + \
    geom_point() + \
    ggtitle('p<0.05') + \
    scale_x_continuous(breaks=[0, 1], labels=["wet", "dry"]) + \
    facet_wrap('elnino_metric')

g.save(filename=os.path.join(output_directory, 'seasonal_values_r_by_station_nino_metric_plot.pdf'))
h.save(filename=os.path.join(output_directory, 'seasonal_values_r_by_station_nino_metric_sig_plot.pdf'))

# plot the correlation coefficients by for each station by month
g = ggplot(df_month_master, aes(x='month', y='r_value', color='station')) + \
    geom_point() + \
    facet_wrap('elnino_metric')

h = ggplot(df_month_master, aes(x='month', y='r_value', color='station', alpha='sig')) + \
    geom_point() + \
    ggtitle('p<0.05') + \
    facet_wrap('elnino_metric')

g.save(filename=os.path.join(output_directory, 'monthly_values_r_by_station_nino_metric_plot.pdf'))
h.save(filename=os.path.join(output_directory, 'monthly_values_r_by_station_nino_metric_sig_plot.pdf'))

# save correlation coefficients for all values
df_month_master.sort_values(['r_value'], ascending=[True], inplace=True)
df_season_master.sort_values(['r_value'], ascending=[True], inplace=True)
output_string_monthly = os.path.join(output_directory, 'monthly_elnino_r_squared_values.csv')
output_string_seasonal = os.path.join(output_directory, 'seasonal_elnino_r_squared_values.csv')
df_month_master.to_csv(output_string_monthly)
df_season_master.to_csv(output_string_seasonal)
