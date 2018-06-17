# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:24:34 2017

@author: srh110
"""
import sys
sys.path.append('C:/Anaconda/Anaconda/heatwaves/')

from europe_map import europe_hw_map
from load_mat_var import load_mat_input_var
import os


os.chdir('W:/srh110/CORDEX_europe_heatwave_test2')

lats = load_mat_input_var('lattest2MPI_hist19701999.mat','eh_lats')
lons = load_mat_input_var('lontest2MPI_hist19701999.mat','eh_lons')
tasmax_v = load_mat_input_var('tasmaxtest2MPI_hist19701999.mat','concatted_vari')

europe_hw_map(2,tasmax_v[0,0,:],lats,lons,260,320,'inferno')


