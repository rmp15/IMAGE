# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 15:45:25 2017

@author: srh110
"""
import sys
import numpy as np

sys.path.append('C:\Anaconda\Anaconda\heatwaves')
from load_mat_var import load_mat_input_var
from apparent_temp_c import apparent_temp_c

def load_var_data(var_name,file_prefix,model_name,scen_name):
    
        
    obs_file_name = var_name + '_o_' + file_prefix + model_name + '_' +  scen_name + '.mat'
    sim_file_name = var_name + '_s_' + file_prefix + model_name + '_' +  scen_name + '.mat'
    var_o_name = var_name + '_o'
    var_s_name = var_name + '_s'
    var_o = load_mat_input_var(obs_file_name,var_o_name)
    var_s = load_mat_input_var(sim_file_name,var_s_name)
    return var_o, var_s
    
def get_var_data(var_name,file_prefix,model_name,scen_name):

    var_o, var_s = load_var_data(var_name,file_prefix,model_name,scen_name)
    return var_o, var_s
        
def load_var_data_10k(var_name,file_prefix,model_name,scen_name):
    
        
    obs_file_name = var_name + '_o_' + file_prefix + model_name + '_' +  scen_name + '.mat'
    sim_file_name1 = var_name + '_s1_' + file_prefix + model_name + '_' +  scen_name + '.mat'
    sim_file_name2 = var_name + '_s2_' + file_prefix + model_name + '_' +  scen_name + '.mat'    
    var_o_name = var_name + '_o'
    var_s_name = var_name + '_s'
    var_o = load_mat_input_var(obs_file_name,var_o_name)
    var_s1 = load_mat_input_var(sim_file_name1,var_s_name)
    var_s1 = (var_s1 - 273.15) * 100
    var_s1 = np.int16(var_s1)
    var_s2 = load_mat_input_var(sim_file_name2,var_s_name)
    var_s2 = (var_s2 - 273.15) * 100
    var_s2 = np.int16(var_s2)    
    return var_o, var_s1, var_s2
    
def get_var_data_10k(var_name,file_prefix,model_name,scen_name):

    var_o, var_s1, var_s2 = load_var_data_10k(var_name,file_prefix,model_name,scen_name)
    return var_o, var_s1, var_s2    