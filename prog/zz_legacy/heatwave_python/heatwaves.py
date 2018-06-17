# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:22:57 2016

@author: srh110
"""

import matplotlib.pyplot as plt
from os import chdir
import scipy.io as io

chdir('W:/srh110/MVAREOF/')

model_name = 'MPI'



scen_names = ['hist19701999','4520202049','4520702099']

wsdi_rvs = zeros((3,10000))
wsdi_obs_rvs = zeros((3,30))

for scen in range(0,2):
    file_name1 = 'WSDI_' + model_name + '_' + scen_names[scen] + '.mat'
    #file_name2 = 'WSDI_' + model_name + '_' + scen_names[scen] + '2.mat'
    file_name3 = 'WSDI_OBS' + model_name + '_' + scen_names[scen] + '.mat'
    
    loadmat1 = io.loadmat(file_name1)
    #loadmat2 = io.loadmat(file_name2)
    loadmat3 = io.loadmat(file_name3)
    
    mean_wsdi_sim = loadmat1['mean_wsdi_sim']
    #mean_wsdi_sim2 = loadmat2['mean_wsdi_sim']
    mean_wsdi_obs = loadmat3['mean_wsdi_obs']
    
#    #mean_wsdi_sim = zeros(10000)
#    #for i in range(0,10000):
#        mean_wsdi_sim[i] = mean_wsdi_sim1[i]
#    for j in range(0,5000):
#        mean_wsdi_sim[j+5000] = mean_wsdi_sim2[j]
        
    wsdi_rv = sorted(mean_wsdi_sim,reverse=True)
    wsdi_rvs[scen,:] = wsdi_rv
    
    wsdi_obs_rv = sorted(mean_wsdi_obs,reverse=True)
    wsdi_obs_rvs[scen,:] = wsdi_obs_rv
    
wsdi_rp = zeros(10000)
for i in range(0,10000):
    wsdi_rp[i] = 10000.0/(i+1)
    
wsdi_rp_obs = zeros(30)
for i in range(0,30):
    wsdi_rp_obs[i] = 30.0/(i+1)
    
plt.figure(1)
plt.scatter(wsdi_rp,wsdi_rvs[0,:],c='black',marker='x',label='1970 - 1999')
plt.scatter(wsdi_rp,wsdi_rvs[1,:],c='green',marker='x',label='2020 - 2049')
#plt.scatter(wsdi_rp,wsdi_rvs[2,:],c='red',marker='x',label='2070 - 2099')
plt.xscale('log')
plot_title = model_name + ' ' + 'RCP 4.5'
plt.title(plot_title)
plt.ylim((0,160))
plt.xlim((0,1000))
plt.ylabel('Warm Spell Duration Index (days)')
plt.xlabel('Return period (years)')
plt.legend(fontsize = 14, handletextpad = 0.4, handlelength = 1, scatterpoints=1, loc=2)

savefig_name = model_name + '_' + '45.png'

plt.savefig(savefig_name)

plt.figure(2)
plt.scatter(wsdi_rp_obs,wsdi_obs_rvs[0,:],c='purple',marker='+')
plt.scatter(wsdi_rp_obs,wsdi_obs_rvs[1,:],c='yellow',marker='+')
#plt.scatter(wsdi_rp_obs,wsdi_obs_rvs[2,:],c='blue',marker='+')
plt.xscale('log')

plt.figure(5)
plt.scatter(wsdi_rp,wsdi_rvs[0,:],c='black',marker='x',label='1970 - 1999')
plt.scatter(wsdi_rp_obs,wsdi_obs_rvs[0,:],c='purple',marker='+')
plt.xscale('log')
plt.xlim((0,1000))

plt.figure(6)
plt.scatter(wsdi_rp,wsdi_rvs[1,:],c='black',marker='x',label='1970 - 1999')
plt.scatter(wsdi_rp_obs,wsdi_obs_rvs[1,:],c='purple',marker='+')
plt.xscale('log')
plt.xlim((0,1000))

#scen_names = ['hist19701999','8520202049','8520702099']
#
#wsdi_rvs = zeros((3,10000))
#
#for scen in range(0,3):
#    file_name1 = 'WSDI_' + model_name + '_' + scen_names[scen] + '1.mat'
#    file_name2 = 'WSDI_' + model_name + '_' + scen_names[scen] + '2.mat'
#    file_name3 = 'WSDI_OBS' + model_name + '_' + scen_names[scen] + '.mat'
#    
#    loadmat1 = io.loadmat(file_name1)
#    loadmat2 = io.loadmat(file_name2)
#    loadmat3 = io.loadmat(file_name3)
#    
#    mean_wsdi_sim1 = loadmat1['mean_wsdi_sim']
#    mean_wsdi_sim2 = loadmat2['mean_wsdi_sim']
#    mean_wsdi_obs = loadmat3['mean_wsdi_obs']
#    
#    mean_wsdi_sim = zeros(10000)
#    for i in range(0,5000):
#        mean_wsdi_sim[i] = mean_wsdi_sim1[i]
#    for j in range(0,5000):
#        mean_wsdi_sim[j+5000] = mean_wsdi_sim2[j]
#        
#    wsdi_rv = sorted(mean_wsdi_sim,reverse=True)
#    wsdi_rvs[scen,:] = wsdi_rv
#    
#    wsdi_obs_rv = sorted(mean_wsdi_obs,reverse=True)
#    wsdi_obs_rvs[scen,:] = wsdi_obs_rv
#    
#    
#
#    
#plt.figure(3)
#plt.scatter(wsdi_rp,wsdi_rvs[0,:],c='black',marker='x',label='1970 - 1999')
#plt.scatter(wsdi_rp,wsdi_rvs[1,:],c='green',marker='x',label='2020 - 2049')
##plt.scatter(wsdi_rp,wsdi_rvs[2,:],c='red',marker='x',label='2070 - 2099')
#plt.xscale('log')
#plot_title = model_name + ' ' + 'RCP 8.5'
#plt.title(plot_title)
#plt.ylim((0,160))
#plt.xlim((0,1000))
#plt.ylabel('Warm Spell Duration Index (days)')
#plt.xlabel('Return period (years)')
#plt.legend(fontsize = 14, handletextpad = 0.4, handlelength = 1, scatterpoints=1, loc=2)
#
#
#savefig_name = model_name + '_' + '85.png'
#
#plt.savefig(savefig_name)
#
#plt.figure(4)
#plt.scatter(wsdi_rp_obs,wsdi_obs_rvs[0,:],c='purple',marker='+')
#plt.scatter(wsdi_rp_obs,wsdi_obs_rvs[1,:],c='yellow',marker='+')
##plt.scatter(wsdi_rp_obs,wsdi_obs_rvs[2,:],c='blue',marker='+')
#plt.xscale('log')
#
