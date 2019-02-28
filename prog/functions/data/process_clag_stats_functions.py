import scipy.io as io
import os as os
import h5py
from data.file_paths.file_paths import *
import numpy as np
import pandas as pd
import math
from scipy.stats import rankdata

# based on steve's previous code in legacy 'load_mat_var.py'
def load_clag_output(step, num_years, continent, scen_name, start_year, end_year, var):


    if var == 'appt':
        ext = 'mat.npy'
    else:
        ext = 'mat'

    fn_o = var + '/out_' + step + '_y' + str(num_years) + '_' + continent + '_' + str(scen_name) + '_' + str(start_year) + '_' + str(end_year) + '_' + var + '_o.' + ext
    fn_s = var + '/out_' + step + '_y' + str(num_years) + '_' + continent + '_' + str(scen_name) + '_' + str(start_year) + '_' + str(end_year) + '_' + var + '_s.' + ext

    if var in ['appt']:
        o_array = np.load(os.path.join(image_output_local, fn_o))
        s_array = np.load(os.path.join(image_output_local, fn_s))
    else:
        o = h5py.File(os.path.join(image_output_local, fn_o), 'r')
        s = h5py.File(os.path.join(image_output_local, fn_s), 'r')
        o_array = np.array(o[list(o.keys())[0]])
        s_array = np.array(s[list(s.keys())[0]])

    return o_array, s_array


def wind_chill_creator(tas_array, wind_array):

    wind_chill_array = 13.12 + (0.6215 * (tas_array-273.15)) - (11.37*wind_array**0.16) + (0.3965*(tas_array-273.15)*wind_array**0.16)

    return wind_chill_array


def rel_humid_creator(tas_array, huss_array, ps_array):

    # from
    # % e = (ps. * huss). / (0.622 + 0.378 * huss); (steve's code in CORDEX_create_nobc_data.m)
    # % dpt = (log(e / 6.112) * 243.5). / (17.67 - log(e / 6.112)); (steve's code in CORDEX_create_nobc_data.m)
    # RH: = 100*(EXP((17.625*TD)/(243.04+TD))/EXP((17.625*T)/(243.04+T))) (http://andrew.rsmas.miami.edu/bmcnoldy/Humidity.html)

    e_array = (ps_array * huss_array) / (0.622 + 0.378 * huss_array)
    dpt_array = (np.log(e_array / 6.112) * 243.5) / (17.67 - np.log(e_array / 6.112))
    rel_humid_array = 100*(np.exp((17.625*dpt_array)/(243.04+dpt_array))/np.exp((17.625*tas_array)/(243.04+tas_array)))

    return rel_humid_array


def app_temp_creator(tas_array, huss_array, ps_array):

    # from steve's code in CORDEX_create_nobc_data.m
    # %e = (ps.*huss)./(0.622 + 0.378*huss);
    # %dpt = (log(e/6.112) * 243.5) ./ (17.67 - log(e/6.112));
    # %appt = (0.0153*(dpt.*dpt)) +(0.994*tas) - 2.653;
    #
    # %load(tas_file);
    # %tas = v.o - 273.15;
    # %load(huss_file);
    # %huss = save_data;
    # %load(ps_file);
    # %ps = v.o / 100;

    tas_array = tas_array - 273.15
    ps_array = ps_array / 100

    e_array = (ps_array * huss_array) / (0.622 + 0.378 * huss_array)
    dpt_array = (np.log(e_array / 6.112) * 243.5) / (17.67 - np.log(e_array / 6.112))
    appt_array = (0.0153 * (dpt_array * dpt_array)) + (0.994*tas_array) - 2.653

    return appt_array


# this function will process the data into a format monthly_data[month][site]
def monthly_data(var):

    # information for how to create the monthly array
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)

    # create data by site and by month for entire time period of form
    # monthly_data[month][site]
    var_shape = np.ma.shape(var)
    no_sites = var_shape[0]
    no_years = var_shape[1]
    days_in_year = var_shape[2]
    monthly_data = {}
    for i in range(0, 12):
        month_data = np.zeros(((month_start_end_inds[i + 1] - month_start_end_inds[i]) * no_years, no_sites))
        for j in range(0, no_sites):
            month_data[:, j] = np.ndarray.flatten(var[j, :, month_start_end_inds[i]:month_start_end_inds[i + 1]])
        monthly_data[i] = month_data
    return monthly_data, no_years, no_sites


# this function will process the data into a format seasonal_data[season][site]
def seasonal_data(var, start, end):

    # information for how to create the seasonal array
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)

    # create data by site and by season for entire time period of form
    # seasonal_data[month][site]
    var_shape = np.ma.shape(var)
    no_sites = var_shape[0]
    no_years = var_shape[1]
    days_in_year = var_shape[2]
    seasonal_data = {}
    season_data = np.zeros(((month_start_end_inds[end] - month_start_end_inds[start-1]) * no_years, no_sites))  # is this right???
    for j in range(0, no_sites):
        season_data[:, j] = np.ndarray.flatten(var[j, :, month_start_end_inds[start-1]:month_start_end_inds[end]])  # is this right???
    seasonal_data[1] = season_data  # only built for one season's data at the moment
    return seasonal_data, no_years, no_sites

# this is the improved function of above
def seasonal_data_2(var, start, end):
    # information for how to create the seasonal array
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)

    # create data by site and by season for entire time period of form
    # seasonal_data[month][site]
    var_shape = np.ma.shape(var)
    no_sites = var_shape[0]
    no_years = var_shape[1]
    days_in_year = var_shape[2]
    season_day_indices = range(month_start_end_inds[start-1], (month_start_end_inds[end]))
    seasonal_data = var[:, :, season_day_indices]

    return seasonal_data, no_years, no_sites


# this function will cycle through each site per month and find the mean value of a defined ensemble
def monthly_mean_summary(var, ens_length, ob_sim):

    # load data and number of years
    data, no_years, no_sites = monthly_data(var)

    # divide into ens_length-year ensembles (e.g. if no_years = 300, no_ens = 300/30 = 10
    no_ens = int(math.floor(no_years / ens_length))

    # number of sites
    no_sites = no_sites

    # 1. calculate average for entire period

    print('Processing all values together ')

    # create empty frame to populate with average values per month at each site
    data_avg = pd.DataFrame(columns=['month', 'site', 'mean_value', 'sd_value'])
    # cycle through months
    for month in range(0, 12):
        # cycle through sites
        for site in range(0, no_sites):
            mean_value = np.mean(data[month][:, site])
            sd_value = np.std(data[month][:, site])
            data_append = pd.DataFrame({'month': int(month+1), 'site': int(site+1), 'mean_value': mean_value,
                                        'sd_value':sd_value}, index=[0])
            data_avg = pd.concat([data_avg, data_append])

    if ob_sim == 1:

        # 2. calculate average for ens_length-year ensembles

        # create empty frame to populate with average values per month at each site
        data_avg_ens = pd.DataFrame(columns=['month', 'site', 'ens', 'mean_value', 'sd_value'])
        for k in range(0,no_ens):

            print('Processing ensemble ' + str(k + 1) + ' of ' + str(no_ens))

            # create empty frame to populate with average values per month at each site in particular ensemble
            data_avg_ens_working = pd.DataFrame(columns=['month', 'site', 'ens', 'mean_value', 'sd_value'])
            # cycle through months
            for month in range(0, 12):

                # number of days in each month
                month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                # starting position of ensemble slice in particular month
                slice_size = month_days[month] * ens_length

                # cycle through sites
                for site in range(0, no_sites):
                    mean_value = np.mean(data[month][k*slice_size:(k+1)*slice_size, site])
                    sd_value = np.std(data[month][k*slice_size:(k+1)*slice_size, site])
                    data_append = pd.DataFrame({'month': int(month+1), 'site': int(site+1), 'ens': int(k+1),
                                                'mean_value': mean_value, 'sd_value': sd_value}, index=[0])
                    data_avg_ens_working = pd.concat([data_avg_ens_working, data_append])

            # append to master ensemble file
            data_avg_ens = pd.concat([data_avg_ens,data_avg_ens_working])

        return data_avg, data_avg_ens

    if ob_sim == 0:
        return data_avg


# this function will cycle through each site for selected season and find the percentile values of observed values
def seasonal_percentile_calculator(var, start, end, pctile):

    # information for how to create the seasonal array
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)

    # load data and number of years
    data, no_years, no_sites = seasonal_data(var, start, end)

    # calculate percentile for each site
    pctile_data = {}
    for j in range(0, no_sites):
        pctile_data[1, j] = np.percentile(np.ndarray.flatten(var[j, :, month_start_end_inds[start-1]:month_start_end_inds[end]]), pctile)

    return pctile_data


# this function will take the entire of Europe for selected season and find the percentile values of observed values
def seasonal_percentile_calculator_europe(var, start, end, pctile):

    # information for how to create the seasonal array
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)

    # load data and number of years
    data, no_years, no_sites = seasonal_data_2(var, start, end)

    # take average for entire europe for each day for the entire period
    days = (month_start_end_inds[end] - month_start_end_inds[start-1])
    num_days = days * no_years
    avg_data = np.zeros(num_days)
    for j in range(0,no_years):
        for i in range(0, days):
            k = j*days+i
            avg_data[k] = np.mean(np.ndarray.flatten(data[:, j, i]))

    # calculate percentile for Europe
    pctile_data = np.percentile(avg_data,pctile)
        # pctile_data[1, j] = np.percentile(np.ndarray.flatten(var[j, :, month_start_end_inds[start-1]:month_start_end_inds[end]]), pctile)

    return pctile_data


# this function will cycle through each site for selected season and sum the variable
def seasonal_sum_calculator(var, start, end):

    # information for how to create the seasonal array
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)

    # load data and number of years
    data, no_years, no_sites = seasonal_data(var, start, end)

    # calculate sum for each site
    sum_data = np.zeros((no_sites, no_years))
    for j in range(0, no_sites):
        for k in range(0, no_years):
            sum_data[j, k] = 86400 * np.sum(np.ndarray.flatten(var[j, k, month_start_end_inds[start-1]:month_start_end_inds[end]]))

    return sum_data

# this function will create a heatwave summary for a chosen footprint (which could be Europe but also a country)
def seasonal_hw_duration_summary_europe(var, var_process, start, end, pctile):

    print('Calculating seasonal heatwave duration summary for loaded data')

    # information for how to create the seasonal array
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)

    # load data to process, number of years
    data, no_years, no_sites = seasonal_data_2(var_process, start, end)

    # no_years = var_process.shape[1]

    # calculate where the pctile desired is for europe from a source dataset
    pctile_data = seasonal_percentile_calculator_europe(var, start, end, pctile)

    # take average for entire footprint for each day for the entire period
    days = (month_start_end_inds[end] - month_start_end_inds[start-1])
    num_days = days * no_years
    avg_data = np.zeros(num_days)
    for j in range(0, no_years):
        for i in range(0, days):
            k = j*days+i
            avg_data[k] = np.mean(np.ndarray.flatten(data[:, j, i]))

    # for each year, calculate maximum number of consecutive days above XXth percentile from pctile_data
    no_days = (month_start_end_inds[end] - month_start_end_inds[start - 1])
    consecutive_data = np.zeros(no_years)

    # iteratively go through years to figure out number of days over a threshold selected
    for i in range(0, no_years):
            # assign seasonal data to the year
            year_data = np.ndarray.flatten(avg_data[(i*no_days):((i+1)*no_days)])
            # recover percentile data for comparison
            pctile_threshold = pctile_data
            # test on entire year for above or below threshold
            threshold_data = [0 if a < pctile_threshold else 1 for a in year_data]
            # figure out longest consecutive over threshold (equivalent of rle in R and outputting longest 'streak')
            consecutive_data[i] = consecutive_one(threshold_data)

    print('Processed heat wave duration summary for loaded data')

    return consecutive_data


# this function will calculate the seasonal averages for each site
def seasonal_mean_calculator(var, start, end):

    temp_array = seasonal_sum_calculator(var, start, end)
    no_sites = temp_array.shape[0]

    mean_data = np.zeros((int(no_sites), 1))
    for j in range(0, no_sites):
        mean_data[j] = np.mean(np.ndarray.flatten(temp_array[j, :]))

    return mean_data


# this function will cycle through each site per year for selected season and figure out how many consecutive days are above a threshold
# TO FINISH
def seasonal_hw_duration_summary(var, var_process, start, end, pctile):

    # information for how to create the seasonal array
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)

    # load data to process, number of years and number of sites
    data, no_years, no_sites = seasonal_data_2(var_process, start, end)

    # calculate where the pctile desired is for each site from a source dataset
    pctile_data = seasonal_percentile_calculator(var, start, end, pctile)

    # for each year, at each site, calculate maximum number of consecutive days above XXth percentile from pctile_data
    no_days = (month_start_end_inds[end] - month_start_end_inds[start - 1])
    year_data = np.zeros((no_days, no_years, no_sites))
    threshold_data = np.zeros((no_days, no_years, no_sites))
    consecutive_data = np.zeros((no_years, no_sites))
    for i in range(0, no_years):
        for j in range(0, no_sites):
            # assign seasonal data to the year and site
            year_data[:, i, j] = np.ndarray.flatten(var_process[j, :, month_start_end_inds[start-1]:month_start_end_inds[end]])[(i*no_days):((i+1)*no_days)]
            # recover percentile data for comparison
            pctile_threshold = pctile_data[1, j]
            # test on entire year for above or below threshold
            threshold_data[:, i, j] = [0 if a < pctile_threshold else 1 for a in year_data[:, i, j]]
            # figure out longest consecutive over threshold (equivalent of rle in R and outputting longest 'streak')
            consecutive_data[i, j] = consecutive_one(threshold_data[:, i, j])
            print(i,j)

    return consecutive_data


# rle equivalent in R to give longest string of 1's
def consecutive_one(data):
    longest = 0
    current = 0
    for num in data:
        if num == 1:
            current += 1
        else:
            longest = max(longest, current)
            current = 0

    return max(longest, current)

# rle equivalent in R to give longest string of 1's
def consecutive_zero(data):
    longest = 0
    current = 0
    for num in data:
        num= 1- num
        if num == 1:
            current += 1
        else:
            longest = max(longest, current)
            current = 0

    return max(longest, current)


if __name__ == '__main__':
    data = [0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0]
    print(consecutive_one(data))


# generate return periods based on results for observed and simulated data
# return period = (n+1)/m, where n=number of years in data set, m=rank of exceedence probability
# based on http://geog.uoregon.edu/amarcus/geog422/Handout_Recurrence_calcs.htm
def hw_durationreturn_periods(data):
    data_master = pd.DataFrame()
    for j in range(0, data.shape[1]):
        # for each location, generate a probability rank, where lowest number is lowest ranked
        rank_data = len(data[:, j]) + 1 - rankdata(data[:, j], method='min')

        # calculate return period
        return_period = (len(data[:, j]) + 1) / rank_data

        # collect values of heat wave intensity and return period for each location
        data_current = pd.DataFrame({'site': (j + 1), 'days_over': np.unique(data[:, j]),
                                     'return_period': np.unique(return_period)})
        data_master = pd.concat([data_master.reset_index(drop=True), data_current.reset_index(drop=True)], axis=0)
        # data_master.append(data_current, ignore_index=True)

    return data_master


# generate return periods based on results for observed and simulated data
# return period = (n+1)/m, where n=number of years in data set, m=rank of exceedence probability
# based on http://geog.uoregon.edu/amarcus/geog422/Handout_Recurrence_calcs.htm
def hw_duration_return_periods_europe(data):

    print('loading data to calculate return periods')

    print(data)

    data_master = pd.DataFrame()
    # for entire country/region, generate a probability rank, where lowest number is lowest ranked
    rank_data = len(data) + 1 - rankdata(data, method='min')

    print(rank_data)

    # calculate return periods
    return_period = (len(data) + 1) / rank_data

    print(np.unique(data))
    print(np.unique(return_period))

    # collect values of heat wave intensity and return period for each location
    data_current = pd.DataFrame({'days_over': data,
                                     'return_period': return_period})
    data_current.drop_duplicates(inplace=True)
    # data_current = np.unique(data_current)
    # data_current = pd.DataFrame({'days_over': np.unique(data),
    #                                  'return_period': np.unique(return_period)})

    print('return periods calculated')

    return data_current


# drought calculator
def seasonal_drought_duration_summary_europe(var, var_process, start, end, pctile):

    # information for how to create the seasonal array
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)

    # load data to process, number of years
    data, no_years, no_sites = seasonal_data_2(var_process, start, end)

    no_years = var_process.shape[1]

    # calculate where the pctile desired is for europe from a source dataset
    pctile_data = seasonal_percentile_calculator_europe(var, start, end, pctile)

    # take average for entire europe for each day for the entire period
    days = (month_start_end_inds[end] - month_start_end_inds[start-1])
    num_days = days * no_years
    avg_data = np.zeros(num_days)
    for j in range(0,no_years):
        for i in range(0, days):
            k = j*days+i
            avg_data[k] = np.mean(np.ndarray.flatten(data[:, j, i]))

    # for each year, calculate maximum number of consecutive days below XXth percentile from pctile_data
    no_days = (month_start_end_inds[end] - month_start_end_inds[start - 1])
    consecutive_data = np.zeros((no_years))
    for i in range(0, no_years):
            # assign seasonal data to the year
            year_data = np.ndarray.flatten(avg_data[(i*no_days):((i+1)*no_days)])
            # recover percentile data for comparison
            pctile_threshold = pctile_data
            # test on entire year for above or below threshold
            threshold_data = [0 if a > pctile_threshold else 1 for a in year_data]
            # figure out longest consecutive over threshold (equivalent of rle in R and outputting longest 'streak')
            consecutive_data[i] = consecutive_zero(threshold_data)
            print(i)

    return consecutive_data


# this function will create a drought summary for a chosen footprint (which could be Europe but also a country)
def seasonal_drought_duration_summary_europe_2(var, var_process, start, end, pctile):

    print('Calculating seasonal drought duration summary for loaded data')

    # information for how to create the seasonal array
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)

    # load data to process, number of years
    data, no_years, no_sites = seasonal_data_2(var_process, start, end)

    # calculate where the pctile desired is for europe from a source dataset
    pctile_data = seasonal_percentile_calculator_europe(var, start, end, pctile)

    # take average for entire footprint for each day for the entire period
    days = (month_start_end_inds[end] - month_start_end_inds[start-1])
    num_days = days * no_years
    avg_data = np.zeros(num_days)
    for j in range(0, no_years):
        for i in range(0, days):
            k = j*days+i
            avg_data[k] = np.mean(np.ndarray.flatten(data[:, j, i]))

    # for each year, calculate maximum number of consecutive days above XXth percentile from pctile_data
    no_days = (month_start_end_inds[end] - month_start_end_inds[start - 1])
    consecutive_data = np.zeros(no_years)

    # iteratively go through years to figure out number of days over a threshold selected
    for i in range(0, no_years):
            # assign seasonal data to the year
            year_data = np.ndarray.flatten(avg_data[(i*no_days):((i+1)*no_days)])
            # recover percentile data for comparison
            pctile_threshold = pctile_data
            # test on entire year for above or below threshold
            threshold_data = [0 if a < pctile_threshold else 1 for a in year_data]
            # figure out longest consecutive over threshold (equivalent of rle in R and outputting longest 'streak')
            consecutive_data[i] = consecutive_one(threshold_data)

    print('Processed seasonal drought duration summary for loaded data')

    return consecutive_data
