import scipy.io as io
import os as os
import h5py
from data.file_paths.file_paths import *
import numpy as np
import pandas as pd
import math

# based on steve's previous code in legacy 'load_mat_var.py'
def load_clag_output(step, num_years, continent, scen_name, start_year, end_year, var):

    fn_o = var + '/out_' + step + '_y' + str(num_years) + '_' + continent + '_' + str(scen_name) + '_' + str(start_year) + '_' + str(end_year) + '_' + var + '_o.mat'
    fn_s = var + '/out_' + step + '_y' + str(num_years) + '_' + continent + '_' + str(scen_name) + '_' + str(start_year) + '_' + str(end_year) + '_' + var + '_s.mat'

    o = h5py.File(os.path.join(image_output_local, fn_o), 'r')
    s = h5py.File(os.path.join(image_output_local, fn_s), 'r')

    o_array = np.array(o[list(o.keys())[0]])
    s_array = np.array(s[list(s.keys())[0]])

    return o_array, s_array


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


# this function will cycle through each site per month and find the mean value of a defined ensemble
def monthly_summary(var, ens_length, ob_sim):

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

