import os

from ggplot import *

from prog.functions.data.data_tools import *


def plot_knmi_scenarios(metric, input, output, years1, years2, years3):
    """isolates years of data and finds the mean over a period of time
    then plots it
    """

    result = data_prep_knmi_scenarios(metric, input, output, years1, years2, years3)

    # reshape data frame for plotting purposes
    result = result.unstack().reset_index()

    # rename columns (need to fix)
    result.columns = ['time', 'month', 'value']

    # plot by month over the time periods
    g = ggplot(result, aes(x='time', y='value', color='month')) + \
        geom_line() + \
        theme_bw()

    # create recursive directory
    output_path = output
    recursive_directory(output_path)

    g.save(filename=os.path.join(output_path, metric + '_plot.pdf'))

def plot_scaled_data(metric, input, output, years1, years2):
    """chooses a time period and plots the output of the scaled values
    """

    result = data_prep_knmi_scenarios(metric, input, output, years1, years2, years3)

    # reshape data frame for plotting purposes
    result = result.unstack().reset_index()

    # rename columns (need to fix)
    result.columns = ['time', 'month', 'value']

    # plot by month over the time periods
    g = ggplot(result, aes(x='time', y='value', color='month')) + \
        geom_line() + \
        theme_bw()

    # create recursive directory
    output_path = output
    recursive_directory(output_path)

    g.save(filename=os.path.join(output_path, metric + '_plot.pdf'))

