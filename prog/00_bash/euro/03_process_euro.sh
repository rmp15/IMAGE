#!/bin/bash

# this script
# processes the output of CLaGARMi into something R can plot

clear

#cd ~/git/IMAGE/prog/CLaGARMi/

# arguments for processing of files
declare slice='01'
declare -a years_sims=(6000 4000)
declare -a metrics=('tasmax' 'huss' 'sfcWindmax')
declare -a continents=('euro')
declare -a scens=('hist')
declare -i start_year=1971
declare -i end_year = 2000

#################################################
# 1. EURO-CORDEX RUNS
#################################################

for years_sim in "${years_sims[@]}"; do
for metric in "${metrics[@]}"; do
for continent in "${continents[@]}"; do
for scen in "${scens[@]}"; do

python3 ~/git/IMAGE/prog/02_processing_CLaGARMi/figure_2_processing.py $slice $years_sim $metric $continent $scen $start_year $end_year

done; done; done; done;