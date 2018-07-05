#!/bin/bash

# this script
# processes the output of CLaGARMi into something R can plot

clear

#cd ~/git/IMAGE/prog/CLaGARMi/

# arguments for processing of files
declare slice='01'
declare -y years_sim1=6000
declare -y years_sim2=4000
declare -a metrics=('tasmax') # 'huss' 'sfcWindmax')
declare -a continents=('euro')
declare -a scens=('hist')
declare -i start=1971
declare -i end=2000

#################################################
# 1. EURO-CORDEX RUNS
#################################################

for metric in "${metrics[@]}"; do
for continent in "${continents[@]}"; do
for scen in "${scens[@]}"; do

Rscript ~/git/IMAGE/prog/02_processing_CLaGARMi/figures.R $slice $years_sim1 $years_sim2 $metric $continent $scen $start $end

done; done; done;