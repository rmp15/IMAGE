# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 10:01:40 2017

@author: srh110
"""

def gen_gpd_pdf(param1,param2,param3):

    t = np.zeros(200)
    pdf = np.zeros(200)
    
    for i in range(0,200):
        temp = 22 + ((25/200)*i)
        t[i] = temp
        pdf[i] = ss.genpareto.pdf(temp,param1,param2,param3)
        
    return t, pdf

o_fit_params = ss.pareto.fit(rv_pot_o)
boot_params = boot.ci(rv_pot_o,ss.pareto.fit,n_samples=1000)
b_fit_params = ss.genpareto.fit(rv_pot_o,floc=27)

temps, pdfs = gen_gpd_pdf(b_fit_params[0],b_fit_params[1],b_fit_params[2])

plt.plot(temps,pdfs*91)



plt.hist(rv_pot_o)

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
    
plt.figure(4)
for i in range(26):
    plt.plot(temps,sphere_pdfs[i,:])
    
max_band = np.zeros(200)
min_band = np.zeros(200)

for i in range(0,200):
    max_band[i] = np.max(sphere_pdfs[:,i])
    min_band[i] = np.min(sphere_pdfs[:,i])
    
obs_cdf = np.zeros(91)

for i in range(91):
    obs_cdf[i] = (90-i)/91
    
#plt.plot(rv_pot_o,obs_cdf,c='black')