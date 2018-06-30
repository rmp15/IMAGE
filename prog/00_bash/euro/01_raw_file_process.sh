#!/bin/bash

# this script
# run Cordex IMAGE

clear

cd ~/git/IMAGE/prog/01_extract_files/

#################################################
# 1. EURO-CORDEX RUNS
#################################################

(

nohup matlab -nosplash -nodesktop -softwareopengl -r CORDEX_create_nobc_data ;

) &
