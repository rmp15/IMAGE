# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 11:20:43 2017

@author: srh110
"""

import numpy as np
from europe_map import europe_map, europe_diff_clim_map2, europe_map_sp
from monthly_climatology import monthly_climatology, seasonal_climatology
import matplotlib.pyplot as plt

def extreme_maps(var,var_o,ex_y_d,fig_no,lats,lons):

    obs_climatology = monthly_climatology(var_o)
    fig = plt.figure(fig_no)
    for i in range(0,12):
        sp_num = (i + 1) + np.floor(i/3)
        im = europe_diff_clim_map2(ex_y_d[i,1],lats,lons,var[ex_y_d[i,1],ex_y_d[i,0],:],obs_climatology,4,4,sp_num,fig)
    plt.tight_layout() 
    cbar_ax = fig.add_axes([0.8, 0.15, 0.05, 0.7])
    fig.colorbar(im, cax=cbar_ax)


def annmax_extreme_maps(var,var_o,year_day_pair,fig_no,lats,lons,no_days):
    seasonal_clim = seasonal_climatology(var_o)
    summer_clim = seasonal_clim[2,:]
    mean_val = np.mean(var[year_day_pair[1]:year_day_pair[1]+5,year_day_pair[0],:],axis=0) - summer_clim
    europe_map_sp(lats,lons,mean_val)
    
