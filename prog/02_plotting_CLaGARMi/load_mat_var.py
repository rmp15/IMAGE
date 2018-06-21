import scipy.io as io
import os as os
import h5py
from data.file_paths.file_paths import *
import numpy as np


def load_mat_var(step, num_years, continent, scen_name, start_year, end_year, var):

    # fn_o = 'out_' + step + '_y' + str(num_years) + '_' + continent + '_' + str(scen_name) + '_' + str(start_year) + '_' + str(end_year) + '_' + var + '_o.mat'
    # fn_s = 'out_' + step + '_y' + str(num_years) + '_' + continent + '_' + str(scen_name) + '_' + str(start_year) + '_' + str(end_year) + '_' + var + '_s.mat'

    # o_array = o[list(o.keys())[0]]
    # s_array = s[list(s.keys())[0]]

    # o = h5py.File(os.path.join(image_output_local, fn_o), 'r')
    # s = h5py.File(os.path.join(image_output_local, fn_s), 'r')

    fn = 'out_' + step + '_y' + str(num_years) + '_' + continent + '_' + str(scen_name) + '_' + str(start_year) + '_' + str(end_year) + '.mat'

    file = h5py.File(os.path.join(image_output_local, fn), 'r')

    o_1 = file['mv']['o'][0]
    o_2 = file['mv']['o'][1]
    s_1 = file['mv']['s'][0]
    s_2 = file['mv']['s'][1]

    return o_1, o_2, s_1, s_2
