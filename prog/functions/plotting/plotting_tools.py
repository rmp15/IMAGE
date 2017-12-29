import os

from ggplot import *

from prog.functions.data.data_tools import data_prep_knmi_scenarios


def plot_knmi_scenarios(metric, input, output, years1, years2, years3):
    """isolates years of data and finds the mean over a period of time
    then plots it
    """

    result = data_prep_knmi_scenarios(input, years1, years2, years3)

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
    print(output_path)
    os.makedirs(output_path, exist_ok=1)

    g.save(filename=os.path.join(output_path, metric + '_plot.pdf'))

