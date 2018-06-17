# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 14:39:41 2017

@author: srh110
"""

import sys

sys.path.append('/net/wrfstore6-10/disk1/srh110/heatwave_python/')

import matplotlib.pyplot as plt
import os
import scipy.io as io
from hw_averager import hw_averager, max_each_year
from numpy import *
#import cartopy as cp
#from europe_map import europe_map, europe_diff_clim_map2
from monthly_climatology import monthly_climatology, monthly_pctile, annual_pctile
from load_mat_var import load_mat_input_var
from get_var_data import get_var_data, get_var_data_10k
from rp_rv import rp_rv, rp_rv_fig, md_rp_rv_annmax, gc_dmv, make_figure, make_label
from perc_area_exceed import ann_perc_area_exceed
from country_borders import country_polygon, country_only_points
from extreme_maps import extreme_maps, annmax_extreme_maps
from ensemble_cut import ensemble_cut, rp_rv_fig_ens, rp_rv_fig_pot_ens
from peak_ot import pot_rp_rv, pot_rp_rv_fixed_thresh
from conf_band import ci_gev_band_sphere, ci_gpd_band_sphere
import scipy.stats as ss
import scikits.bootstrap as boot









file_prefix = 'v4_10k_EUR_hw_'
model_name = 'MPI'

scen_names = ['hist19701999','4520202049','4520702099','8520202049','8520702099']
var_names = ['tasmax','tasmin','tas','tdps','app_t']

var_name = var_names[0]
scen_name = scen_names[0]

os.chdir('/net/wrfstore6-10/disk1srh110/CORDEX_europe_heatwave_input')

lats = load_mat_input_var('eh_lats2.mat','eh_lats')
lons = load_mat_input_var('eh_lons2.mat','eh_lons')

os.chdir('/net/wrfstore6-10/disk1/srh110/European Heatwave Analysis/paper_10k')





gridcells = 'Germany'
ensemble_member_length = 30
no_days = 5
fig_c = 2
time_thr = 3
no_events_des = 90

#load data
var_o, var_s1, var_s2 = get_var_data_10k(var_name,file_prefix,model_name,scen_name)

#cut to gridcells of interest and find daily means
var_o_dmv = gc_dmv(var_o,gridcells)
var_s1_dmv = gc_dmv(var_s1,gridcells)
var_s2_dmv = gc_dmv(var_s2,gridcells)
var_s1 = int16((var_s1-273.15)*100)
var_s2 = int16((var_s2-273.15)*100)
var_s_dmv = concatenate((var_s1_dmv,var_s2_dmv),axis=1) 

var_s1 = None
var_s2 = None
#var_o = None
#var_s = None
#var_s_ens = ensemble_cut(var_s_dmv,ensemble_member_length)
#ex_inds = make_figure('AnnMax',var_o_dmv,var_s_ens,no_days,fig_c,cbands=False,extrap_obs=False)
#make_label('AnnMax',var_name,model_name,scen_name,no_days,gridcells)
ensemble_member_length = 10000
var_s_ens = ensemble_cut(var_s_dmv,ensemble_member_length)
ex_inds2 = make_figure('AnnMax',var_o_dmv,var_s_ens,no_days,fig_c,scol='blue')
fig_c += 1
#annmax_extreme_maps(var_s,var_o,ex_inds2[0,0,:],fig_c,lats,lons,no_days)
#make_figure('POT',var_o_dmv,var_s_ens,no_days,fig_c,time_thresh=time_thr,no_events_desired=no_events_des)
#make_label('POT',var_name,model_name,scen_name,no_days,gridcells)




