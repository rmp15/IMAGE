# this script
# processes monthly means for the CORDEX input data
# processes monthly means for the total length of the IMAGE data
# processes monthly means for each of the 30-year ensembles of IMAGE data

from prog.functions.data.process_clag_stats_functions import *

# loading data for both observations and simulations
obs_data, sim_data = load_clag_output('01', 300, 'euro', 'hist', 1971, 2000, 'tasmax')

# processing monthly means for the CORDEX observation data
obs_data_processed = monthly_summary(obs_data, 30, 0)
sim_data_processed = monthly_summary(sim_data, 30, 0)
obs_data_processed.columns = ['month', 'site', 'value_obs']
sim_data_processed.columns = ['month', 'site', 'value_sim']

# combine two tables temporarily
obs_sim_data_processed = pd.merge(obs_data_processed,sim_data_processed)

# output to csv
obs_sim_data_processed.to_csv(os.path.join('test.csv'))