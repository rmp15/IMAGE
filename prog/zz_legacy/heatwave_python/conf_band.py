# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 14:41:27 2017

@author: srh110
"""

import numpy as np
import itertools as it
import scipy.stats as ss
import matplotlib.pyplot as plt


def gen_gev_pdf(param1,param2,param3):

    t = np.zeros(500)
    pdf = np.zeros(500)
    
    for i in range(0,500):
        temp = 20 + ((65/500)*i)
        t[i] = temp
        pdf[i] = ss.genextreme.cdf(temp,param1,param2,param3)
        
    return t, pdf

def gen_gpd_pdf(param1,param2,param3):

    t = np.zeros(200)
    pdf = np.zeros(200)
    
    for i in range(0,200):
        temp = -5 + ((25/200)*i)
        t[i] = temp
        pdf[i] = ss.genpareto.cdf(temp,param1,param2,param3)
        
    return t, pdf

#corner_pdfs = np.zeros((8,200))
#count = 0
#    
#for i in range(2):
#    for j in range(2):
#        for k in range(2):
#            temps, corner_pdfs[count,:] = gen_gev_pdf(boot_params[i,0],boot_params[j,1],boot_params[k,2])
#            count += 1
#            
#plt.figure(1)
#for i in range(8):
#    plt.plot(temps,corner_pdfs[i,:])
#    
#max_band = np.zeros(200)
#min_band = np.zeros(200)
#
#for i in range(0,200):
#    max_band[i] = np.max(corner_pdfs[:,i])
#    min_band[i] = np.min(corner_pdfs[:,i])
#    
#plt.plot(temps,max_band,c='black')
#plt.plot(temps,min_band,c='black')
#
#rp_max = np.zeros(200)
#rp_min = np.zeros(200)
#
#for i in range(200):
#    rp_max[i] = (1 / (1-max_band[i]))
#    rp_min[i] = (1 / (1-min_band[i]))
#
#plt.figure(3)    
#plt.plot(rp_min,temps,c='black')
#plt.plot(rp_max,temps,c='black')
#plt.xlim(0.5,30)
#plt.xscale('log')
#plt.ylim(22,47)

def ci_gev_band_sphere(o_fit_params,boot_params,min_s_rp,max_s_rp,col):

    sphere_pdfs = np.zeros((26,500))
    count = 0
    
    #one extreme and two ML
    for i in range(2):
        temps, sphere_pdfs[count,:] = gen_gev_pdf(boot_params[i,0],o_fit_params[1],o_fit_params[2])
        count += 1
        temps, sphere_pdfs[count,:] = gen_gev_pdf(o_fit_params[0],boot_params[i,1],o_fit_params[2])
        count += 1
        temps, sphere_pdfs[count,:] = gen_gev_pdf(o_fit_params[0],o_fit_params[1],boot_params[i,2])
        count += 1
    
    #two extreme and one ML
    param_distances = np.zeros((2,3))
    for i in range(2):
        param_distances[i,:] = boot_params[i,:] - o_fit_params
    
    
    root2_distances = np.zeros((3,3))
    root2_distances[0,:] = o_fit_params
    root2_distances[1,:] = o_fit_params + (0.707*param_distances[0,:])
    root2_distances[2,:] = o_fit_params + (0.707*param_distances[1,:])
    
    temps, sphere_pdfs[count,:] = gen_gev_pdf(root2_distances[0,0],root2_distances[1,1],root2_distances[1,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gev_pdf(root2_distances[0,0],root2_distances[1,1],root2_distances[2,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gev_pdf(root2_distances[0,0],root2_distances[2,1],root2_distances[1,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gev_pdf(root2_distances[0,0],root2_distances[2,1],root2_distances[2,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gev_pdf(root2_distances[1,0],root2_distances[0,1],root2_distances[1,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gev_pdf(root2_distances[1,0],root2_distances[0,1],root2_distances[2,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gev_pdf(root2_distances[2,0],root2_distances[0,1],root2_distances[1,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gev_pdf(root2_distances[2,0],root2_distances[0,1],root2_distances[2,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gev_pdf(root2_distances[1,0],root2_distances[1,1],root2_distances[0,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gev_pdf(root2_distances[1,0],root2_distances[2,1],root2_distances[0,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gev_pdf(root2_distances[2,0],root2_distances[1,1],root2_distances[0,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gev_pdf(root2_distances[2,0],root2_distances[2,1],root2_distances[0,2])        
    count += 1
    
    
    
    root3_distances = np.zeros((2,3))
    root3_distances[0,:] = o_fit_params + (0.577*param_distances[0,:])
    root3_distances[1,:] = o_fit_params + (0.577*param_distances[1,:])
    
    for i in range(2):
        for j in range(2):
            for k in range(2):
                temps, sphere_pdfs[count,:] = gen_gev_pdf(root3_distances[i,0],root3_distances[j,1],root3_distances[k,2])        
                count += 1
        
    #plt.figure(4)
    #for i in range(18):
    #    plt.plot(temps,sphere_pdfs[i,:])
        
    max_band = np.zeros(500)
    min_band = np.zeros(500)
    
    for i in range(0,500):
        max_band[i] = np.max(sphere_pdfs[:,i])
        min_band[i] = np.min(sphere_pdfs[:,i])
        

    
    rp_max = np.zeros(500)
    rp_min = np.zeros(500)
    
    for i in range(500):
        rp_max[i] = (1 / (1-max_band[i]))
        rp_min[i] = (1 / (1-min_band[i]))
    
    rp_diff = np.abs(rp_min - max_s_rp)

    ymax = temps[rp_diff.argmin()] 
    
    
    rp_diff2 = np.abs(rp_max - (min_s_rp*1.02))
    ymin = temps[rp_diff2.argmin()]
    
    #plt.figure(3)    
    plt.plot(rp_min,temps,c=col)
    plt.plot(rp_max,temps,c=col)
    
    plt.xscale('log')

    plt.ylim(ymin,ymax)
    return ymin, ymax

def ci_gpd_band_sphere(o_fit_params,boot_params,min_s_rp,max_s_rp,opt_thresh,rp_scaler):

    sphere_pdfs = np.zeros((26,200))
    count = 0
    
    #one extreme and two ML
    for i in range(2):
        temps, sphere_pdfs[count,:] = gen_gpd_pdf(boot_params[i,0],o_fit_params[1],o_fit_params[2])
        count += 1
        temps, sphere_pdfs[count,:] = gen_gpd_pdf(o_fit_params[0],boot_params[i,1],o_fit_params[2])
        count += 1
        temps, sphere_pdfs[count,:] = gen_gpd_pdf(o_fit_params[0],o_fit_params[1],boot_params[i,2])
        count += 1
    
    #two extreme and one ML
    param_distances = np.zeros((2,3))
    for i in range(2):
        param_distances[i,:] = boot_params[i,:] - o_fit_params
    
    
    root2_distances = np.zeros((3,3))
    root2_distances[0,:] = o_fit_params
    root2_distances[1,:] = o_fit_params + (0.707*param_distances[0,:])
    root2_distances[2,:] = o_fit_params + (0.707*param_distances[1,:])
    
    temps, sphere_pdfs[count,:] = gen_gpd_pdf(root2_distances[0,0],root2_distances[1,1],root2_distances[1,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gpd_pdf(root2_distances[0,0],root2_distances[1,1],root2_distances[2,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gpd_pdf(root2_distances[0,0],root2_distances[2,1],root2_distances[1,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gpd_pdf(root2_distances[0,0],root2_distances[2,1],root2_distances[2,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gpd_pdf(root2_distances[1,0],root2_distances[0,1],root2_distances[1,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gpd_pdf(root2_distances[1,0],root2_distances[0,1],root2_distances[2,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gpd_pdf(root2_distances[2,0],root2_distances[0,1],root2_distances[1,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gpd_pdf(root2_distances[2,0],root2_distances[0,1],root2_distances[2,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gpd_pdf(root2_distances[1,0],root2_distances[1,1],root2_distances[0,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gpd_pdf(root2_distances[1,0],root2_distances[2,1],root2_distances[0,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gpd_pdf(root2_distances[2,0],root2_distances[1,1],root2_distances[0,2])
    count += 1
    temps, sphere_pdfs[count,:] = gen_gpd_pdf(root2_distances[2,0],root2_distances[2,1],root2_distances[0,2])        
    count += 1
    
    
    
    root3_distances = np.zeros((2,3))
    root3_distances[0,:] = o_fit_params + (0.577*param_distances[0,:])
    root3_distances[1,:] = o_fit_params + (0.577*param_distances[1,:])
    
    for i in range(2):
        for j in range(2):
            for k in range(2):
                temps, sphere_pdfs[count,:] = gen_gpd_pdf(root3_distances[i,0],root3_distances[j,1],root3_distances[k,2])        
                count += 1
        
#    plt.figure(4)
#    for i in range(26):
#        plt.plot(temps,sphere_pdfs[i,:])
        
    max_band = np.zeros(200)
    min_band = np.zeros(200)
    
    for i in range(0,200):
        max_band[i] = np.max(sphere_pdfs[:,i])
        min_band[i] = np.min(sphere_pdfs[:,i])
        

    
    rp_max = np.zeros(200)
    rp_min = np.zeros(200)
    
    for i in range(200):
        rp_max[i] = (1 / (1-max_band[i])) / rp_scaler
        rp_min[i] = (1 / (1-min_band[i])) / rp_scaler

    rp_diff = np.abs(rp_min - max_s_rp)

    ymax = temps[rp_diff.argmin()] + opt_thresh
    
    
    rp_diff2 = np.abs(rp_max - (min_s_rp*1.02))
    ymin = temps[rp_diff2.argmin()] + opt_thresh
    
    #plt.figure(3)    
    plt.plot(rp_min,temps+opt_thresh,c='black')
    plt.plot(rp_max,temps+opt_thresh,c='black')
    
    plt.xscale('log')    
    
    plt.ylim(ymin,ymax)