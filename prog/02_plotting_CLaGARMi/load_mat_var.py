import scipy.io as io
import os as os
import h5py
from data.file_paths.file_paths import *


def load_mat_var(step, num_years, continent, scen_name, start_year, end_year):

    file_name = 'out_' + step + '_y' + str(num_years) + '_' + continent + '_' + str(scen_name) + '_' + str(start_year) + '_' + str(end_year) + '.mat'

    loadmat1 = h5py.File(os.path.join(image_output_local, file_name), 'r')

    # mat_var_name = var_name + '_s' # how does this work from the file itself?
        
    # var_o = loadmat1[mat_var_name]
    # return loadmat1 #var_o


def load_mat_input_var(fn,var_name):
    loadmat1 = io.loadmat(fn)
    var_o = loadmat1[var_name]
    return var_o


def load_mat_var_73(var_name,model_name,scen_name,ob_sim):
    if ob_sim == 'o':
        ob = '_o'
    elif ob_sim == 's':
        ob = '_'
    else:
        return None
       
    file_name = var_name + ob + model_name + '_' +  scen_name + '.mat'

    
    f = h5py.File(file_name)
    f.keys()    