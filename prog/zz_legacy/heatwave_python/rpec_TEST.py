# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:16:14 2017

@author: srh110
"""

import numpy as np

rp = np.array([15,7.5,5,3.75,3,2.5])
rv = np.array([33,32,31,30.5,30,29.5])

rp_event_val = 7.5

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
    
print(rp_event)