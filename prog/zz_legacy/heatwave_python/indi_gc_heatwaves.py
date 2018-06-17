# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 11:12:23 2016

@author: srh110
"""

import matplotlib.pyplot as plt
from os import chdir
import scipy.io as io

chdir('W:/srh110/MVAREOF/')

wsdi_rvs = zeros((10000))
wsdi_obs_rvs = zeros((30))


file_name1 = 'WSDI_MPI_hist19701999indi_gc.mat'
file_name2 = 'WSDI_OBSMPI_hist19701999indi_gc.mat'


loadmat1 = io.loadmat(file_name1)
loadmat2 = io.loadmat(file_name2)
loadmat3 = io.loadmat(file_name3)

wsdi_sim = loadmat1['wsdi_sim']
wsdi_obs = loadmat2['wsdi_obs']

gc = 998
    
wsdi_rv = sorted(wsdi_sim[:,gc],reverse=True)
wsdi_rvs = wsdi_rv

wsdi_obs_rv = sorted(wsdi_obs[:,gc],reverse=True)
wsdi_obs_rvs = wsdi_obs_rv

wsdi_rp = zeros(10000)
for i in range(0,10000):
    wsdi_rp[i] = 10000.0/(i+1)
    
wsdi_rp_obs = zeros(30)
for i in range(0,30):
    wsdi_rp_obs[i] = 30.0/(i+1)
    
plt.figure(1)
plt.scatter(wsdi_rp,wsdi_rvs[:],c='black',marker='x')

plt.xscale('log')
plot_title = model_name + ' ' + 'RCP 4.5'
plt.title(plot_title)

plt.xlim((0,1000))
plt.ylabel('Warm Spell Duration Index (days)')
plt.xlabel('Return period (years)')
#plt.legend(fontsize = 14, handletextpad = 0.4, handlelength = 1, scatterpoints=1, loc=2)

savefig_name = model_name + '_' + '45.png'



plt.figure(1)
plt.scatter(wsdi_rp_obs,wsdi_obs_rvs[:],c='red',marker='+')

plt.xscale('log')