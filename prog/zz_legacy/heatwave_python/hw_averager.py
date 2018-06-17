# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 15:18:26 2017

@author: srh110
"""

from numpy import mean,size,zeros

def hw_averager(temp_data,no_days,region):
    region_ave = mean(temp_data[:,:,region[0]:region[1]],2)
    return region_ave
    
def max_each_year(temp_data,no_days,region):
    region_ave = mean(temp_data[:,:,region[0]:region[1]],2)
    no_years = size(temp_data,1)
    max_ey = zeros(no_years)
    for i in range(0,no_years):
        max_ey[i] = max(region_ave[:,i])
    return max_ey
    