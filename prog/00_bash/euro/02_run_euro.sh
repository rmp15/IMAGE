#!/bin/bash

# this script
# run Cordex IMAGE

clear

cd ~/git/IMAGE/prog/CLaGARMi/

#################################################
# 1. EURO-CORDEX RUNS
#################################################

(

#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_hist_tasmax_huss_sfcWindmax_6000yr;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_hist_tasmax_huss_sfcWindmax_4000yr;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_hist_pr_ps_6000yr;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_hist_pr_ps_4000yr;

#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_85_2071_2100_tasmax_huss_sfcWindmax_6000yr ;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_85_2071_2100_tasmax_huss_sfcWindmax_4000yr ;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_85_2071_2100_pr_ps_6000yr ;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_85_2071_2100_pr_ps_4000yr ;

#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_45_2071_2100_tasmax_huss_sfcWindmax_6000yr ;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_45_2071_2100_tasmax_huss_sfcWindmax_4000yr ;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_45_2071_2100_pr_ps_6000yr ;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_45_2071_2100_pr_ps_4000yr ;

#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_85_2021_2050_tasmax_huss_sfcWindmax_6000yr ;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_85_2021_2050_tasmax_huss_sfcWindmax_4000yr ;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_85_2021_2050_pr_ps_6000yr ;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_85_2021_2050_pr_ps_4000yr ;

#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_45_2021_2050_tasmax_huss_sfcWindmax_6000yr ;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_45_2021_2050_tasmax_huss_sfcWindmax_4000yr ;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_45_2021_2050_pr_ps_6000yr ;
#matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_euro_45_2021_2050_pr_ps_4000yr ;

:
) &

#nohup matlab -nosplash -nodesktop -softwareopengl -r run_CLaGARMi_testdat ;
