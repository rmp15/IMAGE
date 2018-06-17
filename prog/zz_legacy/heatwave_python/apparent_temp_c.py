# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 16:42:22 2017

@author: srh110
"""

import numpy as np


"""
THIS IS WRONG
"""

def apparent_temp_c(mean_temp,dew_point_temp):
    #check input arrays are same size
    if np.shape(mean_temp) == np.shape(dew_point_temp):
        
        mean_temp_f = (1.8*mean_temp) + 32
        dpt_f = (1.8*mean_temp) + 32
        app_t_f = (0.0153*dpt_f*dpt_f) + (0.994*mean_temp_f) - 2.653
        app_t_c = (5.0/9.0)*(app_t_f-32)
        return app_t_c
    
    else:
        raise ValueError('input temp arrays not same shape')
        
        