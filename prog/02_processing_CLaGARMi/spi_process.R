rm(list=ls())

library(SPEI)

# break down the arguments from Rscript
args <- commandArgs(trailingOnly=TRUE)
slice = as.character(args[1])                   # slice = '01'
years_sim_1 = as.numeric(args[2])               # years_sim_1 = 4000 ; years_sim_2 = 6000
metric = as.character(args[3])                  # metric = 'pr'
continent = as.character(args[4])               # continent = 'euro'
scen = as.character(args[5])                    # scen = 'hist'
year_start = as.numeric(args[6])                # year_start = 1971
year_end = as.numeric(args[7])                  # year_end = 2000

# slice = '01' ; years_sim_1 = 4000 ; years_sim_2 = 6000 ; metric = 'pr' ; continent = 'euro' ;
# scen = 'hist'; year_start = 1971 ; year_end = 2000

# local file outputs from IMAGE (change for on wrfstore because of python's weird system)
image_output_local = '/Users/rmiparks/data/IMAGE/CLaGARMi/euro_cordex_output/'
file.loc.hist = paste0(image_output_local,metric,'/out_',slice,'_y',years_sim_1,'_',continent,'_',scen,'_',year_start,'_',year_end,'_',metric,'_o.npy' )
file.loc.sim = paste0(image_output_local,metric,'/out_',slice,'_y',years_sim_1,'_',continent,'_',scen,'_',year_start,'_',year_end,'_',metric,'_s.npy' )

# to enable reading of numpy files in R
library(reticulate)
np = import("numpy")

# load historical file and sim files
pr.hist = np$load(file.loc.hist)
pr.sim = np$load(file.loc.sim)

# concatenate 4000,6000 year files
# FIGURE OUT LATER

# test take one site and calculate SPI as test, convert to mm m-2 s-1 (currently in kg m-2 s-1)
site = pr.hist[1,,]
site.vector = as.vector(t(site))

# calculate monthly means through time
month_days = c(31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
month_end_inds = cumsum(month_days)

# create dataframe with year, month, precipitation
