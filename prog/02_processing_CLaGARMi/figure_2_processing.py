# this script
# processes monthly means for the CORDEX input data
# processes monthly means for the total length of the IMAGE data
# processes monthly means for each of the 30-year ensembles of IMAGE data

from 02_processing_CLaGARMi.process_clag_stats_functions import *

# loading data for both observations and simulations
obs_data, sim_data = load_clag('01', 300, 'euro', 'hist', 1971, 2000, 'tasmax')

# processing monthly means for the CORDEX observation data

