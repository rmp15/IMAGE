# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 16:24:03 2017

@author: srh110
"""

from monthly_climatology import monthly_climatology, monthly_pctile
import numpy as np





#    obs_95pctile = monthly_pctile(var_o,pctile)
#    
def perc_area_exceed(var,obs_pctile,months):    
    var_shape = np.ma.shape(var)
    no_days_in_year = var_shape[0]
    no_years = var_shape[1]
    no_sites = var_shape[2]
    
    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)    
    
    yearly_sites_exceed_p = {}
    
    for month in months:
        sites_exceed_p = np.zeros((month_days[month],no_years))
        day_indices = np.linspace(int(month_start_end_inds[month]),int(month_start_end_inds[month+1]-1),month_days[month])
        day_indices = day_indices.astype(int)
        d_ind = 0
        for day in day_indices:
            print(day)
            for year in range(0,no_years):
                
                sites_x = 0
                for site in range(0,no_sites):
                    if var[day,year,site] > obs_pctile[month,site]:
                        sites_x += 1
                sites_exceed_p[d_ind,year] = sites_x
            d_ind += 1
        yearly_sites_exceed_p[month] = sites_exceed_p
    
    month_exceed_extremes = {}
    
    for month in months:
        day_year_data = yearly_sites_exceed_p[month]
        all_month_data = np.ndarray.flatten(day_year_data,order='F')
        all_month_data_extremes = sorted(all_month_data,reverse=True)
        month_exceed_extremes[month] = all_month_data_extremes
    return month_exceed_extremes
    
def ann_perc_area_exceed(var,obs_pctile):
    var_shape = np.ma.shape(var)
    no_days_in_year = var_shape[0]
    no_years = var_shape[1]
    no_sites = var_shape[2]
    
    sites_exceed_p = np.zeros((no_days_in_year,no_years))
    for day in range(no_days_in_year):
        print('day:', day)
        for year in range(no_years):
            
            sites_x = 0
            for site in range(no_sites):
                if var[day,year,site] > obs_pctile[site]:
                    sites_x += 1
            sites_exceed_p[day,year] = sites_x
    return sites_exceed_p