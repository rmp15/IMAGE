# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 10:00:35 2017

@author: srh110
"""

import numpy as np

def lat_lon_gridder(lats,lons,data):
    unique_lons = np.unique(lons)
    unique_lats = np.unique(lats)
    lon_spaces = np.diff(unique_lons)
    lat_spaces = np.diff(unique_lats)
    lon_space = np.min(lon_spaces)
    lat_space = np.min(lat_spaces)
    no_lons = ((unique_lons[-1] - unique_lons[0]) / lon_space) + 1
    no_lats = ((unique_lats[-1] - unique_lats[0]) / lat_space) + 1
    grid_lons = np.linspace(unique_lons[0],unique_lons[-1],no_lons)
    grid_lats = np.linspace(unique_lats[0],unique_lats[-1],no_lats)
    grid_center_lons = grid_lons - (.5 * lon_space)
    grid_center_lats = grid_lats - (.5 * lat_space)

    grid_data = np.empty((np.size(grid_lats),np.size(grid_lons)))
    grid_data[:] = np.NAN
    for i in range(0,np.size(data)):
        lat_i = lats[i]
        lon_i = lons[i]
        lat_index = int((lat_i - grid_lats[0]) / lat_space)
        lon_index = int((lon_i - grid_lons[0]) / lon_space)
        grid_data[lat_index,lon_index] = data[i]
    return grid_center_lats, grid_center_lons, grid_data