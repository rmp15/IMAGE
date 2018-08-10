# this script
# processes monthly percentile means for the CORDEX input data
# processes monthly means for the total length of the IMAGE data
# processes monthly means for each of the 30-year ensembles of IMAGE data

from prog.functions.data.process_clag_stats_functions import *
import sys
from scipy.stats import rankdata
import scipy.io

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

# load lon/lat data for European
lons = scipy.io.loadmat(os.path.join(cordex_output_local,'euro_cordex','lonlat/nobc_lons.mat'))
lons_array = np.array(lons[list(lons.keys())[3]])
lats = scipy.io.loadmat(os.path.join(cordex_output_local,'euro_cordex','lonlat/nobc_lats.mat'))
lats_array = np.array(lats[list(lats.keys())[3]])
lonlat = pd.DataFrame(pd.concat([lons_array, lats_array]))

# loading data for both observations and simulations
obs_data, sim_data_1 = load_clag_output(slice, years_sim_1, continent, scen, year_start, year_end, metric)
obs_data, sim_data_2 = load_clag_output(slice, years_sim_2, continent, scen, year_start, year_end, metric)

# combine two sets of simulations (must be a faster way?) (check out numpy.stack
sim_data_combined = np.empty([no_sites,(years_sim_1+years_sim_2),365])
for i in range(0, no_sites):
    for j in range(0,365):
        sim_data_combined[i,:,j] = np.concatenate((sim_data_1[i,:,j], sim_data_2[i,:,j]), axis=0)


#################################
# HEAT WAVE DURATION
#################################

# processing seasonal percentiles and then calculating number of consecutive days over it for observed data
obs_data_processed = seasonal_hw_duration_summary(obs_data, obs_data, season_start, season_end, percentile)

# processing seasonal percentiles and then calculating number of consecutive days over it for simulated data
sim_data_processed = seasonal_hw_duration_summary(obs_data, sim_data_combined, season_start, season_end, percentile)

# generate return periods based on results for observed and simulated data
# return period = (n+1)/m, where n=number of years in data set, m=rank of
def hw_duration_return_periods(data):
    data_master = pd.DataFrame()
    for j in range(0, data.shape[1]):
        # for each location, generate a probability rank, where lowest number is lowest ranked
        rank_data = len(data[:, j]) + 1 - rankdata(data[:, j], method='min')

        # calculate return period
        return_period = (len(data[:, j]) + 1) / rank_data

        # collect values of heat wave intensity and return period for each location
        data_current = pd.DataFrame({'site': (j + 1), 'days_over': np.unique(data[:, j]),
                                     'return_period': np.unique(return_period)})
        data_master = pd.concat([data_master.reset_index(drop=True), data_current.reset_index(drop=True)], axis=0)
        # data_master.append(data_current, ignore_index=True)

    return data_master

# create duration characteristics for each site
data_obs = hw_duration_return_periods(obs_data_processed)
data_sim = hw_duration_return_periods(sim_data_processed)

# save to csv
data_obs.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_sim_intensity_return_periods.csv')
data_sim.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' +  str(years_sim) + 'yrs_sim_intensity_return_periods.csv')

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
