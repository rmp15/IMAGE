# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 13:54:53 2017

@author: srh110
"""

from load_mat_var import load_mat_var
from monthly_climatology import monthly_pctile
from europe_map import europe_hw_map

model_name = 'MPI'
scen_names = ['hist19701999','4520202049','4520702099','8520202049','8520702099']
var_names = ['tasmax','tasmin','tas','tdps']

var_name = var_names[0]
scen_name = scen_names[0]

var_o = load_mat_var(var_name,model_name,scen_name,'o')
var_o_shape = np.ma.shape(var_o)
o_years = var_o_shape[1]
print('var loaded')
var_s = load_mat_var(var_name,model_name,scen_name,'s')
var_s_shape = np.ma.shape(var_s)
s_years = var_s_shape[1]
print('var loaded')

obs_95pctile = monthly_pctile(var_o,95)
sim_95pctile = monthly_pctile(var_s,95)

pctile_diff = sim_95pctile - obs_95pctile

europe_hw_map(1,pctile_diff[0,:],-2,2,'seismic')
europe_hw_map(2,pctile_diff[1,:],-2,2,'seismic')
europe_hw_map(3,pctile_diff[2,:],-2,2,'seismic')
europe_hw_map(4,pctile_diff[3,:],-2,2,'seismic')
europe_hw_map(5,pctile_diff[4,:],-2,2,'seismic')
europe_hw_map(6,pctile_diff[5,:],-2,2,'seismic')
europe_hw_map(7,pctile_diff[6,:],-2,2,'seismic')
europe_hw_map(8,pctile_diff[7,:],-2,2,'seismic')
europe_hw_map(9,pctile_diff[8,:],-2,2,'seismic')
europe_hw_map(10,pctile_diff[9,:],-2,2,'seismic')
europe_hw_map(11,pctile_diff[10,:],-2,2,'seismic')
europe_hw_map(12,pctile_diff[11,:],-2,2,'seismic')