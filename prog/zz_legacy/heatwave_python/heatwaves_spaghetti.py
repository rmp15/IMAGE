# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 16:33:45 2017

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
from rp_rv import rp_rv, rp_rv_fig, md_rp_rv_annmax
from perc_area_exceed import ann_perc_area_exceed
from country_borders import country_polygon, country_only_points
from extreme_maps import extreme_maps
from ensemble_cut import ensemble_cut, rp_rv_fig_ens, rp_rv_fig_pot_ens
from peak_ot import pot_rp_rv, pot_rp_rv_fixed_thresh
from conf_band import ci_gev_band_sphere, ci_gpd_band_sphere
import scipy.stats as ss
import scikits.bootstrap as boot


def gpd_floc(data):
    p1, p2, p3 = ss.genpareto.fit(data,floc=27)
    print (p1, p2, p3)
    return p1, p3

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
no_days = 3

chdir('W:/srh110/European Heatwave Analysis')

for scen in range(0,1):
    for var in range(1):
        var_o, var_s = get_var_data(var_names[var],file_prefix,model_name,scen_names[scen])
        var_s_ens = ensemble_cut(var_o,var_s)
        rp_o, rv_o = md_rp_rv_annmax(var_o,gcs,no_days)
        no_s_ens = np.shape(var_s_ens)[0]
        rv_s_ens = np.zeros((no_s_ens,np.size(rv_o)))
        for i in range(no_s_ens):
            rp_s, rv_s_ens[i,:] = md_rp_rv_annmax(var_s_ens[i,:,:,:],gcs,no_days)   
        rp_rv_fig_ens(fig_c,rp_o,rv_o,rp_s,rv_s_ens)
        plt.savefig((var_names[var]+model_name+scen_names[scen]+country_name+'_abs.png'))
        fig_c += 1
        
        o_fit_params = ss.genextreme.fit(rv_o)
        boot_params = boot.ci(rv_o,ss.genextreme.fit,n_samples=1000)
        ci_gev_band_sphere(o_fit_params,boot_params)
        plt.xlim(0.75,rp_o[0])
        rp_pot_o, rv_pot_o, opt_thresh = pot_rp_rv(var_o,gcs,no_days,2,90)
        rp_pot_s_ens = {}
        rv_pot_s_ens = {}
        for i in range(no_s_ens):
            rp_pot_s_ens[i], rv_pot_s_ens[i] = pot_rp_rv_fixed_thresh(var_s_ens[i,:,:,:],gcs,no_days,2,opt_thresh) 
        rp_rv_fig_pot_ens(fig_c,rp_pot_o,rv_pot_o,rp_pot_s_ens,rv_pot_s_ens)
        fig_c += 1
        rv_pot_fit = rv_pot_o - opt_thresh
        o_fit_params = ss.genpareto.fit(rv_pot_fit)
        boot_params = boot.ci(rv_pot_fit,ss.genpareto.fit,n_samples=1000)
        ci_gpd_band_sphere(o_fit_params,boot_params,np.size(rv_pot_o),opt_thresh)
        
        plt.ylim(25,42)



