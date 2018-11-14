# this script
# processes apparent temperature values

from prog.functions.data.process_clag_stats_functions import *
import sys
import scipy.stats as stats
import matplotlib.pyplot as plt
import standard_precip

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
pr_jja_mean_sim = seasonal_mean_calculator(pr_sim_data[:, 0:1000, :], 6, 8)

# number of sites to cycle through
no_sites = int(pr_jja_sum_obs.shape[0])

# for each site in the data
for i in range(0, no_sites):

    # calculate gamma fit parameters for each site
    fit_alpha, fit_loc, fit_beta = stats.gamma.fit(pr_jja_sum_obs[i, :])

    #  cycle through obs and sim to generate spi for each site
    x = np.linspace(0, 100, 200)
    y1 = stats.gamma.pdf(x, a=fit_alpha, scale=fit_beta)
    y2 = stats.gamma.cdf(x, a=fit_alpha, scale=fit_beta)
    plt.plot(x, y2)



# temporary save text
# np.savetxt('pr_jja_mean_obs.csv', pr_jja_mean_obs, delimiter=",")
# np.savetxt('pr_jja_mean_sim.csv', pr_jja_mean_sim, delimiter=",")

