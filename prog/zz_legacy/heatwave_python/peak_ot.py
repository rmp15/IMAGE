# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 14:01:39 2017

@author: srh110
"""

import numpy as np

def threshold_events(x_day_tots,thresh,time_thresh):    
    ab_be = np.zeros(np.size(x_day_tots))
    
    for i in range(np.size(x_day_tots)):
        if x_day_tots[i] > thresh:
            ab_be[i] = 1
    
    thresh_changes = np.diff(ab_be)
    pos_changes = np.where(thresh_changes==1)
    neg_changes = np.where(thresh_changes==-1)    
    
    no_pos_changes = np.size(pos_changes[0])
    no_neg_changes = np.size(neg_changes[0])
    
    
    event_lengths = np.zeros(no_pos_changes)
    non_event_lengths = np.zeros(no_pos_changes)
    non_event_lengths[0] = time_thresh+1
    for i in range(no_pos_changes):
        event_lengths[i] = neg_changes[0][i] - pos_changes[0][i]
        if i < (no_pos_changes-1):
            non_event_lengths[i+1] = pos_changes[0][i+1] - neg_changes[0][i]
        
    
    


    event_length_list = []
    event_start_inds = []
    for i in range(np.size(non_event_lengths)):
        if non_event_lengths[i] > time_thresh:
            event_length_list.append(int(event_lengths[i]))
            event_start_inds.append(pos_changes[0][i]+1)
        else:
            event_length_list[-1] += int(event_lengths[i])
    
    return event_length_list, event_start_inds, len(event_length_list)

def pot_rp_rv(daily_mean_var,no_days,time_thresh,no_events_desired):

    
    var_shape = np.shape(daily_mean_var)
    
    no_years = var_shape[1]
    
    

    

    
    
    var_flat = np.ndarray.flatten(daily_mean_var,order='F')
    var_flat = var_flat - 273.15
    x_day_tots = np.zeros(np.size(var_flat)+1-no_days)
    for i in range(np.size(x_day_tots)):
        x_day_tots[i] = np.mean(var_flat[i:i+no_days])
    
    

    
    min_thresh_try = 23
    thresh_tries = 20
    thresh_gap = 0.5
    thresh_stop = int(min_thresh_try + (thresh_tries*thresh_gap))
    thresholds = np.arange(min_thresh_try,thresh_stop,thresh_gap)
    thresh_events = np.zeros((thresh_tries,2))
    th = 0
    for thresh in thresholds:
        thresh_events[th,0] = thresh
        _,_, thresh_events[th,1] = threshold_events(x_day_tots,thresh,time_thresh)
        th += 1
            

    
    opt_thresh = thresh_events[(np.abs(thresh_events[:,1]-no_events_desired)).argmin(),0]
    
    event_length_list, event_start_inds, no_events = threshold_events(x_day_tots,opt_thresh,time_thresh)
    
    peak_values = np.zeros(no_events)
    peak_value_inds = np.zeros(no_events)
    for i in range(no_events):
        peak_values[i] = np.max(x_day_tots[event_start_inds[i]:(event_start_inds[i]+event_length_list[i])])
        peak_value_inds[i] = (x_day_tots[event_start_inds[i]:(event_start_inds[i]+event_length_list[i])]).argmax() + event_start_inds[i]
        
#    plt.figure(1)
#    plt.plot(x_day_tots)
#    for i in range(no_events):
#        plt.scatter(peak_value_inds[i],x_day_tots[peak_value_inds[i]],c='black',marker='+')
#    plt.plot([0,10000],[27,27],c='red') 
#    plt.xlim(1560,2520)   
    
    peak_values = sorted(peak_values,reverse=True)
    no_peak_values = np.size(peak_values)
    rp = np.zeros(no_peak_values)
    for i in range(0,no_peak_values):
        rp[i] = no_years / (i+1)

    return rp, peak_values, opt_thresh
    
def pot_rp_rv_fixed_thresh(daily_mean_var,no_days,time_thresh,thresh):

    
    var_shape = np.shape(daily_mean_var)
    
    no_years = var_shape[1]
    
    

    

   
    
    
    var_flat = np.ndarray.flatten(daily_mean_var,order='F')
    var_flat = var_flat - 273.15
    x_day_tots = np.zeros(np.size(var_flat)+1-no_days)
    for i in range(np.size(x_day_tots)):
        x_day_tots[i] = np.mean(var_flat[i:i+no_days])
    
    

    

            

    
    opt_thresh = thresh
    
    event_length_list, event_start_inds, no_events = threshold_events(x_day_tots,opt_thresh,time_thresh)
    
    peak_values = np.zeros(no_events)
    peak_value_inds = np.zeros(no_events)
    for i in range(no_events):
        peak_values[i] = np.max(x_day_tots[event_start_inds[i]:(event_start_inds[i]+event_length_list[i])])
        peak_value_inds[i] = (x_day_tots[event_start_inds[i]:(event_start_inds[i]+event_length_list[i])]).argmax() + event_start_inds[i]
        
#    plt.figure(1)
#    plt.plot(x_day_tots)
#    for i in range(no_events):
#        plt.scatter(peak_value_inds[i],x_day_tots[peak_value_inds[i]],c='black',marker='+')
#    plt.plot([0,10000],[27,27],c='red') 
#    plt.xlim(1560,2520)   
    no_peak_values = np.size(peak_values)
    rp = np.zeros(no_peak_values)
    for i in range(0,no_peak_values):
        rp[i] = no_years / (i+1)  
    peak_values = sorted(peak_values,reverse=True)
    return rp, peak_values
    