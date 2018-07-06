#!/bin/bash

# this script
# run Cordex IMAGE

clear

cd ~/git/IMAGE/prog/CLaGARMi/

#################################################
# 1. EURO-CORDEX RUNS
#################################################

(

#nohup matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_hist ;
#nohup matlab -nosplash -nojvm -nodesktop -softwareopengl -r run_CLaGARMi_euro_85_2021_2050 ;
#nohup matlab -nosplash -nojvm -nodesktop -softwareopengl -r run_CLaGARMi_euro_85_2071_2100 ;
nohup matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_45_2021_2050 ;
#nohup matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_45_2071_2100 ;
:
) &

#nohup matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_testdat ;
