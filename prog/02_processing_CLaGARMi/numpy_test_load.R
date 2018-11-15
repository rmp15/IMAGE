# break down the arguments from Rscript
args <- commandArgs(trailingOnly=TRUE)
slice = as.character(args[1])                   # slice = '01'
years_sim_1 = as.numeric(args[2])               # years_sim_1 = 4000 ; years_sim_2 = 6000
metric = as.character(args[3])                  # metric = 'tasmax'
continent = as.character(args[4])               # continent = 'euro'
scen = as.character(args[5])                    # scen = 'hist'
year_start = as.numeric(args[6])                # year_start = 1971
year_end = as.numeric(args[7])                  # year_end = 2000

# slice = '01' ; years_sim_1 = 4000 ; years_sim_2 = 6000 ; metric = 'tasmax' ; continent = 'euro' ;
# scen = 'hist'; year_start = 1971 ; year_end = 2000

# local file outputs from IMAGE (change for on wrfstore because of python's weird system)
image_output_local = '/Users/rmiparks/data/IMAGE/CLaGARMi/euro_cordex_output/'

file.loc = paste0(image_output_local,metric,'/out_',slice,'_y',years_sim_1,'_',continent,'_',scen,'_',year_start,'_',year_end,'_',metric,'_o.npy' )
# image_output_local + metric + '/out_' + slice + '_y' + str(years_sim_1) + '_' + continent + '_' + str(scen) + '_' \
# + str(year_start) + '_' + str(year_end) + '_' + metric + '_o.npy'

# to enable reading of numpy files in R
library(reticulate)
np <- import("numpy")

file.loc = # SOME FILE LOCATION DEFINED BY ARGUMENTS
mat <- np$load(file.loc)

# how to concatenate 4000,6000 year files