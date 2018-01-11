import os
import glob
from ggplot import *
from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
from data.objects.objects import *
from prog.functions.plotting.plotting_tools import plot_knmi_scenarios_monthly

# this file
# loads the monthly scaled values of precipitation and the scaled values of number of days above 1mm of rainfall
# and then plots them against each other for each climate scenario

# create locations for the files
file_paths = [os.path.join(minas_knmi_climate_output, 'minas_brazil', i) for i in stations_brazil]

j = 3
metric = 'r1mm'

# load monthly values FOR 2040
path = os.path.join(file_paths[j],'pr_real_values_scaled_to_2040_1981.csv')
print(path)
dat_monthly = pd.read_csv(str(path))

# sum over years
data_monthly = pd.DataFrame(dat_monthly.groupby(by=["year"])['num_days_pr_scenario'].sum())
data_monthly['year'] = data_monthly.index

print(data_monthly.head())

# load yearly values FOR 2040
path = os.path.join(file_paths[j],'r1mm_real_values_yearly_scaled_to_2030_2040.csv')
print(path)
dat_yearly = pd.read_csv(str(path))

print(dat_yearly.head())

dat_monthly_yearly_merged = pd.merge(data_monthly, dat_yearly)

print(dat_monthly_yearly_merged)

# plot by month over the time periods
g = ggplot(dat_monthly_yearly_merged, aes(x='num_days_pr_scenario', y='num_days_pr_2040')) + \
    geom_point() + \
    geom_abline(a=1) + \
    xlab('2040 monthly sum') +\
    ylab('2040 yearly scaled') + \
    ggtitle(stations_brazil[j]) + \
    theme_bw()

# create recursive directory
output_path = os.path.join(minas_knmi_climate_output,'minas_brazil', stations_brazil[j])
print(output_path)

print(metric)
g.save(filename=os.path.join(output_path, metric + '_plot.pdf'))

