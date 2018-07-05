#!/bin/bash

# this script
# processes the output of CLaGARMi into something R can plot

clear

#cd ~/git/IMAGE/prog/CLaGARMi/

# arguments for processing of files
declare slice='01'
declare -a years_sims=(4000)
declare -a metrics=('tasmax') # 'huss' 'sfcWindmax')
declare -a continents=('euro')
declare -a scens=('hist')
declare -i start=1971
declare -i end=2000

#################################################
# 1. EURO-CORDEX RUNS
#################################################

python ~/git/IMAGE/prog/02_processing_CLaGARMi/figures.py
