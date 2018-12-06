# this script
# processes apparent temperature values

from prog.functions.data.process_clag_stats_functions import *
import sys
import hdf5storage


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

metric = 'appt'

print('loading data for tasmax, huss and ps')

# loading data for both observations and simulations

tas_obs_data,  tas_sim_data = load_clag_output(slice, years_sim, continent, scen, year_start, year_end, 'tasmax')
print('tasmax loaded')

huss_obs_data, huss_sim_data = load_clag_output(slice, years_sim, continent, scen, year_start, year_end, 'huss')
print('huss loaded')

ps_obs_data, ps_sim_data = load_clag_output(slice, years_sim, continent, scen, year_start, year_end, 'ps')
print('ps loaded')

# process apparent temperature
print('processing apparent temperature')
appt_obs_data = app_temp_creator(tas_obs_data, huss_obs_data, ps_obs_data)
appt_sim_data = app_temp_creator(tas_sim_data, huss_sim_data, ps_sim_data)


# names for output files
fn_o = 'appt/out_' + slice + '_y' + str(years_sim) + '_' + continent + '_' + str(scen) + '_' + str(
    year_start) + '_' + str(year_end) + '_appt_o.mat'
fn_s = 'appt/out_' + slice + '_y' + str(years_sim) + '_' + continent + '_' + str(scen) + '_' + str(
    year_start) + '_' + str(year_end) + '_appt_s.mat'

# save files
print('saving files')
np.save(os.path.join(image_output_local, fn_o), appt_obs_data)
np.save(os.path.join(image_output_local, fn_s), appt_sim_data)

print('complete')

# # processing monthly means for the CORDEX observation data
# obs_data_processed = monthly_summary(appt_obs_data, 30, 0)
#
# # processing monthly means for the CORDEX sim data
# # with summary statistics for the entire period and for ensembles chunks
# sim_data_processed_all, sim_data_processed_ens = monthly_summary(appt_sim_data, 30, 1)
# obs_data_processed.columns = ['mean_value_obs', 'month', 'sd_value_obs', 'site']
#
# sim_data_processed_all.columns = ['mean_value_sim', 'month', 'sd_value_sim', 'site']
#
# # combine two tables of complete values
# obs_sim_data_processed = pd.merge(obs_data_processed, sim_data_processed_all)
#
# # output to merged obs and sim values to csv
# obs_sim_data_processed.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' + str(years_sim) + 'yrs_' + '_obs_sim_merged.csv')
# sim_data_processed_ens.to_csv('~/git/IMAGE/output/CLaGARMi/' + continent + '_cordex/figures_processing/' + metric + '_' + continent + '_' + scen + '_' + str(year_start) + '_' + str(year_end) + '_' + str(years_sim) + 'yrs_' + '_sim_ens.csv')
