# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 16:50:09 2017

@author: srh110
"""

import iris 
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import scipy.io as io
import os
import numpy as np
from lat_lon_gridder import lat_lon_gridder

os.chdir('W:/srh110')


def europe_map(index,lats,lons,data):


    a_shape = np.ma.shape(data)
    data_rs = np.ndarray.reshape(data,(a_shape[0]*a_shape[1],a_shape[2]),order='F')
    data_rs_ind = data_rs[index,:]
    
    
    grid_lats, grid_lons, data_grid = lat_lon_gridder(lats,lons,data_rs_ind)
    data_grid = data_grid - 273.15
    data_grid_mask = np.ma.masked_where(np.isnan(data_grid),data_grid)
    
    
    
    fig = plt.figure(index)
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    plt.pcolormesh(grid_lons, grid_lats, data_grid_mask ,
                 transform=ccrs.PlateCarree(),cmap='inferno',vmin=12,vmax=42)
    
    ax.coastlines()
    
    plt.colorbar()
    plt.show()
    
    return 0
    
def europe_diff_clim_map(index,lats,lons,data,climatology):

    
    a_shape = np.ma.shape(data)
    data_rs = np.ndarray.reshape(data,(a_shape[0]*a_shape[1],a_shape[2]),order='F')
    data_rs_ind = data_rs[index,:]
    
    year_day = index%365
    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    for month in range(0,12):
        if month_start_end_inds[month] <= year_day < month_start_end_inds[month+1]: 
            event_month = month
            break
    data_rs_ind = data_rs_ind - climatology[month,:]
    grid_lats, grid_lons, data_grid = lat_lon_gridder(lats,lons,data_rs_ind)
    
    data_grid_mask = np.ma.masked_where(np.isnan(data_grid),data_grid)
    
    
    
    plt.figure(index+1)
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    plt.pcolormesh(grid_lons, grid_lats, data_grid_mask ,
                 transform=ccrs.PlateCarree(),cmap='seismic',vmin=-15,vmax=15)
    
    ax.coastlines()
    
    plt.colorbar()
    plt.show()
    
    return 0   
    
def europe_hw_map(fig_no,data,lats,lons,min_val,max_val,cmap_name):
#    lat_file_name = 'eh_lats1.mat'
#    lon_file_name = 'eh_lons1.mat' 
#    loadmat1 = io.loadmat(lon_file_name)
#    lons = loadmat1['eh_lons']
#    loadmat1 = io.loadmat(lat_file_name)
#    lats = loadmat1['eh_lats']
    grid_lats, grid_lons, data_grid = lat_lon_gridder(lats,lons,data)
    
    data_grid_mask = np.ma.masked_where(np.isnan(data_grid),data_grid)    
    plt.figure(fig_no)
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    plt.pcolormesh(grid_lons, grid_lats, data_grid_mask ,
                 transform=ccrs.PlateCarree(),cmap=cmap_name,vmin=min_val,vmax=max_val)
    
    ax.coastlines()
    
    plt.colorbar()
    plt.show()
    
def europe_diff_clim_map2(d_index,lats,lons,data,climatology,sp1,sp2,sp3,fig):

    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    month_end_inds = np.cumsum(month_days)
    month_start_end_inds = np.zeros(13)
    month_start_end_inds[0] = 0
    month_start_end_inds[1:] = month_end_inds
    for month in range(0,12):
        if month_start_end_inds[month] <= d_index < month_start_end_inds[month+1]: 
            event_month = month
            break
    data_rs_ind = data - climatology[month,:]
    grid_lats, grid_lons, data_grid = lat_lon_gridder(lats,lons,data_rs_ind)
    
    data_grid_mask = np.ma.masked_where(np.isnan(data_grid),data_grid)
    
    
    
    ax = plt.subplot(sp1,sp2,sp3,projection=ccrs.PlateCarree())
    
    im = plt.pcolormesh(grid_lons, grid_lats, data_grid_mask ,
                 transform=ccrs.PlateCarree(),cmap='seismic',vmin=-15,vmax=15)
    
    ax.coastlines()
    
    #plt.colorbar()
    
    plt.show() 
    return im   
    
def europe_map_sp(lats,lons,data,sp1=1,sp2=1,sp3=1):



    
    
    grid_lats, grid_lons, data_grid = lat_lon_gridder(lats,lons,data)
    data_grid = data_grid - 273.15
    data_grid_mask = np.ma.masked_where(np.isnan(data_grid),data_grid)
    
    
    
    ax = plt.subplot(sp1,sp2,sp3,projection=ccrs.PlateCarree())
    
    im = plt.pcolormesh(grid_lons, grid_lats, data_grid_mask ,
                 transform=ccrs.PlateCarree(),cmap='seismic',vmin=-15,vmax=15)
    
    ax.coastlines()
    
    plt.colorbar()
    plt.show()
   