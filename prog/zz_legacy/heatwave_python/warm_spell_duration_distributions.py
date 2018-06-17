# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 12:58:33 2016

@author: srh110
"""
import matplotlib.pyplot as plt
from os import chdir
import scipy.io as io

chdir('W:/srh110/Danube_Demonstrator_Outputs/')

file_name1 = 'y_sim_s.mat'
file_name2 = 'y_obs_s.mat'


loadmat1 = io.loadmat(file_name1)
loadmat2 = io.loadmat(file_name2)

ys_sim_s = loadmat1['ys_sim_s']
ys_obs_i = loadmat2['ys_obs_i']

y_sim = zeros(100)
y_obs = zeros(100)
for i in range(0,100):
    y_sim[i] = ys_sim_s[0,0,i]
    y_obs[i] = ys_obs_i[0,0,i]

plt.figure(1)
plt.plot(y_sim,c='b')    
plt.plot(y_obs,c='r')