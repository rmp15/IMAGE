# this script
# processes monthly means for the CORDEX input data
# processes monthly means for the total length of the IMAGE data
# processes monthly means for each of the 30-year ensembles of IMAGE data

from prog.functions.data.process_clag_stats_functions import *

# variables for processing CLaGARMi output PUT SOMEWHERE ELSE IN SOME SORT OF DATA FILE
slice = '01'
years_sim = 300
metric = 'sfcWindmax'
continent = 'euro'
scen = 'hist'
year_start = 1971
year_end = 2000

# loading data for both observations and simulations
obs_data, sim_data = load_clag_output(slice, years_sim, continent, scen, year_start, year_end, metric)

# processing monthly means for the CORDEX observation data
obs_data_processed = monthly_summary(obs_data, 30, 0)

# processing monthly means for the CORDEX sim data
# with summary statistics for the entire period and for ensembles chunks
sim_data_processed_all, sim_data_processed_ens = monthly_summary(sim_data, 30, 1)
obs_data_processed.columns = ['mean_value_obs', 'month', 'sd_value_obs', 'site']
sim_data_processed_all.columns = ['mean_value_sim', 'month', 'sd_value_sim', 'site']

# combine two tables of complete values temporarily (next iteration process statistics for ensembles here not in R)
obs_sim_data_processed = pd.merge(obs_data_processed, sim_data_processed_all)

# output to merged obs and sim values to csv
obs_sim_data_processed.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_obs_sim_merged.csv')
sim_data_processed_ens.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_sim_ens.csv')
