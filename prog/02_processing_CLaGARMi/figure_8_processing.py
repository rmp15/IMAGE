# this script
# processes monthly percentile means for the CORDEX input data
# processes monthly means for the total length of the IMAGE data
# processes monthly means for each of the 30-year ensembles of IMAGE data

from prog.functions.data.process_clag_stats_functions import *
import sys
from scipy.stats import rankdata

# get total number of arguments
total = len(sys.argv)

# get the arguments list
cmdargs = str(sys.argv)

# variables for processing CLaGARMi output
slice = sys.argv[1]                             # slice = '01'
years_sim = int(float((sys.argv[2])))           # years_sim = 4000
metric = sys.argv[3]                            # metric = 'tasmax'
continent = sys.argv[4]                         # continent = 'euro'
scen = sys.argv[5]                              # scen = 'hist'
year_start = int(float((sys.argv[6])))          # year_start = 1971
year_end = int(float((sys.argv[7])))            # year_end = 2000
season_start = int(float((sys.argv[8])))        # season_start = 5
season_end = int(float((sys.argv[9])))          # season_end = 9
percentile = int(float((sys.argv[10])))         # percentile = 99

# loading data for both observations and simulations
obs_data, sim_data = load_clag_output(slice, years_sim, continent, scen, year_start, year_end, metric)

# processing seasonal percentiles and then calculating number of consecutive days over it for observed data
obs_data_processed = seasonal_hw_duration_summary(obs_data, obs_data, season_start, season_end, percentile)

# processing seasonal percentiles and then calculating number of consecutive days over it for simulated data
sim_data_processed = seasonal_hw_duration_summary(obs_data, sim_data, season_start, season_end, percentile)

# generate return periods based on results for observed and simulated data
# return period = (n+1)/m, where n=number of years in data set, m=rank of

# cycle through locations adding to dataframe for heat wave intensity for observed data
data_master = pd.DataFrame()
for j in range(0, no_sites):

    # for each location, generate a probability rank, where lowest number is lowest ranked
    rank_data = len(obs_data_processed[:, j]) + 1 - rankdata(obs_data_processed[:, j], method='min')

    # calculate return period
    return_period = (len(obs_data_processed[:, j])+1) / rank_data

    # collect values of heat wave intensity and return period for each location
    data_current = pd.DataFrame({'site': (j+1),'days_over':np.unique(obs_data_processed[:, j]),'return_period':np.unique(return_period)})
    data_master = pd.concat([data_master.reset_index(drop=True), data_current.reset_index(drop=True)], axis=0)
    # data_master.append(data_current, ignore_index=True)
    print(data_master.head())


data_master.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_obs_intensity_return_periods.csv')























# processing monthly means for the CORDEX sim data
# with summary statistics for the entire period and for ensembles chunks
sim_data_processed_all, sim_data_processed_ens = monthly_summary(sim_data, 30, 1)
obs_data_processed.columns = ['mean_value_obs', 'month', 'sd_value_obs', 'site']
sim_data_processed_all.columns = ['mean_value_sim', 'month', 'sd_value_sim', 'site']

# combine two tables of complete values
obs_sim_data_processed = pd.merge(obs_data_processed, sim_data_processed_all)

# output to merged obs and sim values to csv
obs_sim_data_processed.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' + str(years_sim) + 'yrs_' + '_obs_sim_merged.csv')
sim_data_processed_ens.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' + str(years_sim) + 'yrs_' + '_sim_ens.csv')
