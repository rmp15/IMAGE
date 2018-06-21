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




