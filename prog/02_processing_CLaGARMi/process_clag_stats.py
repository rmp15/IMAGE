import scipy.io as io
import os as os
import h5py
from data.file_paths.file_paths import *
import numpy as np

# based on steve's previous code in legacy 'load_mat_var.py'
def load_clag_output(step, num_years, continent, scen_name, start_year, end_year, var):

    fn_o = 'out_' + step + '_y' + str(num_years) + '_' + continent + '_' + str(scen_name) + '_' + str(start_year) + '_' + str(end_year) + '_' + var + '_o.mat'
    fn_s = 'out_' + step + '_y' + str(num_years) + '_' + continent + '_' + str(scen_name) + '_' + str(start_year) + '_' + str(end_year) + '_' + var + '_s.mat'

    o = h5py.File(os.path.join(image_output_local, fn_o), 'r')
    s = h5py.File(os.path.join(image_output_local, fn_s), 'r')

    o_array = np.array(o[list(o.keys())[0]])
    s_array = np.array(s[list(s.keys())[0]])

    return o_array, s_array


def monthly_data(var):

    # information for how to create the monthly array
    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)

    # create data by site and by month for entire time period
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
    return monthly_data





# def load_mat_var_together(step, num_years, continent, scen_name, start_year, end_year, var):
#
#     fn = 'out_' + step + '_y' + str(num_years) + '_' + continent + '_' + str(scen_name) + '_' + str(start_year) + '_' + str(end_year) + '.mat'
#
#     file = h5py.File(os.path.join(image_output_local, fn), 'r')
#
#     o_1 = np.array(file['mv']['o']['appt_o'])
#     o_2 = file['mv']['o'][1]
#     s_1 = file['mv']['s'][0]
#     s_2 = file['mv']['s'][1]
#
#     return o_1, o_2, s_1, s_2
#




