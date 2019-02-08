# this script
# processes monthly percentile means for the CORDEX input data
# processes monthly means for the total length of the IMAGE data
# processes monthly means for each of the 30-year ensembles of IMAGE data

# arguments for testing
# slice = '01'; years_sim_1 = 4000; years_sim_2 = 6000; metric = 'appt'; continent = 'euro'; scen = 'hist'
# year_start = 1971; year_end = 2000; season_start = 5; season_end = 9; percentile = 99

from prog.functions.data.process_clag_stats_functions import *
import sys

# get total number of arguments
total = len(sys.argv)

# get the arguments list
cmdargs = str(sys.argv)

print(cmdargs)

# variables for processing CLaGARMi output
slice = sys.argv[1]
years_sim_1 = int(float((sys.argv[2])))
years_sim_2 = int(float((sys.argv[3])))
metric = sys.argv[4]
continent = sys.argv[5]
scen = sys.argv[6]
year_start = int(float((sys.argv[7])))
year_end = int(float((sys.argv[8])))
season_start = int(float((sys.argv[9])))
season_end = int(float((sys.argv[10])))
percentile = int(float((sys.argv[11])))

years_sim = years_sim_1 + years_sim_2
print(str(years_sim) + ' total years of simluation')

# load lon/lat table with country identifiers
lonlat = pd.read_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/lonlat/' + continent +'_lonlat_edit.csv')

print('loading all data')

# loading data for both observations and simulations
obs_data, sim_data_1 = load_clag_output(slice, years_sim_1, continent, scen, year_start, year_end, metric)
obs_data, sim_data_2 = load_clag_output(slice, years_sim_2, continent, scen, year_start, year_end, metric)

no_sites = obs_data.shape[0]

print('combining all simulation years')

# combine two sets of simulations (must be a faster way?) (check out numpy.stack)
sim_data_combined = np.empty([no_sites,(years_sim_1+years_sim_2),365])
for i in range(0, no_sites):
    for j in range(0,365):
        sim_data_combined[i,:,j] = np.concatenate((sim_data_1[i, :, j], sim_data_2[i, :, j]), axis=0)

print('simulation years combined')

#################################
# PORTUGAL (to generalise)
#################################

# values for location
port_values = [0, 1, 2, 3, 4, 5, 6, 7, 8]

# take footprint of country TO FINISH
obs_data_site = obs_data[port_values, :, :]

# take sample of combined years from sim_data_1
sim_data_combined_subset = sim_data_combined[port_values, :, :]

print('calculating Portugal return periods')

#################################
# HEAT WAVE DURATION PORTUGAL
#################################

obs_data_processed_site = seasonal_hw_duration_summary_europe(obs_data_site, obs_data_site, season_start, season_end, percentile)
sim_data_processed_site = seasonal_hw_duration_summary_europe(obs_data_site, sim_data_combined_subset, season_start, season_end, percentile)

# create duration characteristics for each site
data_obs = hw_duration_return_periods_europe(obs_data_processed_site)
data_sim = hw_duration_return_periods_europe(sim_data_processed_site)

# save to csv
data_obs.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_obs_intensity_return_periods_portugal.csv')
data_sim.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' + str(years_sim) + 'yrs_sim_intensity_return_periods_portugal.csv')

print('Heatwave return periods calculated for Portugal for ' + scen + ' ' + year_start + ' - ' + year_end)

#################################
# HEAT WAVE DURATION (30-year chunks)
# #################################

# # create empty frame to populate with subset values
# data_avg = pd.DataFrame(columns=['days_over', 'return_period', 'subset'])
#
# # loop through subsets to get some heat wave return periods
# for subset in range(0, int(np.floor(sim_data_combined_subset.shape[1]/30))):
#     print(subset)
#     # take sample of 30 years from sim_data_1 recursively
#     sim_data_1_subset_subset = sim_data_combined_subset[:,range(30*subset,(30*(subset+1))),:]
#     sim_data_processed_temp = seasonal_hw_duration_summary_europe(obs_data_site, sim_data_1_subset_subset, season_start, season_end, percentile)
#     # create duration characteristics for each site
#     data_sim_temp = hw_duration_return_periods_europe(sim_data_processed_temp)
#     # convert into pandas dataframe
#     data_sim_temp = pd.DataFrame(data_sim_temp)
#     data_sim_temp['subset'] = subset + 1
#     # concatenate to master file
#     data_avg = pd.concat([data_avg.reset_index(drop=True), data_sim_temp.reset_index(drop=True)], axis=0)
#
# print('saving Portugal return periods')
#
# # save to csv
# data_avg.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_30yrs_subsets_' + str(years_sim) + 'yrs_sim_intensity_return_periods_portugal.csv',index=False)
#
# print('thank u, next')

# BELOW TO FINISH

# # load lon/lat data for European grids
# lons = scipy.io.loadmat(os.path.join(cordex_output_local,'euro_cordex','lonlat/nobc_lons.mat'))
# lons_array = np.array(lons[list(lons.keys())[3]])
# lats = scipy.io.loadmat(os.path.join(cordex_output_local,'euro_cordex','lonlat/nobc_lats.mat'))
# lats_array = np.array(lats[list(lats.keys())[3]])
# lonlat = pd.DataFrame(np.concatenate([lons_array, lats_array], axis=1),columns=['lon','lat'])
#
# # export lon/lat table
# lonlat.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/lonlat/'+ continent +'_lonlat.csv')