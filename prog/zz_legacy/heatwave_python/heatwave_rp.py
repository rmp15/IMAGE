# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 13:51:11 2017

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
from europe_map import europe_map, europe_diff_clim_map
from monthly_climatology import monthly_climatology, monthly_pctile
import sys
from load_mat_var import load_mat_input_var
from get_var_data import get_var_data
from rp_rv import rp_rv, rp_rv_fig

chdir('W:/srh110')


file_prefix = 'v2_EUR_hw_'
model_name = 'MPI'

scen_names = ['hist19701999','4520202049','4520702099','8520202049','8520702099']
var_names = ['tasmax','tasmin','tas','tdps']

all_data = {}

gcs = 'all'
fig_c = 1

for scen in range(0,1):
    for var in range(1):
       var_o, var_s = get_var_data(var_names[var],file_prefix,model_name,scen_names[scen])
       
       rp_o, rv_o = rp_rv(var_o,gcs)
       rp_s, rv_s = rp_rv(var_s,gcs)   
       rp_rv_fig(fig_c,rp_o,rv_o,rp_s,rv_s)
       fig_c += 1
       

scen_heat_extremes = zeros((5,4,5000))
scen_year_max = zeros((5,4,600))
scen_appt_extremes = zeros((5,1000))
qq_s = zeros((5,4,999))
qq_o = zeros((5,4,999))
rps = zeros(600)

for i in range(0,600):
    rps[i] = 600.0/(i+1)
    
rps_d = zeros(5000)

for i in range(0,5000):
    rps_d[i] = 600.0/(i+1)

for scen in range(0,1):
    scen_data = {}
    for var in range(0,1):
        file_name = var_names[var] + '_' + model_name + '_' +  scen_names[scen] + '.mat'
        lat_file_name = 'eh_lats1.mat'
        lon_file_name = 'eh_lons1.mat'
        
        loadmat1 = io.loadmat(file_name)
        mat_var_name = var_names[var] + '_s'
        
        var_s = loadmat1[mat_var_name]
        loadmat1 = io.loadmat(lon_file_name)
        lons = loadmat1['eh_lons']
        loadmat1 = io.loadmat(lat_file_name)
        lats = loadmat1['eh_lats']
        year_max_heat = max_each_year(var_s,1,[0,896])
        region_s1 = hw_averager(var_s,1,[0,896])
        region_s = ndarray.flatten(region_s1,order='F')
        region_s = array(region_s) - 273.15
        heat_extremes = sorted(region_s,reverse=True)
        year_max_heat = sorted(year_max_heat,reverse=True)
        scen_heat_extremes[scen,var,:] = heat_extremes[0:5000]
        scen_year_max[scen,var,:] = year_max_heat
        s_extreme_inds = [p[0] for p in sorted(enumerate(region_s), key=lambda x:-x[1])]
        for i in range(0,999):
            qq_s[scen,var,i] = percentile(heat_extremes,(i+1)/10)

#for scen in range(0,1):
#        file_name = 'tas' + '_' + model_name + '_' +  scen_names[scen] + '.mat'
#        loadmat1 = io.loadmat(file_name)
#        mat_var_name = 'tas' + '_s'        
#        tas = loadmat1[mat_var_name]
#        region_tas = hw_averager(tas,1,[0,1])
#        region_tas = array(list(flatten(region_tas)))
#        region_tas = region_tas - 273.15        
#        file_name = 'tdps' + '_' + model_name + '_' +  scen_names[scen] + '.mat'        
#        loadmat1 = io.loadmat(file_name)
#        mat_var_name = 'tdps' + '_s'        
#        tdps = loadmat1[mat_var_name]  
#        region_tdps = hw_averager(tdps,1,[0,1])
#        region_tdps = array(list(flatten(region_tdps)))
#        region_tdps = region_tdps - 273.15
#        appt = -2.653 + (0.994*region_tas) + (0.0153*region_tdps*region_tdps)
#        appt_extremes = sorted(appt,reverse=True)
#        scen_appt_extremes[scen,:] = appt_extremes[0:1000]

scen_heat_extremes_o = zeros((5,4,1000))
scen_appt_extremes_o = zeros((5,1000))
scen_year_max_o = zeros((5,4,30))
rps_o = zeros(30)

for i in range(0,30):
    rps_o[i] = 30.0/(i+1)
    
rps_o_d = zeros(1000)

for i in range(0,1000):
    rps_o_d[i] = 30.0/(i+1)

for scen in range(0,1):

    for var in range(0,1):
        file_name = var_names[var] + '_o' + model_name + '_' +  scen_names[scen] + '.mat'

        
        loadmat1 = io.loadmat(file_name)
        mat_var_name = var_names[var] + '_s'
        
        var_o = loadmat1[mat_var_name]
        year_max_heat_o = max_each_year(var_o,1,[0,896])
        region_o1 = hw_averager(var_o,1,[0,896])
        region_o = ndarray.flatten(region_o1,order='F')
        region_o = array(region_o) - 273.15
        heat_extremes = sorted(region_o,reverse=True)
        year_max_heat_o = sorted(year_max_heat_o,reverse=True)
        scen_heat_extremes_o[scen,var,:] = heat_extremes[0:1000]
        scen_year_max_o[scen,var,:] = year_max_heat_o
        o_extreme_inds = [p[0] for p in sorted(enumerate(region_o), key=lambda x:-x[1])]
        for i in range(0,999):
            qq_o[scen,var,i] = percentile(heat_extremes,(i+1)/10)

obs_climatology = monthly_climatology(var_o)
obs_95pctile = monthly_pctile(var_o,95)

#rf = europe_map(s_extreme_inds[0],lats,lons,var_s)
#rf = europe_diff_clim_map(s_extreme_inds[0],lats,lons,var_s,obs_climatology)
#rf = europe_map(s_extreme_inds[1],lats,lons,var_s)
#rf = europe_diff_clim_map(s_extreme_inds[1],lats,lons,var_s,obs_climatology)
#rf = europe_map(s_extreme_inds[2],lats,lons,var_s)
#rf = europe_diff_clim_map(s_extreme_inds[2],lats,lons,var_s,obs_climatology)
#rf = europe_map(s_extreme_inds[19],lats,lons,var_s)
#rf = europe_diff_clim_map(s_extreme_inds[19],lats,lons,var_s,obs_climatology)
#rf = europe_map(s_extreme_inds[38],lats,lons,var_s)
#rf = europe_diff_clim_map(s_extreme_inds[38],lats,lons,var_s,obs_climatology)
#rf = europe_map(s_extreme_inds[39],lats,lons,var_s)
#rf = europe_diff_clim_map(s_extreme_inds[39],lats,lons,var_s,obs_climatology)
#rf = europe_map(s_extreme_inds[40],lats,lons,var_s)
#rf = europe_diff_clim_map(s_extreme_inds[40],lats,lons,var_s,obs_climatology)
#rf = europe_map(o_extreme_inds[0],lats,lons,var_o)
#rf = europe_diff_clim_map(o_extreme_inds[0],lats,lons,var_o,obs_climatology)
#rf = europe_map(o_extreme_inds[1],lats,lons,var_o)
#rf = europe_diff_clim_map(o_extreme_inds[1],lats,lons,var_o,obs_climatology)
#rf = europe_map(o_extreme_inds[2],lats,lons,var_o)
#rf = europe_diff_clim_map(o_extreme_inds[2],lats,lons,var_o,obs_climatology)
#rf = europe_map(o_extreme_inds[3],lats,lons,var_o)
#rf = europe_diff_clim_map(o_extreme_inds[3],lats,lons,var_o,obs_climatology)
#rf = europe_map(o_extreme_inds[4],lats,lons,var_o)
#rf = europe_diff_clim_map(o_extreme_inds[4],lats,lons,var_o,obs_climatology)

plt.figure(1)
plt.scatter(rps,scen_year_max[0,0,:],marker='x',c='b')
plt.scatter(rps_o,scen_year_max_o[0,0,:],marker='+',c='r')
plt.xscale('log')

#for scen in range(0,5):
#        file_name = 'tas' + '_o' + model_name + '_' +  scen_names[scen] + '.mat'
#        loadmat1 = io.loadmat(file_name)
#        mat_var_name = 'tas' + '_s'        
#        tas = loadmat1[mat_var_name]
#        region_tas = hw_averager(tas,1,[0,896])
#        region_tas = array(list(flatten(region_tas)))
#        region_tas = region_tas - 273.15        
#        file_name = 'tdps' + '_o' + model_name + '_' +  scen_names[scen] + '.mat'        
#        loadmat1 = io.loadmat(file_name)
#        mat_var_name = 'tdps' + '_s'        
#        tdps = loadmat1[mat_var_name]  
#        region_tdps = hw_averager(tdps,1,[0,896])
#        region_tdps = array(list(flatten(region_tdps)))
#        region_tdps = region_tdps - 273.15
#        appt = -2.653 + (0.994*region_tas) + (0.0153*region_tdps*region_tdps)
#        appt_extremes = sorted(appt,reverse=True)
#        scen_appt_extremes_o[scen,:] = appt_extremes[0:1000]
        
plt.figure(2)
plt.scatter(rps_d,scen_heat_extremes[0,0,:],c='black',marker='x',label='1970-1999')
plt.scatter(rps_d,scen_heat_extremes[3,0,:],c='b',marker='x',label='2020-2049')
plt.scatter(rps_d,scen_heat_extremes[4,0,:],c='r',marker='x',label='2070-2099')
plt.scatter(rps_o_d,scen_heat_extremes_o[0,0,:],c='black')
plt.scatter(rps_o_d,scen_heat_extremes_o[3,0,:],c='b')
plt.scatter(rps_o_d,scen_heat_extremes_o[4,0,:],c='r')
plt.xscale('log')
plt.xlim(0.1,615)
plt.ylabel('Max temperature (C)')
plt.xlabel('Return period (years)')
plt.title('RCP 45')
plt.legend(loc=2,scatterpoints=1)

plt.figure(3)
plt.scatter(qq_o[0,0,:],qq_s[0,0,:],marker='x',c='black')
plt.plot([-10,30],[-10,30])

plt.figure(4)
plt.scatter(qq_o[1,0,:],qq_s[1,0,:],marker='x',c='black')
plt.plot([-10,30],[-10,30])

plt.figure(5)
plt.scatter(qq_o[2,0,:],qq_s[2,0,:],marker='x',c='black')
plt.plot([-10,30],[-10,30])

plt.figure(6)
plt.scatter(qq_o[3,0,:],qq_s[3,0,:],marker='x',c='black')
plt.plot([-10,30],[-10,30])

plt.figure(7)
plt.scatter(qq_o[4,0,:],qq_s[4,0,:],marker='x',c='black')
plt.plot([-2,32],[-2,32])


#plt.figure(2)
#plt.scatter(rps,scen_heat_extremes[0,0,:],c='black',marker='x',label='1970-1999')
#plt.scatter(rps,scen_heat_extremes[3,0,:],c='b',marker='x',label='2020-2049')
#plt.scatter(rps,scen_heat_extremes[4,0,:],c='r',marker='x',label='2070-2099')
#plt.xscale('log')
#plt.xlim(0,615)
#plt.ylabel('Max temperature (C)')
#plt.xlabel('Return period (years)')
#plt.title('RCP 85')
#plt.legend(loc=2,scatterpoints=1)
#
#plt.figure(3)
#plt.scatter(rps,scen_heat_extremes[0,1,:],c='black',marker='x',label='1970-1999')
#plt.scatter(rps,scen_heat_extremes[1,1,:],c='b',marker='x',label='2020-2049')
#plt.scatter(rps,scen_heat_extremes[2,1,:],c='r',marker='x',label='2070-2099')
#plt.scatter(rps_o,scen_heat_extremes_o[0,1,:],c='g')
#plt.scatter(rps_o,scen_heat_extremes_o[1,1,:],c='g')
#plt.scatter(rps_o,scen_heat_extremes_o[2,1,:],c='g')
#plt.xscale('log')
#plt.xlim(0,615)
#plt.ylabel('Min temperature (C)')
#plt.xlabel('Return period (years)')
#plt.title('RCP 45')
#plt.legend(loc=2,scatterpoints=1)
#
#plt.figure(4)
#plt.scatter(rps,scen_heat_extremes[0,1,:],c='black',marker='x',label='1970-1999')
#plt.scatter(rps,scen_heat_extremes[3,1,:],c='b',marker='x',label='2020-2049')
#plt.scatter(rps,scen_heat_extremes[4,1,:],c='r',marker='x',label='2070-2099')
#plt.xscale('log')
#plt.xlim(0,615)
#plt.ylabel('Min temperature (C)')
#plt.xlabel('Return period (years)')
#plt.title('RCP 85')
#plt.legend(loc=2,scatterpoints=1)
#
#plt.figure(5)
#plt.scatter(rps,scen_heat_extremes[0,2,:],c='black',marker='x',label='1970-1999')
#plt.scatter(rps,scen_heat_extremes[1,2,:],c='b',marker='x',label='2020-2049')
#plt.scatter(rps,scen_heat_extremes[2,2,:],c='r',marker='x',label='2070-2099')
#plt.xscale('log')
#plt.xlim(0,615)
#plt.ylabel('Mean temperature (C)')
#plt.xlabel('Return period (years)')
#plt.title('RCP 45')
#plt.legend(loc=2,scatterpoints=1)
#
#plt.figure(6)
#plt.scatter(rps,scen_heat_extremes[0,2,:],c='black',marker='x',label='1970-1999')
#plt.scatter(rps,scen_heat_extremes[3,2,:],c='b',marker='x',label='2020-2049')
#plt.scatter(rps,scen_heat_extremes[4,2,:],c='r',marker='x',label='2070-2099')
#plt.xscale('log')
#plt.xlim(0,615)
#plt.ylabel('Mean temperature (C)')
#plt.xlabel('Return period (years)')
#plt.title('RCP 85')
#plt.legend(loc=2,scatterpoints=1)
#
#plt.figure(7)
#plt.scatter(rps,scen_heat_extremes[0,3,:],c='black',marker='x',label='1970-1999')
#plt.scatter(rps,scen_heat_extremes[1,3,:],c='b',marker='x',label='2020-2049')
#plt.scatter(rps,scen_heat_extremes[2,3,:],c='r',marker='x',label='2070-2099')
#plt.xscale('log')
#plt.xlim(0,615)
#plt.ylabel('Dew point temperature (C)')
#plt.xlabel('Return period (years)')
#plt.title('RCP 45')
#plt.legend(loc=2,scatterpoints=1)
#
#plt.figure(8)
#plt.scatter(rps,scen_heat_extremes[0,3,:],c='black',marker='x',label='1970-1999')
#plt.scatter(rps,scen_heat_extremes[3,3,:],c='b',marker='x',label='2020-2049')
#plt.scatter(rps,scen_heat_extremes[4,3,:],c='r',marker='x',label='2070-2099')
#plt.xscale('log')
#plt.xlim(0,615)
#plt.ylabel('Dew point temperature (C)')
#plt.xlabel('Return period (years)')
#plt.title('RCP 85')
#plt.legend(loc=2,scatterpoints=1)
#
#plt.figure(9)
#plt.scatter(rps,scen_appt_extremes[0,:],c='black',marker='x',label='1970-1999')
#plt.scatter(rps,scen_appt_extremes[1,:],c='b',marker='x',label='2020-2049')
#plt.scatter(rps,scen_appt_extremes[2,:],c='r',marker='x',label='2070-2099')
#plt.scatter(rps_o,scen_appt_extremes_o[0,:],c='g')
#plt.scatter(rps_o,scen_appt_extremes_o[1,:],c='g')
#plt.scatter(rps_o,scen_appt_extremes_o[2,:],c='g')
#plt.xscale('log')
#plt.xlim(0,615)
#plt.ylabel('Apparent temperature (C)')
#plt.xlabel('Return period (years)')
#plt.title('RCP 45')
#plt.legend(loc=2,scatterpoints=1)
#
#plt.figure(10)
#plt.scatter(rps,scen_appt_extremes[0,:],c='black',marker='x',label='1970-1999')
#plt.scatter(rps,scen_appt_extremes[3,:],c='b',marker='x',label='2020-2049')
#plt.scatter(rps,scen_appt_extremes[4,:],c='r',marker='x',label='2070-2099')
#
#plt.xscale('log')
#plt.xlim(0,615)
#plt.ylabel('Apparent temperature (C)')
#plt.xlabel('Return period (years)')
#plt.title('RCP 85')
#plt.legend(loc=2,scatterpoints=1)

    