import os
import glob
from ggplot import *
from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
from data.objects.objects import *
from prog.functions.plotting.plotting_tools import plot_knmi_scenarios_monthly_over_time
from scipy.stats import linregress

# this file
# loads the monthly scaled values of precipitation and the scaled values of number of days above 1mm of rainfall
# and then plots them against each other for each climate scenario
# create locations for the files
file_paths = [os.path.join(minas_knmi_climate_output, 'minas_brazil', i) for i in stations_brazil]

j = 3

# load monthly values for scaled by 2040-2060 ratio
path = os.path.join(file_paths[j], 'pr_real_values_scaled_20402060_to_19802000_ratio.csv')
print(path)
dat_monthly = pd.read_csv(str(path))

# test to only include months from chosen years
#dat_monthly = dat_monthly[dat_monthly['year'].isin(years_past)]

# remove duplicate rows
dat_monthly = dat_monthly.drop_duplicates(subset=['month', 'year'], keep='first')

df_master = pd.DataFrame(columns=r_names_2)

# where to adjust threshold (loop over this) when finished
for current_threshold in list(np.arange(0.1, 10.1, 0.1)):
    dat_monthly['num_days_pr_scenario'] = dat_monthly.iloc[:, 4:35][dat_monthly.iloc[:, 4:35] >= current_threshold].count(axis=1)
    #
    # sum over years
    data_monthly = pd.DataFrame(dat_monthly.groupby(by=["year"])['num_days_pr_scenario'].sum())
    data_monthly['year'] = data_monthly.index

    # load yearly values FOR 2040
    path = os.path.join(file_paths[j], 'r1mm_real_values_yearly_scaled_to_2030_2040.csv')
    dat_yearly = pd.read_csv(str(path))

    dat_monthly_yearly_merged = pd.merge(data_monthly, dat_yearly)

    # test to only include chosen years
    #dat_monthly_yearly_merged = dat_monthly_yearly_merged[dat_monthly_yearly_merged['year'].isin(years_past)]

    print(dat_monthly_yearly_merged.head())

    slope, intercept, r_value, p_value, std_err = linregress(dat_monthly_yearly_merged['num_days_pr_scenario'],
                                                               dat_monthly_yearly_merged['num_days_pr_2040'])

    # finish to create data frame
    #df_append = pd.DataFrame([[j, current_threshold, slope, r_value, p_value]], columns=r_names_2)
    #df_append['sig'] = np.where(df_append['p_value'] <= 0.05, 1, 0)
    #print(df_append)
    #df = df.append(df_append)

    # plot by month over the time periods
    g = ggplot(dat_monthly_yearly_merged, aes(x='num_days_pr_scenario', y='num_days_pr_2040')) + \
        geom_point() + \
        xlab('1980-2000 monthly method yearly sum') +\
        ylab('1980-2000 yearly method yearly sum ') + \
        xlim(low=0,high=300) + \
        ylim(low=0,high=300) + \
        geom_abline(a=1) + \
        ggtitle(stations_brazil[j] + ': number of wet days, precipitation threshold = ' + str(current_threshold) + ' mm' +
                ', slope = ' + str(round(slope,2)) +
                ', R= ' + str(round(r_value, 2)) +
                ', p = ' + str(round(p_value,3))) + \
        theme_bw()

    # create recursive directory
    output_path = os.path.join(minas_knmi_climate_output,'minas_brazil', stations_brazil[j], 'yearly_monthly_thresholds')
    recursive_directory(output_path)
    print(output_path)

    print(metric)
    g.save(filename=os.path.join(output_path, stations_brazil[j] +
                                 '_threshold_'+ str(current_threshold) +
                                 'mm_wet_days_yearly_against_monthly_method_plot.pdf'))