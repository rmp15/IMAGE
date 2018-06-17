# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 16:36:50 2017

@author: srh110
"""

import numpy as np
import matplotlib.pyplot as plt

def ensemble_cut(var_s,mem_len):    
    var_s_shape = np.shape(var_s)    
    no_years_s = var_s_shape[1]
    no_sim_ens_mems = int(np.floor(no_years_s/mem_len))
    var_s_ens = np.zeros((no_sim_ens_mems,var_s_shape[0],mem_len))
    for em in range(0,no_sim_ens_mems):
        var_s_ens[em,:,:] = var_s[:,(em*mem_len):((em+1)*mem_len)]
    return var_s_ens
    
def rp_rv_fig_ens(fig_no,rp_o,rv_o,rp_s,rv_s_ens,scol):
    no_ens = int(np.shape(rv_s_ens)[0])
    plt.figure(fig_no)
    for i in range(no_ens):
        if i == 0:
            plt.plot(rp_s,rv_s_ens[i,:],c='black',label='Sim')
        else:
            plt.plot(rp_s,rv_s_ens[i,:],c='black')
    plt.plot(rp_o,rv_o,c='',label='Obs')

    plt.xscale('log')
    plt.xlabel('Return period (years)')
    
    plt.legend(loc=2)
    
def rp_rv_fig_pot_ens(fig_no,rp_o,rv_o,rp_s_ens,rv_s_ens):
    no_ens = len(rp_s_ens)
    plt.figure(fig_no)
    for i in range(no_ens):
        if i == 0:
            plt.plot(rp_s_ens[i],rv_s_ens[i],c='black',label='Sim')
        else:
            plt.plot(rp_s_ens[i],rv_s_ens[i],c='black')
    plt.plot(rp_o,rv_o,c='blue',label='Obs')
    
    
    plt.xscale('log')
    plt.xlabel('Return period (years)')
    plt.legend(loc=2)