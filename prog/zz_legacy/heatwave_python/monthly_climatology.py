# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 18:02:45 2017

@author: srh110
"""

import numpy as np

def monthly_climatology(var):
    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)
    var_shape = np.ma.shape(var)
    days_in_year = var_shape[0]
    no_years = var_shape[1]
    no_sites = var_shape[2]
    month_clim = np.zeros((12,no_sites))
    for i in range(0,12):
        for j in range(0,no_sites):
            month_clim[i,j] = np.mean(var[month_start_end_inds[i]:month_start_end_inds[i+1],:,j])
    return month_clim
    
def seasonal_climatology(var):
    var_shape = np.shape(var)
    no_days = var_shape[0]
    no_sites = var_shape[2]
    if no_days == 365:
        seasonal_clim = np.zeros((4,no_sites))
        for j in range(0,no_sites):
            seasonal_clim[0,j] = np.mean(np.concatenate((var[0:59,:,j],var[334:,:,j]),axis=0)) - 273.15
            seasonal_clim[1,j] = np.mean(var[59:151,:,j]) - 273.15
            seasonal_clim[2,j] = np.mean(var[151:243,:,j]) - 273.15
            seasonal_clim[3,j] = np.mean(var[243:334,:,j]) - 273.15
    elif no_days == 92:
        seasonal_clim = np.zeros((4,no_sites))
        seasonal_clim[2,:] = np.mean(np.mean(var,axis=0),axis=0) - 273.15
    return seasonal_clim
    
def monthly_pctile(var,pctile):
    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)
    var_shape = np.ma.shape(var)
    days_in_year = var_shape[0]
    no_years = var_shape[1]
    no_sites = var_shape[2]
    month_pctile = np.zeros((12,no_sites))

    for i in range(0,12):
        for site in range(0,no_sites):

            
            month_pctile[i,site] = np.percentile(np.ndarray.flatten(var[month_start_end_inds[i]:month_start_end_inds[i+1],:,site]),pctile)
    return month_pctile
            
def monthly_data(var):
    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    month_start_end_inds = month_start_end_inds.astype(int)
    var_shape = np.ma.shape(var)
    days_in_year = var_shape[0]
    no_years = var_shape[1]
    no_sites = var_shape[2]
    monthly_data = {}
    for i in range(0,12):
        month_data = np.zeros(((month_start_end_inds[i+1]-month_start_end_inds[i])*no_years,no_sites))
        for j in range(0,no_sites):
            month_data[:,j] = np.ndarray.flatten(var[month_start_end_inds[i]:month_start_end_inds[i+1],:,j])
        monthly_data[i] = month_data
    return monthly_data
    
def annual_pctile(var,pctile):
    var_shape = np.ma.shape(var)
    days_in_year = var_shape[0]
    no_years = var_shape[1]
    no_sites = var_shape[2]
    ann_pctile = np.zeros(no_sites)
    for site in range(0,no_sites):
        ann_pctile[site] = np.percentile(np.ndarray.flatten(var[:,:,site]),pctile)
    return ann_pctile
            