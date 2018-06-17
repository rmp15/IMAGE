# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 14:51:48 2017

@author: srh110
"""

import sys

sys.path.append('C:\Anaconda\Anaconda\heatwaves')

import matplotlib.pyplot as plt
import os
import scipy.io as io
from hw_averager import hw_averager, max_each_year
from numpy import *
import cartopy as cp
from europe_map import europe_map, europe_diff_clim_map2
from monthly_climatology import monthly_climatology, monthly_pctile, annual_pctile
from load_mat_var import load_mat_input_var
from get_var_data import get_var_data
from rp_rv import rp_rv, rp_rv_fig, md_rp_rv_annmax, gc_dmv, make_figure, make_label, rp_event_calc
from perc_area_exceed import ann_perc_area_exceed
from country_borders import country_polygon, country_only_points
from extreme_maps import extreme_maps
from ensemble_cut import ensemble_cut, rp_rv_fig_ens, rp_rv_fig_pot_ens
from peak_ot import pot_rp_rv, pot_rp_rv_fixed_thresh
from conf_band import ci_gev_band_sphere, ci_gpd_band_sphere
import scipy.stats as ss
import scikits.bootstrap as boot


os.chdir('W:/srh110/CORDEX_europe_heatwave_input')







model_name = 'MPI'

scen_names = ['hist19701999','4520202049','4520702099','8520202049','8520702099']
var_names = ['tasmax','tasmin','tas','tdps','app_t']

var_name = var_names[0]
scen_name = scen_names[0]

os.chdir('W:/srh110/European Heatwave Analysis')

#load data


gridcell_tests = ['France','United Kingdom','Spain','Germany','Russia','all',60,500,750]

x_ax_val = 0

rough_errors = np.zeros((2,18))

for gc_ex in gridcell_tests:

    gridcells = gc_ex
    ensemble_member_length = 15
    no_days = 1
    fig_c = 1
    time_thr = 3
    no_events_des = 90
    
    rp_event_val = 5
    os.chdir('W:/srh110/European Heatwave Analysis')
    file_prefix = 'v3_15y_EUR_hw_'
    var_o, var_s = get_var_data(var_name,file_prefix,model_name,scen_name)
    #cut to gridcells of interest and find daily means
    var_o_dmv = gc_dmv(var_o,gridcells)
    var_s_dmv = gc_dmv(var_s,gridcells)
    var_o = None
    var_s = None
    var_s_ens = ensemble_cut(var_s_dmv,ensemble_member_length)
    rp_o, rv_o1, rp_event_obs_int1, s_ens_rp_events1 = rp_event_calc('AnnMax',var_o_dmv,var_s_ens,no_days,fig_c,rp_event_val,cbands=False,extrap_obs=False)
    
    #make_label('AnnMax',var_name,model_name,scen_name,no_days,gridcells)
    ensemble_member_length = 600
    var_s_ens = ensemble_cut(var_s_dmv,ensemble_member_length)
    _, _, _, s_all_rp_event1 = rp_event_calc('AnnMax',var_o_dmv,var_s_ens,no_days,fig_c,rp_event_val,cbands=False,extrap_obs=False)
    #var_s_ens = ensemble_cut(var_s_dmv,ensemble_member_length)
    #make_figure('AnnMax',var_o_dmv,var_s_ens,no_days,fig_c,scol='blue')
    #fig_c += 1
    
    os.chdir('W:/srh110/European Heatwave Analysis')
    file_prefix = 'v3_15y2_EUR_hw_'
    ensemble_member_length = 10
    var_o, var_s = get_var_data(var_name,file_prefix,model_name,scen_name)
    var_o_dmv = gc_dmv(var_o,gridcells)
    var_s_dmv = gc_dmv(var_s,gridcells)
    var_o = None
    var_s = None
    var_s_ens = ensemble_cut(var_s_dmv,ensemble_member_length)
    rp_o, rv_o2, rp_event_obs_int2, s_ens_rp_events2 = rp_event_calc('AnnMax',var_o_dmv,var_s_ens,no_days,fig_c,rp_event_val,cbands=False,extrap_obs=False)
    
    #make_label('AnnMax',var_name,model_name,scen_name,no_days,gridcells)
    ensemble_member_length = 600
    var_s_ens = ensemble_cut(var_s_dmv,ensemble_member_length)
    _, _, _, s_all_rp_event2 = rp_event_calc('AnnMax',var_o_dmv,var_s_ens,no_days,fig_c,rp_event_val,cbands=False,extrap_obs=False)
    
    all_rv_o = np.zeros(np.size(rv_o1)+np.size(rv_o2))
    all_rv_o[:np.size(rv_o1)] = rv_o1
    all_rv_o[np.size(rv_o1):] = rv_o2
    all_rv_o = sorted(all_rv_o,reverse=True)
    true_rv = all_rv_o[2]
    s_ens_rp_events1 = sorted(s_ens_rp_events1)
    sens1_l = s_ens_rp_events1[1]
    sens1_u = s_ens_rp_events1[-2]
    sens_mean1 = np.mean(s_ens_rp_events1)
    s_ens_rp_events2 = sorted(s_ens_rp_events2)
    sens2_l = s_ens_rp_events2[1]
    sens2_u = s_ens_rp_events2[-2]
    sens_mean2 = np.mean(s_ens_rp_events2)
    
    print('True:', true_rv)
    print('Obs int:', rp_event_obs_int1, rp_event_obs_int2)
    print('IMAGE:', s_all_rp_event1, s_all_rp_event2)
    print('IMAGE ens mean:', sens_mean1, sens_mean2)
    print('IMAGE low ens:', sens1_l, sens2_l)
    print('IMAGE upp ens:', sens1_u, sens2_u)
    
    rough_errors[0,x_ax_val*2] = rp_event_obs_int1 - true_rv
    rough_errors[1,x_ax_val*2] = s_all_rp_event1 - true_rv
    rough_errors[0,(x_ax_val*2)+1] = rp_event_obs_int2 - true_rv
    rough_errors[1,(x_ax_val*2)+1] = s_all_rp_event2 - true_rv
        
    plt.figure(8)
    plt.scatter([(x_ax_val*4)+1],true_rv,c='black',marker='x')
    plt.scatter([(x_ax_val*4)+2],rp_event_obs_int1,c='blue',marker='x')
    plt.scatter([(x_ax_val*4)+2],rp_event_obs_int2,c='red',marker='x')
    plt.scatter([(x_ax_val*4)+3],s_all_rp_event1,c='blue',marker='+')
    plt.scatter([(x_ax_val*4)+3],s_all_rp_event2,c='red',marker='+')
    plt.plot([(x_ax_val*4)+3.25,(x_ax_val*4)+3.25],[sens1_l,sens1_u],c='blue',marker='x')
    plt.plot([(x_ax_val*4)+3.5,(x_ax_val*4)+3.5],[sens2_l,sens2_u],c='red',marker='x')
    
    x_ax_val += 1
    
plt.figure(2)
plt.scatter(rough_errors[1,0:10],rough_errors[0,0:10],c='black',marker='x')
plt.scatter(rough_errors[1,10:12],rough_errors[0,10:12],c='blue',marker='x')
plt.scatter(rough_errors[1,12:18],rough_errors[0,12:18],c='red',marker='x')
plt.plot([-1.5,1.5],[-1.5,1.5],c='black')
plt.xlim(-1.5,1.5)
plt.ylim(-1.5,1.5)

plt.figure(3)
plt.scatter(np.absolute(rough_errors[1,0:10]),np.absolute(rough_errors[0,0:10]),c='black',marker='x')
plt.scatter(np.absolute(rough_errors[1,10:12]),np.absolute(rough_errors[0,10:12]),c='blue',marker='x')
plt.scatter(np.absolute(rough_errors[1,12:18]),np.absolute(rough_errors[0,12:18]),c='red',marker='x')
plt.plot([0,1.5],[0,1.5],c='black')
plt.xlim(0,1.5)
plt.ylim(0,1.5)