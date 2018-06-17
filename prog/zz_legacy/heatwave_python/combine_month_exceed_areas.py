# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 10:53:24 2017

@author: srh110
"""

def combine_month_exceed_areas(month_exceed_extremes,months):
    
    
    
    tot_exceed_extremes = []
    for m in months:
        tot_exceed_extremes += month_exceed_extremes[m] 
    sorted_tot_exceed_extremes = sorted(tot_exceed_extremes,reverse=True)
    return sorted_tot_exceed_extremes