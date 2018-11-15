# this script
# processes monthly percentile means for the CORDEX input data
# processes monthly means for the total length of the IMAGE data
# processes monthly means for each of the 30-year ensembles of IMAGE data

from prog.functions.data.process_clag_stats_functions import *
import sys
import os

# get total number of arguments
total = len(sys.argv)

# get the arguments list
cmdargs = str(sys.argv)

# variables for processing CLaGARMi output
slice = sys.argv[1]                             # slice = '01'
years_sim_1 = int(float((sys.argv[2])))         # years_sim_1 = 4000 ; years_sim_2 = 6000
metric = sys.argv[3]                            # metric = 'tasmax'
continent = sys.argv[4]                         # continent = 'euro'
scen = sys.argv[5]                              # scen = 'hist'
year_start = int(float((sys.argv[6])))          # year_start = 1971
year_end = int(float((sys.argv[7])))            # year_end = 2000
season_start = int(float((sys.argv[8])))        # season_start = 5
season_end = int(float((sys.argv[9])))          # season_end = 9
percentile = int(float((sys.argv[10])))         # percentile = 99

#slice = '01'; years_sim_1 = 4000 ; years_sim_2 = 6000; metric = 'tasmax'; continent = 'euro'; scen = 'hist'
year_start = 1971; year_end = 2000; season_start = 5; season_end = 9; percentile = 99

# file loc in case its being run on linux platform
if sys.platform == 'linux' or sys.platform == 'linux2':
    image_output_local = os.path.join('/home/rmp15/data/IMAGE/CLaGARMi/euro_cordex_output/')
    cordex_output_local = os.path.join('/home/rmp15/data/IMAGE/CORDEX/')

# loading data for both observations and simulations
obs_data, sim_data_1 = load_clag_output(slice, years_sim_1, continent, scen, year_start, year_end, metric)
obs_data, sim_data_2 = load_clag_output(slice, years_sim_2, continent, scen, year_start, year_end, metric)

# save obs and sim data
output_obs_name_1 = image_output_local + metric + '/out_' + slice + '_y' + str(years_sim_1) + '_' + continent + '_' + str(scen) + '_' \
                  + str(year_start) + '_' + str(year_end) + '_' + metric + '_o.npy'
output_obs_name_2 = image_output_local + metric + '/out_' + slice + '_y' + str(years_sim_2) + '_' + continent + '_' + str(scen) + '_' \
                  + str(year_start) + '_' + str(year_end) + '_' + metric + '_o.npy'
output_sim_name_1 = image_output_local + metric + '/out_' + slice + '_y' + str(years_sim_1) + '_' + continent + '_' + str(scen) + '_' \
                  + str(year_start) + '_' + str(year_end) + '_' + metric + '_s.npy'
output_sim_name_2 = image_output_local + metric + '/out_' + slice + '_y' + str(years_sim_2) + '_' + continent + '_' + str(scen) + '_' \
                  + str(year_start) + '_' + str(year_end) + '_' + metric + '_s.npy'
np.save(output_obs_name_1, obs_data)
np.save(output_obs_name_2, obs_data)
np.save(output_sim_name_1, sim_data_1)
np.save(output_sim_name_2, sim_data_2)