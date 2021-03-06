#!/bin/bash

# this script
# processes the output of CLaGARMi into something R can plot

clear

#cd ~/git/IMAGE/prog/CLaGARMi/

# arguments for processing of files
declare slice='01'
declare -i years_sim1=6000
declare -i years_sim2=4000
declare -a metrics=('tasmax') # 'appt' 'sfcWindmax')
declare -a continents=('euro')
declare -a scens=('hist')
declare -i start=1971
declare -i end=2000

#################################################
# 1. EURO-CORDEX RUNS
#################################################

# COMPARISON OF
for metric in "${metrics[@]}"; do
for continent in "${continents[@]}"; do
for scen in "${scens[@]}"; do

Rscript ~/git/IMAGE/prog/03_plotting_CLaGARMi/return_periods_country.R $slice $years_sim1 $years_sim2 $metric $continent $scen $start $end

done; done; done;