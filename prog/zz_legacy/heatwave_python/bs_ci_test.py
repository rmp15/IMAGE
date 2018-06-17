# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 15:41:42 2017

@author: srh110
"""

import scipy.stats as ss
import numpy as np

rp = np.zeros(14)
rp2 = np.zeros(14)
rp3 = np.zeros(14)
temps = range(23,37)
for temp in range(23,37):
    pdf1 = ss.genextreme.cdf(temp,o_fit_params[0],o_fit_params[1],o_fit_params[2])
    print(pdf1)
    rp[temp-23] = (1 / (1-pdf1))
    pdf2 = ss.genextreme.cdf(temp,boot_params[0,0],boot_params[0,1],boot_params[0,2])
    rp2[temp-23] = (1 / (1-pdf2))
    pdf3 = ss.genextreme.cdf(temp,boot_params[1,0],boot_params[1,1],boot_params[1,2])
    rp3[temp-23] = (1 / (1-pdf3))  

plt.figure(1)
plt.plot(rp,temps,c='black')
plt.xlim(0,30)
plt.plot(rp2,temps,c='g')
plt.plot(rp3,temps,c='g')
#plt.xscale('log')

#pdf_vals = np.zeros(36)
#temp_vals = range(0,36)
#for temp in range(0,36):
#    pdf_vals[temp] = ss.pareto.pdf(temp,o_fit_params[0],o_fit_params[1],o_fit_params[2])
#
#plt.figure(2)
#plt.plot(temp_vals,pdf_vals)  

t = np.zeros(100)
p1 = np.zeros(100)
p2 = np.zeros(100)
p3 = np.zeros(100)

for i in range(0,100):
    temp = 23 + ((14/100) * i)
    t[i] = temp
    p1[i] = ss.genextreme.pdf(temp,o_fit_params[0],o_fit_params[1],o_fit_params[2])
    p2[i] = ss.genextreme.pdf(temp,boot_params[0,0],boot_params[0,1],boot_params[0,2])
    p3[i] = ss.genextreme.pdf(temp,boot_params[1,0],boot_params[1,1],boot_params[1,2])
    
plt.plot(t,p1)
plt.plot(t,p2,c='r')
plt.plot(t,p3,c='g')