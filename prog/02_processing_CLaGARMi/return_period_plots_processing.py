# this script
# processes monthly percentile means for the CORDEX input data
# processes monthly means for the total length of the IMAGE data
# processes monthly means for each of the 30-year ensembles of IMAGE data

# arguments for testing
# slice = '01'; years_sim_1 = 4000; years_sim_2 = 6000; metric = 'appt'; continent = 'euro'; scen = 'hist'
# year_start = 1971; year_end = 2000; season_start = 5; season_end = 9; percentile = 99; country = 'Sweden'

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
country = sys.argv[12]

years_sim = years_sim_1 + years_sim_2
print(str(years_sim) + ' total years of simluation')

print('loading all data')

# loading data for original observed data to calculate percentiles against
obs_data = load_clag_output_observed_only(slice, years_sim_1, continent, 'hist', 1971, 2000, metric)

# loading data for simulations
dummy, sim_data_1 = load_clag_output(slice, years_sim_1, continent, scen, year_start, year_end, metric)
dummy, sim_data_2 = load_clag_output(slice, years_sim_2, continent, scen, year_start, year_end, metric)

# obtain number of sites (redundant?)
no_sites = obs_data.shape[0]

#################################
# CHOOSE PARTICULAR COUNTRY FOOTPRINT
#################################

# load lon/lat table with country identifiers
lonlat = pd.read_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/lonlat/' + continent +'_lonlat_edit.csv')

# isolate particular country IDs and put into list
if country != 'Europe':
    footprint_values = lonlat[lonlat['country'] == country]['ID'].tolist()

    # take footprint of country
    obs_data_footprint = obs_data[footprint_values, :, :]

    # take sample of sim years then combine
    sim_data_1_subset = sim_data_1[footprint_values, :, :]
    sim_data_2_subset = sim_data_2[footprint_values, :, :]

# if want to take entire continent then special option
if country == 'Europe':
    footprint_values = range(0,obs_data.shape[0])

    obs_data_footprint = obs_data

    # take sample of sim years then combine
    sim_data_1_subset = sim_data_1
    sim_data_2_subset = sim_data_2


#################################
# COMBINE ALL SIM YEARS TOGETHER
#################################

print('combining all simulation years')

# combine two sets of simulations
sim_data_footprint = np.empty([len(footprint_values), (years_sim_1 + years_sim_2), 365])
for i in range(0, len(footprint_values)):
    for j in range(0, 365):
        sim_data_footprint[i, :, j] = np.concatenate((sim_data_1_subset[i, :, j], sim_data_2_subset[i, :, j]), axis=0)

print('simulation years combined')

print('calculating ' + country + ' return periods')

#################################
# HEAT WAVE DURATION CHOSEN COUNTRY
#################################

# obs_data_processed_site = seasonal_hw_duration_summary_europe(obs_data_footprint, obs_data_footprint, season_start, season_end, percentile)
sim_data_processed_site = seasonal_hw_duration_summary_europe(obs_data_footprint, sim_data_footprint, season_start, season_end, percentile)

# create duration characteristics for each site
# data_obs = hw_duration_return_periods_europe(obs_data_processed_site)
data_sim = hw_duration_return_periods_europe(sim_data_processed_site)

print('Heatwave return periods calculated for entire period for '+country +' for ' + scen + ' ' + str(year_start) + ' - ' + str(year_end))

# save to csv
# data_obs.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_obs_intensity_return_periods_'+country+'.csv')
data_sim.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' + str(years_sim) + 'yrs_sim_intensity_return_periods_'+country+'.csv')

#################################
# HEAT WAVE DURATION (30-year chunks)
#################################

# # create empty frame to populate with subset values
# data_avg = pd.DataFrame(columns=['days_over', 'return_period', 'subset'])
#
# # loop through subsets to get some heat wave return periods
# for subset in range(0, int(np.floor(sim_data_footprint.shape[1]/30))):
#     print(subset)
#     # take sample of 30 years from sim_data_1 recursively
#     sim_data_footprint_subset = sim_data_footprint[:,range(30*subset,(30*(subset+1))),:]
#     sim_data_processed_temp = seasonal_hw_duration_summary_europe(obs_data_footprint, sim_data_footprint_subset, season_start, season_end, percentile)
#     # create duration characteristics for each site
#     data_sim_temp = hw_duration_return_periods_europe(sim_data_processed_temp)
#     # convert into pandas dataframe
#     data_sim_temp = pd.DataFrame(data_sim_temp)
#     data_sim_temp['subset'] = subset + 1
#     # concatenate to master file
#     data_avg = pd.concat([data_avg.reset_index(drop=True), data_sim_temp.reset_index(drop=True)], axis=0)
#
# print('saving ' + country + ' return periods')
#
# # save to csv
# data_avg.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_30yrs_subsets_' + str(years_sim) + 'yrs_sim_intensity_return_periods_'+ country +'.csv',index=False)
#
# print(country + ' done. Thank u, next')
#
# legacy for lonlat
#
# # load lon/lat data for European grids
# lons = scipy.io.loadmat(os.path.join(cordex_output_local,'euro_cordex','lonlat/nobc_lons.mat'))
# lons_array = np.array(lons[list(lons.keys())[3]])
# lats = scipy.io.loadmat(os.path.join(cordex_output_local,'euro_cordex','lonlat/nobc_lats.mat'))
# lats_array = np.array(lats[list(lats.keys())[3]])
# lonlat = pd.DataFrame(np.concatenate([lons_array, lats_array], axis=1),columns=['lon','lat'])
#
# # export lon/lat table
# lonlat.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/lonlat/'+ continent +'_lonlat.csv')