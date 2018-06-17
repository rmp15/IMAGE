# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 16:01:45 2017

@author: srh110
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from country_borders import country_polygon, country_only_points
import os
from load_mat_var import load_mat_input_var
from conf_band import ci_gev_band_sphere, ci_gpd_band_sphere
import scipy.stats as ss
import scikits.bootstrap as boot
from peak_ot import pot_rp_rv, pot_rp_rv_fixed_thresh
from ensemble_cut import rp_rv_fig_pot_ens
#from shapely.geometry import Polygon, MultiPoint

#var_o = np.random.uniform(265,320,(365,30,896))
#var_s = np.random.uniform(265,320,(365,600,896))
gcs = 'all'

def gc_dmv(var,gcs):
    var_shape = np.shape(var)
    days_py = var_shape[0]
    no_years = var_shape[1]
    
    if gcs == 'all':
        var_cut = var
        daily_mean_var = np.mean(var_cut,axis=2)
    elif gcs == 'none':
        daily_mean_var = var
    elif isinstance(gcs, str):
        try:
            c_poly = country_polygon(gcs)
            os.chdir('W:/srh110/CORDEX_europe_heatwave_input')
            lats = load_mat_input_var('eh_lats2.mat','eh_lats')
            lons = load_mat_input_var('eh_lons2.mat','eh_lons')
            gcs = country_only_points(lats,lons,c_poly)
            var_cut = np.zeros((days_py,no_years,np.size(gcs)))
            for i in range(np.size(gcs)):
                var_cut[:,:,i] = var[:,:,gcs[i]]
            var_cut = (var_cut-273.15) * 100
            daily_mean_var = np.mean(var_cut,axis=2,dtype=np.float32)
            daily_mean_var = np.int16(daily_mean_var)
        except IndexError:
            print('Invalid Entry: try all, none or country name')
    elif np.size(gcs) == 1:
        var_cut = var[:,:,gcs]
        daily_mean_var = np.squeeze(var_cut)
    else:
        var_cut = np.zeros((days_py,no_years,np.size(gcs)))
        for i in range(np.size(gcs)):
            var_cut[:,:,i] = var[:,:,gcs[i]]
        daily_mean_var = np.mean(var_cut,axis=2)

    return daily_mean_var

def gc_max_pos(var,gcs):
    var_shape = np.shape(var)
    days_py = var_shape[0]
    no_years = var_shape[1]
    
    if gcs == 'all':
        var_cut = var
        site_maxes = np.amax(np.amax(var_cut,axis=0),axis=0)
        daily_mean_var = np.mean(site_maxes)
    elif gcs == 'none':
        daily_mean_var = var
    elif isinstance(gcs, str):
        try:
            c_poly = country_polygon(gcs)
            os.chdir('W:/srh110/CORDEX_europe_heatwave_input')
            lats = load_mat_input_var('eh_lats2.mat','eh_lats')
            lons = load_mat_input_var('eh_lons2.mat','eh_lons')
            gcs = country_only_points(lats,lons,c_poly)
            var_cut = np.zeros((days_py,no_years,np.size(gcs)))
            for i in range(np.size(gcs)):
                var_cut[:,:,i] = var[:,:,gcs[i]]
            site_maxes = np.amax(np.amax(var_cut,axis=0),axis=0)
            daily_mean_var = np.mean(site_maxes)
        except IndexError:
            print('Invalid Entry: try all, none or country name')
    elif np.size(gcs) == 1:
        var_cut = var[:,:,gcs]
        site_maxes = np.amax(np.amax(var_cut,axis=0),axis=0)
        daily_mean_var = np.mean(site_maxes)
    else:
        var_cut = np.zeros((days_py,no_years,np.size(gcs)))
        for i in range(np.size(gcs)):
            var_cut[:,:,i] = var[:,:,gcs[i]]
        site_maxes = np.amax(np.amax(var_cut,axis=0),axis=0)
        daily_mean_var = np.mean(site_maxes)

    return daily_mean_var    

def rp_rv_fig_ens(fig_no,rp_o,rv_o,rp_s,rv_s_ens,scol='red'):
    no_ens = int(np.shape(rv_s_ens)[0])
    plt.figure(fig_no)
    for i in range(no_ens):
        if i == 0:
            plt.plot(rp_s,rv_s_ens[i,:],c=scol,label='Sim')
        else:
            plt.plot(rp_s,rv_s_ens[i,:],c=scol)
    plt.plot(rp_o,rv_o,c='black',label='Obs')
    
    plt.xscale('log')
    plt.xlabel('Return period (years)')
    plt.legend(loc=2)
    

def rp_rv(daily_mean_var):

#    var_shape = np.shape(var)
#    days_py = var_shape[0]
#    no_years = var_shape[1]
#    
#    if gcs == 'all':
#        var_cut = var
#        daily_mean_var = np.mean(var_cut,axis=2)
#    elif gcs == 'none':
#        daily_mean_var = var
#    elif np.size(gcs) == 1:
#        var_cut = var[:,:,gcs]
#        daily_mean_var = np.squeeze(var_cut)
#    else:
#        var_cut = np.zeros((days_py,no_years,np.size(gcs)))
#        for i in range(np.size(gcs)):
#            var_cut[:,:,i] = var[:,:,gcs[i]]
#        daily_mean_var = np.mean(var_cut,axis=2)

    
    dmv_flat = np.ndarray.flatten(daily_mean_var,order='F')
    dmv_flat = dmv_flat - 273.15
    dmv_sorted = sorted(dmv_flat,reverse=True)
    dmv_inds = [p[0] for p in sorted(enumerate(dmv_flat), key=lambda x:-x[1])]
    no_vals = no_years * 2
    rp = np.zeros(no_vals)
    rv = dmv_sorted[0:no_vals]
    for i in range(0,no_vals):
        rp[i] = no_years / (i+1)
    ex_inds = dmv_inds[0:no_vals]
    ex_y_d = np.zeros((no_vals,2))
    for i in range(0,no_vals):
        ex_y_d[i,0] = np.floor(ex_inds[i] / 365.0)
        ex_y_d[i,1] = ex_inds[i] % 365
        
    return rp, rv, ex_y_d
    
def rp_rv_fig(fig_no,rp_o,rv_o,rp_s,rv_s):
    plt.figure(fig_no)
    plt.scatter(rp_s,rv_s,marker='x',c='red',label='Sim')
    plt.scatter(rp_o,rv_o,marker='x',c='blue',label='Obs')
    
    plt.xscale('log')
    plt.xlabel('Return period (years)')
    plt.legend(loc=2,scatterpoints=1)
    
def md_rp_rv(var,gcs,no_days):
    var_shape = np.shape(var)
    days_py = var_shape[0]
    no_years = var_shape[1]
    no_sites = var_shape[2]
    
    if gcs == 'all':
        var_cut = var
        daily_mean_var = np.mean(var_cut,axis=2)
    elif gcs == 'none':
        daily_mean_var = var
    elif np.size(gcs) == 1:
        var_cut = var[:,:,gcs]
        daily_mean_var = np.squeeze(var_cut)
    else:
        var_cut = np.zeros((days_py,no_years,np.size(gcs)))
        for i in range(np.size(gcs)):
            var_cut[:,:,i] = var[:,:,gcs[i]]
        daily_mean_var = np.mean(var_cut,axis=2)
    
    no_vals = no_years * 2
    rp = np.zeros(no_vals)
    rv = np.zeros(no_vals)
    for i in range(0,no_vals):
        rp[i] = no_years / (i+1)
    
    
    var_flat = np.ndarray.flatten(daily_mean_var,order='F')
    var_flat = var_flat - 273.15
    x_day_tots = np.zeros(np.size(var_flat)+1-no_days)
    for i in range(np.size(x_day_tots)):
        x_day_tots[i] = np.mean(var_flat[i:i+no_days])
    for j in range(no_vals):
        rv[j] = max(x_day_tots)
        max_ind = np.where(x_day_tots==rv[j])[0][0]
        x_day_tots = np.delete(x_day_tots,range(max_ind+1-no_days,max_ind+no_days))

            
    
    return rp, rv
    
    
    
def md_rp_rv_annmax(var,no_days):
    var_shape = np.shape(var)
    days_py = var_shape[0]
    no_years = var_shape[1]
    
    

    
    no_vals = no_years
    rp = np.zeros(no_vals)
    rv = np.zeros(no_vals)
    max_ind = np.zeros(no_vals)
    max_ind_sorted = np.zeros((no_vals,2))
    for i in range(0,no_vals):
        rp[i] = no_years / (i+1)
    
    
    for y in range(0,no_years):
        var_flat = var[:,y]
        var_flat = var_flat - 273.15
        x_day_tots = np.zeros(np.size(var_flat)+1-no_days)
        for i in range(np.size(x_day_tots)):
            x_day_tots[i] = np.mean(var_flat[i:i+no_days])
        
        rv[y] = max(x_day_tots)
        
        max_ind[y] = np.where(x_day_tots==rv[y])[0][0]
        #x_day_tots = np.delete(x_day_tots,range(max_ind+1-no_days,max_ind+no_days))
    y_sorted = [y[0] for y in sorted(enumerate(rv),key=lambda x:x[1],reverse=True)]
    rv = sorted(rv, reverse=True)
    for y in range(0,no_years):
        max_ind_sorted[y,0] = y_sorted[y]
        max_ind_sorted[y,1] = max_ind[y_sorted[y]]        
    
    return rp, rv, max_ind_sorted

def extrapolate_obs(fit_params,method,col,ot=0,rps=1):
    if method == 'AnnMax':
        t = np.zeros(500)
        pdf = np.zeros(500)
    
        for i in range(0,500):
            temp = 20 + ((55/500)*i)
            t[i] = temp
            pdf[i] = ss.genextreme.cdf(temp,fit_params[0],fit_params[1],fit_params[2])
            
        rp_fit = np.zeros(500)
    
        for i in range(500):
            rp_fit[i] = (1 / (1-pdf[i]))
        plt.plot(rp_fit,t,linestyle='--',c=col)
    if method == 'POT':
        t = np.zeros(500)
        pdf = np.zeros(500)
    
        for i in range(0,500):
            temp = 20 + ((55/500)*i)
            t[i] = temp
            pdf[i] = ss.genpareto.cdf(temp-ot,fit_params[0],fit_params[1],fit_params[2])
            
        rp_fit = np.zeros(500)
    
        for i in range(500):
            rp_fit[i] = (1 / (1-pdf[i])) / rps
        plt.plot(rp_fit,t,linestyle='--',c=col)

def make_figure(method,o_data,s_data,no_days,fig_c,cbands=True,extrap_obs=True,time_thresh=-1,no_events_desired=100,scol='red'):
    if method == 'AnnMax':
        rp_o, rv_o, o_annmax_inds = md_rp_rv_annmax(o_data,no_days)
        no_s_ens = np.shape(s_data)[0]
        rv_s_ens = np.zeros((no_s_ens,np.shape(s_data)[2]))
        annmax_inds = np.zeros((no_s_ens,np.shape(s_data)[2],2))
        for i in range(no_s_ens):
            rp_s, rv_s_ens[i,:], annmax_inds[i,:,:] = md_rp_rv_annmax(s_data[i,:,:],no_days)
        rp_rv_fig_ens(fig_c,rp_o,rv_o,rp_s,rv_s_ens,scol)
        o_fit_params = ss.genextreme.fit(rv_o)
        if extrap_obs==True:
            extrapolate_obs(o_fit_params,method,'black')
        if cbands == True:
            boot_params = boot.ci(rv_o,ss.genextreme.fit,n_samples=1000)
            ymin, ymax = ci_gev_band_sphere(o_fit_params,boot_params,rp_s[-1],rp_s[0],'black')
            plt.ylim(ymin,ymax)
        if no_s_ens == 1:
            s_fit_params = ss.genextreme.fit(rv_s_ens[0,:])
            boot_params_s = boot.ci(rv_s_ens[0,:],ss.genextreme.fit,n_samples=1000)
            _,_ = ci_gev_band_sphere(s_fit_params,boot_params_s,rp_s[-1],rp_s[0],scol)
            extrapolate_obs(s_fit_params,method,scol)
        plt.xlim(rp_s[-1],rp_s[0])
        return annmax_inds
        
    if method == 'POT':
        rp_o, rv_o, opt_thresh = pot_rp_rv(o_data,no_days,time_thresh,no_events_desired)
        no_s_ens = np.shape(s_data)[0]
        rp_pot_s_ens = {}
        rv_pot_s_ens = {}
        for i in range(no_s_ens):
            rp_pot_s_ens[i], rv_pot_s_ens[i], rv_pot_ = pot_rp_rv_fixed_thresh(s_data[i,:,:],no_days,time_thresh,opt_thresh)
        rp_rv_fig_pot_ens(fig_c,rp_o,rv_o,rp_pot_s_ens,rv_pot_s_ens)
        rv_pot_fit = rv_o - opt_thresh
        o_fit_params = ss.genpareto.fit(rv_pot_fit)
        if cbands == True:
            boot_params = boot.ci(rv_pot_fit,ss.genpareto.fit,n_samples=1000)
            rp_scaler = np.size(rv_o) / rp_o[0]
            ci_gpd_band_sphere(o_fit_params,boot_params,rp_o[-1],rp_pot_s_ens[0][0],opt_thresh,rp_scaler)  
        if extrap_obs==True:
            extrapolate_obs(o_fit_params,method,ot=opt_thresh,rps=rp_scaler)
        plt.xlim(rp_o[-1],rp_pot_s_ens[0][0])
        return annmax_inds
    
            
def make_label(method,var_name,model_name,scen_name,no_days,gridcells):
    if method == 'AnnMax':
        method_name = 'Annual maximum'
    if method == 'POT':
        method_name = 'Peak over threshold'
    if var_name == 'tasmax':
        formal_var_name = "$T_{max}$"
        unit = "$ (^oC)$"
    label = method_name + ' mean ' + str(no_days) + ' day ' + formal_var_name + ' across ' + gridcells + unit
    plt.ylabel(label)

def rp_event_calculator(rp,rv,rp_event_val):
    rp_diff = rp - rp_event_val
    rp_abs_diff = np.absolute(rp_diff)
    clos_ind = rp_abs_diff.argmin()
    clos_rp_diff = rp_diff[clos_ind]
    if clos_rp_diff == 0:
        rp_event = rv[clos_ind]
    elif clos_rp_diff < 0:
        low_rp = rp[clos_ind]
        upp_rp = rp[clos_ind-1]
        lu_rp_diff = upp_rp - low_rp
        lu_rv_diff = rv[clos_ind-1] - rv[clos_ind]
        frac_int = np.absolute(clos_rp_diff) / lu_rp_diff
        rp_event = rv[clos_ind] + (frac_int*lu_rv_diff)
    elif clos_rp_diff > 0:
        low_rp = rp[clos_ind+1]
        upp_rp = rp[clos_ind]
        lu_rp_diff = upp_rp - low_rp
        lu_rv_diff = rv[clos_ind] - rv[clos_ind+1]
        frac_int = np.absolute(clos_rp_diff) / lu_rp_diff
        rp_event = rv[clos_ind+1] + ((1-frac_int)*lu_rv_diff)
    return rp_event

def rp_event_calc(method,o_data,s_data,no_days,fig_c,rp_event_val,cbands=False,extrap_obs=False,time_thresh=-1,no_events_desired=100,scol='red'):
    if method == 'AnnMax':
        rp_o, rv_o = md_rp_rv_annmax(o_data,no_days)
        rp_event_obs_int = rp_event_calculator(rp_o,rv_o,rp_event_val)
        no_s_ens = np.shape(s_data)[0]
        rv_s_ens = np.zeros((no_s_ens,np.shape(s_data)[2]))
        s_ens_rp_events = np.zeros(no_s_ens)
        for i in range(no_s_ens):
            rp_s, rv_s_ens[i,:] = md_rp_rv_annmax(s_data[i,:,:],no_days)
            s_ens_rp_events[i] = rp_event_calculator(rp_s,rv_s_ens[i,:],rp_event_val)
        rp_rv_fig_ens(fig_c,rp_o,rv_o,rp_s,rv_s_ens,scol)
        o_fit_params = ss.genextreme.fit(rv_o)
        if extrap_obs==True:
            extrapolate_obs(o_fit_params,method,'black')
        if cbands == True:
            boot_params = boot.ci(rv_o,ss.genextreme.fit,n_samples=1000)
            ymin, ymax = ci_gev_band_sphere(o_fit_params,boot_params,rp_s[-1],rp_s[0],'black')
            plt.ylim(ymin,ymax)
#        if no_s_ens == 1:
#            s_fit_params = ss.genextreme.fit(rv_s_ens[0,:])
#            boot_params_s = boot.ci(rv_s_ens[0,:],ss.genextreme.fit,n_samples=1000)
#            _,_ = ci_gev_band_sphere(s_fit_params,boot_params_s,rp_s[-1],rp_s[0],scol)
#            extrapolate_obs(s_fit_params,method,scol)
        plt.xlim(rp_s[-1],rp_s[0])
        
    if method == 'POT':
        rp_o, rv_o, opt_thresh = pot_rp_rv(o_data,no_days,time_thresh,no_events_desired)
        no_s_ens = np.shape(s_data)[0]
        rp_pot_s_ens = {}
        rv_pot_s_ens = {}
        for i in range(no_s_ens):
            rp_pot_s_ens[i], rv_pot_s_ens[i] = pot_rp_rv_fixed_thresh(s_data[i,:,:],no_days,time_thresh,opt_thresh)
        rp_rv_fig_pot_ens(fig_c,rp_o,rv_o,rp_pot_s_ens,rv_pot_s_ens)
        rv_pot_fit = rv_o - opt_thresh
        o_fit_params = ss.genpareto.fit(rv_pot_fit)
        if cbands == True:
            boot_params = boot.ci(rv_pot_fit,ss.genpareto.fit,n_samples=1000)
            rp_scaler = np.size(rv_o) / rp_o[0]
            ci_gpd_band_sphere(o_fit_params,boot_params,rp_o[-1],rp_pot_s_ens[0][0],opt_thresh,rp_scaler)  
        if extrap_obs==True:
            extrapolate_obs(o_fit_params,method,ot=opt_thresh,rps=rp_scaler)
        plt.xlim(rp_o[-1],rp_pot_s_ens[0][0])
    return rp_o, rv_o, rp_event_obs_int, s_ens_rp_events


    
