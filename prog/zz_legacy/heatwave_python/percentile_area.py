# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 10:30:03 2017

@author: srh110
"""

import sys

sys.path.append('C:\Anaconda\Anaconda\heatwaves')

import matplotlib.pyplot as plt
import numpy as np
from perc_area_exceed import perc_area_exceed
from monthly_climatology import monthly_climatology, monthly_pctile
from combine_month_exceed_areas import combine_month_exceed_areas
from load_mat_var import load_mat_var

model_name = 'MPI'
scen_names = ['hist19701999','4520202049','4520702099','8520202049','8520702099']
var_names = ['tasmax','tasmin','tas','tdps']

for s in range(0,1):

    var_name = var_names[0]
    scen_name = scen_names[s]
    
    var_o = load_mat_var(var_name,model_name,scen_name,'o')
    var_o_shape = np.ma.shape(var_o)
    o_years = var_o_shape[1]
    print('var loaded')
    var_s = load_mat_var(var_name,model_name,scen_name,'s')
    var_s_shape = np.ma.shape(var_s)
    s_years = var_s_shape[1]
    print('var loaded')
    
    obs_climatology = monthly_climatology(var_o)
    obs_95pctile = monthly_pctile(var_o,95)
    
    summer_months = [0]
    month_area_exceed_o = perc_area_exceed(var_o,obs_95pctile,summer_months)
    month_area_exceed_s = perc_area_exceed(var_s,obs_95pctile,summer_months)
    
    tot_month_area_exceed_o = combine_month_exceed_areas(month_area_exceed_o,summer_months)
    tot_month_area_exceed_s = combine_month_exceed_areas(month_area_exceed_s,summer_months)
    
    rp_s_size = 2000
    rp_o_size = 400
    
    rp_s = np.zeros(rp_s_size)
    rp_o = np.zeros(rp_o_size)
    
    for i in range(0,rp_s_size):
        rp_s[i] = s_years / (i+1)
    for i in range(0,rp_o_size):
        rp_o[i] = o_years / (i+1)
        
    plt.figure(s)
    plt.scatter(rp_s,tot_month_area_exceed_s[0:rp_s_size],marker='x',c='r',label='Sim')
    plt.scatter(rp_o,tot_month_area_exceed_o[0:rp_o_size],marker='x',c='b',label='Obs')
    plt.xscale('log')
    plt.xlabel('Return period (years)')
    plt.ylabel('No Grid Cells')
    plt.title(var_name + scen_name)
    plt.legend(loc=2,scatterpoints=1)
