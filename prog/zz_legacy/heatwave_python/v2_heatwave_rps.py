# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:40:12 2017

@author: srh110
"""


import sys

sys.path.append('C:\Anaconda\Anaconda\heatwaves')

import matplotlib.pyplot as plt
from os import chdir
import scipy.io as io
from hw_averager import hw_averager, max_each_year
from numpy import *
import cartopy as cp
from europe_map import europe_map, europe_diff_clim_map2
from monthly_climatology import monthly_climatology, monthly_pctile, annual_pctile
from load_mat_var import load_mat_input_var
from get_var_data import get_var_data
from rp_rv import rp_rv, rp_rv_fig, md_rp_rv
from perc_area_exceed import ann_perc_area_exceed
from country_borders import country_polygon, country_only_points
from extreme_maps import extreme_maps

os.chdir('W:/srh110/CORDEX_europe_heatwave_input')

lats = load_mat_input_var('eh_lats2.mat','eh_lats')
lons = load_mat_input_var('eh_lons2.mat','eh_lons')




file_prefix = 'v2_EUR_hw_'
model_name = 'MPI'

scen_names = ['hist19701999','4520202049','4520702099','8520202049','8520702099']
var_names = ['tasmax','tasmin','tas','tdps']

all_data = {}

country_name = 'France'

c_poly = country_polygon(country_name)
c_gcs = country_only_points(lats,lons,c_poly)

gcs = c_gcs
fig_c = 1

chdir('W:/srh110/European Heatwave Analysis')

for scen in range(0,1):
    for var in range(1):
        var_o, var_s = get_var_data(var_names[var],file_prefix,model_name,scen_names[scen])
       
        rp_o, rv_o, ex_y_d_o = rp_rv(var_o,gcs)
        rp_s, rv_s, ex_y_d_s = rp_rv(var_s,gcs)   
        rp_rv_fig(fig_c,rp_o,rv_o,rp_s,rv_s)
        plt.savefig((var_names[var]+model_name+scen_names[scen]+country_name+'_abs.png'))
        fig_c += 1
        d3_rp_o, d3_rv_o = md_rp_rv(var_o,gcs,3)
        d3_rp_s, d3_rv_s = md_rp_rv(var_s,gcs,3)
        rp_rv_fig(fig_c,d3_rp_o,d3_rv_o,d3_rp_s,d3_rv_s)
        fig_c += 1
#       
#        ann_pctile = annual_pctile(var_o,95)
#        obs_95p_x = ann_perc_area_exceed(var_o,ann_pctile)
#        rp_95p_o, rv_95p_o = rp_rv(obs_95p_x,'none')
#        sim_95p_x = ann_perc_area_exceed(var_s,ann_pctile)
#        rp_95p_s, rv_95p_s = rp_rv(sim_95p_x,'none')
#        rp_rv_fig(fig_c,rp_95p_o,rv_95p_o,rp_95p_s,rv_95p_s)
#        plt.savefig((var_names[var]+model_name+scen_names[scen]+'_95p.png'))       
#        fig_c += 1

#extreme_maps(var_o,var_o,ex_y_d_o,4,lats,lons)
#extreme_maps(var_s,var_o,ex_y_d_s,5,lats,lons)