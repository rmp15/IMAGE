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
metric = sys.argv[3]                            # metric = 'sfcWindmax'
continent = sys.argv[4]                         # continent = 'euro'
scen = sys.argv[5]                              # scen = 'hist'
year_start = int(float((sys.argv[6])))          # year_start = 1971
year_end = int(float((sys.argv[7])))            # year_end = 2000

print('loading data for ' + metric)

# loading data for both observations and simulations
obs_data, sim_data = load_clag_output(slice, years_sim, continent, scen, year_start, year_end, metric)

print('processing monthly means')

# processing monthly means for the CORDEX observation data
obs_data_processed = monthly_mean_summary(obs_data, 30, 0)

print('processing monthly means')

# processing monthly means for the CORDEX sim data
# with summary statistics for the entire period and for ensembles chunks
sim_data_processed_all, sim_data_processed_ens = monthly_mean_summary(sim_data, 30, 1)
obs_data_processed.columns = ['mean_value_obs', 'month', 'sd_value_obs', 'site']
sim_data_processed_all.columns = ['mean_value_sim', 'month', 'sd_value_sim', 'site']

# combine two tables of complete values
obs_sim_data_processed = pd.merge(obs_data_processed, sim_data_processed_all)

# output to merged obs and sim values to csv
obs_sim_data_processed.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' + str(years_sim) + 'yrs_' + 'obs_sim_merged.csv')
sim_data_processed_ens.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' + str(years_sim) + 'yrs_' + 'sim_ens.csv')
