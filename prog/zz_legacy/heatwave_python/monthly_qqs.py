# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 11:39:37 2017

@author: srh110
"""

from load_mat_var import load_mat_var
from monthly_climatology import monthly_pctile, monthly_data
from europe_map import europe_hw_map
import numpy as np
import matplotlib.pyplot as plt
import os

os.chdir('W:/srh110/ntsp_test')

model_name = 'MPI'
scen_names = ['hist19701999','4520202049','4520702099','8520202049','8520702099']
var_names = ['tasmax','tasmin','tas','tdps']

var_name = var_names[0]
scen_name = scen_names[0]



var_o = load_mat_var(var_name,model_name,scen_name,'o')
var_o_shape = np.ma.shape(var_o)
o_years = var_o_shape[1]
no_sites = var_o_shape[2]
print('var loaded')
var_s = load_mat_var(var_name,model_name,scen_name,'s')
var_s_shape = np.ma.shape(var_s)
s_years = var_s_shape[1]
print('var loaded')

o_monthly_data = monthly_data(var_o)
s_monthly_data = monthly_data(var_s)

monthly_qqs = zeros((2,12,99,no_sites))

for month in range(0,12):
    o_data = o_monthly_data[month]
    s_data = s_monthly_data[month]
    for site in range(0,no_sites):
        print(site)
        for p in range(1,100):
            monthly_qqs[0,month,p-1,site] = np.percentile(o_data[:,site],p)
            monthly_qqs[1,month,p-1,site] = np.percentile(s_data[:,site],p)

site = 4

for m in range(0,12):
    plt.subplot(3,4,m+1)            
    plt.scatter(monthly_qqs[0,m,:,site],monthly_qqs[1,m,:,site],marker='x',c='b')
    plt.plot([min(monthly_qqs[0,m,:,site]),max(monthly_qqs[0,m,:,site])],[min(monthly_qqs[0,m,:,site]),max(monthly_qqs[0,m,:,site])],c='black')
#plt.subplot(342)
#plt.scatter(monthly_qqs[0,1,:,0],monthly_qqs[1,1,:,0])
#plt.plot([min(monthly_qqs[0,1,:,0]),max(monthly_qqs[0,1,:,0])],[min(monthly_qqs[0,1,:,0]),max(monthly_qqs[0,1,:,0])])
#plt.subplot(343)            
#plt.scatter(monthly_qqs[0,2,:,0],monthly_qqs[1,2,:,0])
#plt.subplot(344)
#plt.scatter(monthly_qqs[0,3,:,0],monthly_qqs[1,3,:,0])
#plt.subplot(345)            
#plt.scatter(monthly_qqs[0,4,:,0],monthly_qqs[1,4,:,0])
#plt.subplot(346)
#plt.scatter(monthly_qqs[0,5,:,0],monthly_qqs[1,5,:,0])
#plt.subplot(347)            
#plt.scatter(monthly_qqs[0,6,:,0],monthly_qqs[1,6,:,0])
#plt.subplot(348)
#plt.scatter(monthly_qqs[0,7,:,0],monthly_qqs[1,7,:,0])
#plt.subplot(349)            
#plt.scatter(monthly_qqs[0,8,:,0],monthly_qqs[1,8,:,0])
#plt.subplot(3,4,10)
#plt.scatter(monthly_qqs[0,9,:,0],monthly_qqs[1,9,:,0])
#plt.subplot(3,4,11)            
#plt.scatter(monthly_qqs[0,10,:,0],monthly_qqs[1,10,:,0])
#plt.subplot(3,4,12)
#plt.scatter(monthly_qqs[0,11,:,0],monthly_qqs[1,11,:,0])