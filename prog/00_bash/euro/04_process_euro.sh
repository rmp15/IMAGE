#!/bin/bash

# this script
# processes output of CLaGARMi into combined metrics like apparent temperature and SPEI
# processes the output of CLaGARMi into something R can plot

clear

#cd ~/git/IMAGE/prog/CLaGARMi/

# arguments for processing of files
declare slice='01'
declare -a years_sims=(4000 6000)
declare -a metrics=('huss') # 'huss' 'sfcWindmax')
declare -a continents=('euro')
declare -a scens=('hist')
declare -i start=1971
declare -i end=2000

#################################################
# 1. EURO-CORDEX RUNS
#################################################

for years_sim in "${years_sims[@]}"; do
for metric in "${metrics[@]}"; do
for continent in "${continents[@]}"; do
for scen in "${scens[@]}"; do

#python ~/git/IMAGE/prog/02_processing_CLaGARMi/figure_2_3_processing.py $slice $years_sim $metric $continent $scen $start $end
python3.6 ~/git/IMAGE/prog/02_processing_CLaGARMi/app_temp_process.py $slice $years_sim $continent $scen $start $end

done; done; done; done;

#python ~/git/IMAGE/prog/02_processing_CLaGARMi/figure_8_processing.py $slice $years_sim $metric $continent $scen $start $end
