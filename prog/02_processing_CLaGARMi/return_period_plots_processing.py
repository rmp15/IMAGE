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
print(str(years_sim)+ ' total years of simluation')

# load lon/lat table with country identifiers
lonlat = pd.read_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/lonlat/'+ continent +'_lonlat_edit.csv')

# loading data for both observations and simulations
obs_data, sim_data_1 = load_clag_output(slice, years_sim_1, continent, scen, year_start, year_end, metric)
obs_data, sim_data_2 = load_clag_output(slice, years_sim_2, continent, scen, year_start, year_end, metric)

no_sites = obs_data.shape[0]

print('combining all simulation years')

# combine two sets of simulations (must be a faster way?) (check out numpy.stack)
# TO DO make a separate code to do this once
sim_data_combined = np.empty([no_sites,(years_sim_1+years_sim_2),365])
for i in range(0, no_sites):
    for j in range(0,365):
        sim_data_combined[i,:,j] = np.concatenate((sim_data_1[i,:,j], sim_data_2[i,:,j]), axis=0)

#################################
# HEAT WAVE DURATION PORTUGAL (30-year chunks)
#################################

print('calculating Portugal return periods')

# create empty frame to populate with subset values
data_avg = pd.DataFrame(columns=['days_over', 'return_period', 'subset'])

# loop through subsets to get some heat wave return periods
for subset in range(0, int(np.floor(sim_data_combined_subset.shape[1]/30))):
    print(subset)
    # take sample of 30 years from sim_data_1 recursively
    sim_data_1_subset_subset = sim_data_combined_subset[:,range(30*subset,(30*(subset+1))),:]
    sim_data_processed_temp = seasonal_hw_duration_summary_europe(obs_data_site, sim_data_1_subset_subset, season_start, season_end, percentile)
    # create duration characteristics for each site
    data_sim_temp = hw_duration_return_periods_europe(sim_data_processed_temp)
    # convert into pandas dataframe
    data_sim_temp = pd.DataFrame(data_sim_temp)
    data_sim_temp['subset'] = subset + 1
    # concatenate to master file
    data_avg = pd.concat([data_avg.reset_index(drop=True), data_sim_temp.reset_index(drop=True)], axis=0)

print('saving Portugal return periods')

# save to csv
data_avg.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_30yrs_subsets_' + str(years_sim) + 'yrs_sim_intensity_return_periods_portugal.csv',index=False)

print('thank u, next')

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

#################################
# HEAT WAVE DURATION PORTUGAL
#################################

# port_values = [0,1,2,3,4,5,6,7,8]
#
# # take footprint of country TO FINISH
# obs_data_site = obs_data[port_values,:,:]
#
# # take sample of combined years from sim_data_1
# sim_data_combined_subset = sim_data_combined[port_values,:,:]
#
# obs_data_processed_site = seasonal_hw_duration_summary_europe(obs_data_site, obs_data_site, season_start, season_end, percentile)
# sim_data_processed_site = seasonal_hw_duration_summary_europe(obs_data_site, sim_data_combined_subset, season_start, season_end, percentile)
#
# # create duration characteristics for each site
# data_obs = hw_duration_return_periods_europe(obs_data_processed_site)
# data_sim = hw_duration_return_periods_europe(sim_data_processed_site)
#
# # save to csv
# data_obs.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_obs_intensity_return_periods_portugal.csv')
# # data_sim.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' +  str(years_sim) + 'yrs_sim_intensity_return_periods_europe.csv')
# data_sim.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' + str(years_sim) + 'yrs_sim_intensity_return_periods_portugal.csv')


#################################
# HEAT WAVE DURATION EUROPE-WIDE (all data)
#################################

# obs_data_processed = seasonal_hw_duration_summary_europe(obs_data, obs_data, season_start, season_end, percentile)
#
# # take sample of XX years from sim_data_1 (TEMPORARY)
# sim_data_1_subset = sim_data_1
#
# sim_data_processed = seasonal_hw_duration_summary_europe(obs_data, sim_data_1_subset, season_start, season_end, percentile)
# # sim_data_processed = seasonal_hw_duration_summary_europe(obs_data, sim_data_combined, season_start, season_end, percentile)
#
# # create duration characteristics for each site
# data_obs = hw_duration_return_periods_europe(obs_data_processed)
# data_sim = hw_duration_return_periods_europe(sim_data_processed)
#
# # save to csv
# data_obs.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_obs_intensity_return_periods_europe.csv')
# # data_sim.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' +  str(years_sim) + 'yrs_sim_intensity_return_periods_europe.csv')
# data_sim.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_4000yrs_sim_intensity_return_periods_europe.csv')

#################################
# HEAT WAVE DURATION EUROPE-WIDE (30-year chunks)
#################################

# # create empty frame to populate with subset values
# data_avg = pd.DataFrame(columns=['days_over', 'return_period', 'subset'])
#
# # loop through subsets to get some heat wave return periods
# for subset in range(0, int(np.floor(sim_data_1.shape[1]/30))):
#
#     # print subset
#     print(subset)
#
#     # take sample of 30 years from sim_data_1 recursively
#     sim_data_1_subset = sim_data_1[:,range(30*subset,(30*(subset+1))),:]
#
#     sim_data_processed_temp = seasonal_hw_duration_summary_europe(obs_data, sim_data_1_subset, season_start, season_end, percentile)
#
#     # create duration characteristics for each site
#     data_sim_temp = hw_duration_return_periods_europe(sim_data_processed_temp)
#
#     # convert into pandas dataframe
#     data_sim_temp = pd.DataFrame(data_sim_temp)
#     data_sim_temp['subset'] = subset + 1
#
#     # concatenate to master file
#     data_avg = pd.concat([data_avg.reset_index(drop=True), data_sim_temp.reset_index(drop=True)], axis=0)
#
#
# # save to csv
# data_avg.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_30yrs_subsets_4000yrs_sim_intensity_return_periods_europe.csv',index=False)

#################################
# HEAT WAVE DURATION UK
#################################

# # UK first of all
# # lonlat.loc[lonlat['country']] == 'UK'
# # UK_values = [66,79,80,81,84,95,96,97,98,99,100,101,102,103,115,116,117,118,119,120,121,122,123,124,135,136,137,138,139,
# #              140,141,142,143,144,154,155,156,157,167]
#
# # take footprint of country TO FINISH
# obs_data_site = obs_data[UK_values,:,:]
#
# obs_data_processed_site = seasonal_hw_duration_summary_europe(obs_data_site, obs_data_site, season_start, season_end, percentile)
#
# # take sample of XX years from sim_data_1 (TEMPORARY)
# sim_data_1_subset = sim_data_1[UK_values,:,:]
#
# sim_data_processed_site = seasonal_hw_duration_summary_europe(obs_data_site, sim_data_1_subset, season_start, season_end, percentile)
# # sim_data_processed = seasonal_hw_duration_summary_europe(obs_data, sim_data_combined, season_start, season_end, percentile)
#
# # create duration characteristics for each site
# data_obs = hw_duration_return_periods_europe(obs_data_processed_site)
# data_sim = hw_duration_return_periods_europe(sim_data_processed_site)
#
# # save to csv
# data_obs.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_obs_intensity_return_periods_uk.csv')
# # data_sim.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' +  str(years_sim) + 'yrs_sim_intensity_return_periods_europe.csv')
# data_sim.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_4000yrs_sim_intensity_return_periods_uk.csv')

#################################
# HEAT WAVE DURATION UK (30-year chunks)
#################################

# # create empty frame to populate with subset values
# data_avg = pd.DataFrame(columns=['days_over', 'return_period', 'subset'])
#
# # loop through subsets to get some heat wave return periods
# for subset in range(0, int(np.floor(sim_data_1.shape[1]/30))):
#
#     # print subset
#     print(subset)
#
#     # take sample of 30 years from sim_data_1 recursively
#     sim_data_1_subset_subset = sim_data_1_subset[:,range(30*subset,(30*(subset+1))),:]
#
#     sim_data_processed_temp = seasonal_hw_duration_summary_europe(obs_data_site, sim_data_1_subset_subset, season_start, season_end, percentile)
#
#     # create duration characteristics for each site
#     data_sim_temp = hw_duration_return_periods_europe(sim_data_processed_temp)
#
#     # convert into pandas dataframe
#     data_sim_temp = pd.DataFrame(data_sim_temp)
#     data_sim_temp['subset'] = subset + 1
#
#     # concatenate to master file
#     data_avg = pd.concat([data_avg.reset_index(drop=True), data_sim_temp.reset_index(drop=True)], axis=0)
#
#
# # save to csv
# data_avg.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_30yrs_subsets_4000yrs_sim_intensity_return_periods_uk.csv',index=False)

# BELOW TO FINISH

#################################
# HEAT WAVE DURATION BY SITE
#################################
#
# # processing seasonal percentiles and then calculating number of consecutive days over it for observed data
# obs_data_processed = seasonal_hw_duration_summary(obs_data, obs_data, season_start, season_end, percentile)
#
# # processing seasonal percentiles and then calculating number of consecutive days over it for simulated data
# sim_data_processed = seasonal_hw_duration_summary(obs_data, sim_data_combined, season_start, season_end, percentile)
#
# # create duration characteristics for each site
# data_obs = hw_duration_return_periods(obs_data_processed)
# data_sim = hw_duration_return_periods(sim_data_processed)
#
# # save to csv
# data_obs.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_sim_intensity_return_periods.csv')
# data_sim.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' +  str(years_sim) + 'yrs_sim_intensity_return_periods.csv')

# need to create heatwave duration characteristics for each footprint instead of each site

#################################
# HEAT WAVE INTENSITY
#################################

# # processing monthly means for the CORDEX sim data
# # with summary statistics for the entire period and for ensembles chunks
# sim_data_processed_all, sim_data_processed_ens = monthly_summary(sim_data, 30, 1)
# obs_data_processed.columns = ['mean_value_obs', 'month', 'sd_value_obs', 'site']
# sim_data_processed_all.columns = ['mean_value_sim', 'month', 'sd_value_sim', 'site']
#
# # combine two tables of complete values
# obs_sim_data_processed = pd.merge(obs_data_processed, sim_data_processed_all)
#
# # output to merged obs and sim values to csv
# obs_sim_data_processed.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' + str(years_sim) + 'yrs_' + '_obs_sim_merged.csv')
# sim_data_processed_ens.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' + str(years_sim) + 'yrs_' + '_sim_ens.csv')

#################################
# DROUGHT DURATION EUROPE-WIDE
#################################

# obs_data_processed = seasonal_drought_duration_summary_europe(obs_data, obs_data, season_start, season_end, 1)
#
# # take sample of 1000 years from sim_data_1 (TEMPORARY)
# # sim_data_1_subset = sim_data_1[:,range(0,1000),:]
#
# # sim_data_processed = seasonal_hw_duration_summary_europe(obs_data, sim_data_1_subset, season_start, season_end, percentile)
# sim_data_processed = seasonal_drought_duration_summary_europe(obs_data, sim_data_1_subset, season_start, season_end, 1)
#
# # create duration characteristics for each site
# data_obs = hw_duration_return_periods_europe(obs_data_processed)
# data_sim = hw_duration_return_periods_europe(sim_data_processed)
#
# # save to csv
# data_obs.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_obs_drought_intensity_return_periods_europe.csv')
# # data_sim.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' +  str(years_sim) + 'yrs_sim_intensity_return_periods_europe.csv')
# data_sim.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_1000yrs_sim_drought_intensity_return_periods_europe.csv')
