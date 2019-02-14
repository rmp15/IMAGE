#!/bin/bash

# this script
# processes output of CLaGARMi into combined metrics like apparent temperature and SPEI
# processes the output of CLaGARMi into something R can plot

clear

cd ~/git/IMAGE/

# arguments for processing of files
declare slice='01'
declare -a years_sims=(4000 6000)
declare -a metrics=('appt')
declare -a continents=('euro')
declare -a countries=('Sweden' 'UK' 'Spain' 'Italy' 'Romania')
declare -a scens=('hist')
declare -i start=1971
declare -i end=2000

#################################################
# 1. EURO-CORDEX RUNS
#################################################

# PROCESS APPARENT TEMPERATURE
for years_sim in "${years_sims[@]}"; do
for continent in "${continents[@]}"; do
for scen in "${scens[@]}"; do

:
#python -m prog.02_processing_CLaGARMi.app_temp_process $slice $years_sim $continent $scen $start $end

done; done; done;

# PROCESS SETS OF 30-YEAR AVERAGES FOR COMPARISON IN A FIGURE
for years_sim in "${years_sims[@]}"; do
for metric in "${metrics[@]}"; do
for continent in "${continents[@]}"; do
for scen in "${scens[@]}"; do

:
#python -m prog.02_processing_CLaGARMi.30_year_averages_processing $slice $years_sim $metric $continent $scen $start $end

done; done; done; done;

#python ~/git/IMAGE/prog/02_processing_CLaGARMi/figure_8_processing.py $slice $years_sim $metric $continent $scen $start $end

# PROCESS RETURN PERIODS
declare -i year_sim_1=4000
declare -i year_sim_2=6000
declare -i season_start=5
declare -i season_end=9
declare -i percentile=99

for metric in "${metrics[@]}"; do
for continent in "${continents[@]}"; do
for scen in "${scens[@]}"; do
for country in "${counties[@]}"; do

python -m prog.02_processing_CLaGARMi.return_period_plots_processing $slice $year_sim_1 $year_sim_2 $metric $continent $scen $start $end $season_start $season_end $percentile $country

done; done; done; done;

