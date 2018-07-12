# this script
# processes monthly means for the CORDEX input data
# processes monthly means for the total length of the IMAGE data
# processes monthly means for each of the 30-year ensembles of IMAGE data

from prog.functions.data.process_clag_stats_functions import *
import sys

# get total number of arguments
total = len(sys.argv)

# get the arguments list
cmdargs = str(sys.argv)

# variables for processing CLaGARMi output
slice = sys.argv[1]                             # slice = '01'
years_sim = int(float((sys.argv[2])))           # years_sim = 4000
continent = sys.argv[3]                         # continent = 'euro'
scen = sys.argv[4]                              # scen = 'hist'
year_start = int(float((sys.argv[5])))          # year_start = 1971
year_end = int(float((sys.argv[6])))            # year_end = 2000

# loading data for both observations and simulations
tas_obs_data,  tas_sim_data = load_clag_output(slice, years_sim, continent, scen, year_start, year_end, 'tasmax')
wind_obs_data, wind_sim_data = load_clag_output(slice, years_sim, continent, scen, year_start, year_end, 'sfcWindmax')

windchill_obs_data = wind_chill_creator(tas_obs_data, wind_obs_data)
windchill_sim_data = wind_chill_creator(tas_sim_data, wind_sim_data)

# output root file
sroot = '~/data/IMAGE/CLaGARMi/euro_cordex_output/'
savefilename = 'out_' + slice + '_y' + str(years_sim) + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end)


windchill_o_fn = sroot + 'windchill/' + savefilename + '_windchill_o'
windchill_s_fn = sroot + 'windchill/' + savefilename + '_windchill_s'


