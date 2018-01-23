import os
import glob
from ggplot import *
from prog.functions.data.data_tools import *
from data.file_paths.file_paths import *
from data.objects.objects import *
from prog.functions.plotting.plotting_tools import plot_knmi_scenarios_monthly_over_time
import pandas as pd
import numpy as np

# this file will plot the scaled daily values over the time period
def plot_scaled_data(metric, station):
    """chooses a time period and plots the output of the scaled values
    """

    file_path = os.path.join(minas_knmi_climate_output, 'minas_brazil', str(station),
                               metric + '_real_values_scaled_to_' + str(years_future_2[0]) + '_' +
                               str(years_past[0]) + '.csv')

    print(file_path)

    result = pd.read_csv(file_path)

    # plot by month over the time periods
    g = ggplot(result, aes(x='num_days_pr', y='num_days_pr_scenario')) + \
        geom_point() + \
        geom_abline(slope=1) + \
        xlim(low=0, high=35) + \
        ylim(low=0, high=35) + \
        ggtitle(metric + ' ' + station) +\
        facet_wrap('month') +\
        theme_bw()

    # create recursive directory
    output_path = os.path.join(minas_knmi_climate_output, 'minas_brazil', str(station),
                               metric + '_real_values_scaled_to_' + str(years_future_2[0]) + '_' +
                               str(years_past[0]) + '_scaled_drought_days_plot.pdf')
    g.save(filename=os.path.join(output_path))


    g = ggplot(result, aes(x='total_pr', y='total_pr_scenario')) + \
        geom_point() + \
        geom_abline(slope=1) + \
        xlim(low=0, high=200) + \
        ylim(low=0, high=200) + \
        ggtitle(metric + ' , ' + station) +\
    facet_wrap('month') + \
        theme_bw()

    # create recursive directory
    output_path = os.path.join(minas_knmi_climate_output, 'minas_brazil', str(station),
                               metric + '_real_values_scaled_to_' + str(years_future_2[0]) + '_' +
                               str(years_past[0]) + '_scaled_values_plot.pdf')
    g.save(filename=os.path.join(output_path))

for i in stations_brazil:
    plot_scaled_data(metric, i)


