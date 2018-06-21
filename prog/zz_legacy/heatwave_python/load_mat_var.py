# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 11:01:44 2017

@author: srh110
"""

import scipy.io as io
import os as os
import h5py

def load_mat_var(var_name,model_name,scen_name,ob_sim):
    #os.chdir('W:/srh110')
    if ob_sim == 'o':
        ob = '_o'
    elif ob_sim == 's':
        ob = '_'
    else:
        return None
       
    file_name = var_name + ob + model_name + '_' + scen_name + '.mat'

    loadmat1 = io.loadmat(file_name)
    mat_var_name = var_name + '_s'
        
    var_o = loadmat1[mat_var_name]
    return var_o
    
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