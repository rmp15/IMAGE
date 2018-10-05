# this script
# processes apparent temperature values

from prog.functions.data.process_clag_stats_functions import *
import sys
import scipy.stats as stats

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
pr_obs_data,  pr_sim_data = load_clag_output(slice, years_sim, continent, scen, year_start, year_end, 'pr')

# take only the JJA months of data for each site and calculate means
pr_jja_sum_obs = seasonal_sum_calculator(pr_obs_data, 6, 8)
pr_jja_sum_sim = seasonal_sum_calculator(pr_sim_data[:,0:1000,:], 6, 8)

# compare a year of the simulated data to the mean value for each site
pr_jja_mean_obs = seasonal_mean_calculator(pr_obs_data, 6, 8)
pr_jja_mean_sim = seasonal_mean_calculator(pr_sim_data[:,0:1000,:], 6, 8)

# calculate gamma fit parameters for each site

#  cycle through obs and sim to generate spi for each site




# temporary save text
# np.savetxt('pr_jja_mean_obs.csv', pr_jja_mean_obs, delimiter=",")
# np.savetxt('pr_jja_mean_sim.csv', pr_jja_mean_sim, delimiter=",")

# take only the JJA months of data for each site and calculate rainfall percentiles
# pr_obs_jja = seasonal_data(pr_obs_data, 6, 8)
# pr_percentile_jja = seasonal_percentile_calculator(pr_obs_data, 6, 8, 50)

# appt_obs_data = app_temp_creator(tas_obs_data, huss_obs_data, ps_obs_data)
# appt_sim_data = app_temp_creator(tas_sim_data, huss_sim_data, ps_sim_data)

# processing monthly means for the CORDEX observation data
obs_data_processed = monthly_summary(appt_obs_data, 30, 0)

# processing monthly means for the CORDEX sim data
# with summary statistics for the entire period and for ensembles chunks
sim_data_processed_all, sim_data_processed_ens = monthly_summary(appt_sim_data, 30, 1)
obs_data_processed.columns = ['mean_value_obs', 'month', 'sd_value_obs', 'site']

sim_data_processed_all.columns = ['mean_value_sim', 'month', 'sd_value_sim', 'site']

# combine two tables of complete values
obs_sim_data_processed = pd.merge(obs_data_processed, sim_data_processed_all)

# output to merged obs and sim values to csv
obs_sim_data_processed.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' + str(years_sim) + 'yrs_' + '_obs_sim_merged.csv')
sim_data_processed_ens.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' + str(years_sim) + 'yrs_' + '_sim_ens.csv')
