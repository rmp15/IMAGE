import os

from ggplot import *

from prog.functions.data.data_tools import *


def plot_knmi_scenarios_monthly_over_time(metric, input, output, years1, years2, years3):
    """isolates years of data and finds the mean over a period of time
    then plots it
    """

    result = data_prep_knmi_scenarios_monthly(metric, input, output, years1, years2, years3)

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

    g.save(filename=os.path.join(output_path, metric + '_plot_over_time.pdf'))


def plot_knmi_scenarios_scale_factors(metric, input, output, years1, years2, years3):
    """isolates years of data and plots the scale factors between sets of years
    """

    result = pd.read_csv(os.path.join(output, metric + '_mean_scale_factors_' +
                                 str(years1[0]) + str(years1[-1]) + '_' +
                                 str(years2[0]) + str(years2[-1]) + '_' +
                                 str(years3[0]) + str(years3[-1]) + '.csv'))

    # throw away unimportant columns
    result['month'] = result.iloc[:, 2]
    result['month_number'] = result.index + 1
    result = result.iloc[:, 8:12]

    print(result)

    # names of columns
    string_1 = str(years2[0]) + str(years2[-1]) + '_to_' + str(years1[0]) + str(years1[-1])
    string_2 = str(years3[0]) + str(years3[-1]) + '_to_' + str(years1[0]) + str(years1[-1])
    string_name_list = [string_1, string_2]
    col_name_1 = string_1 + '_percdelta'
    col_name_2 = string_2 + '_percdelta'
    col_name_list = [col_name_1, col_name_2]

    # plot by month over the two comparison time periods
    for i in range(0,1+1):

        g = ggplot(result, aes(x='month_number', y=col_name_list[i])) + \
            geom_point() + \
            geom_hline(y=0) + \
            xlab('Month') + \
            ylab('Percentage change') + \
            ylim(low=-25, high=25) + \
            ggtitle('Percentage change in ' + metric + ' from ' + string_name_list[i])

        # create recursive directory
        output_path = output
        recursive_directory(output_path)
        print(output_path)

        g.save(filename=os.path.join(output_path, metric + '_' + col_name_list[i] + '_plot.pdf'))


def plot_knmi_scenarios_abs_change(metric, input, output, years1, years2, years3):
    """isolates years of data and plots the scale factors between sets of years
    """

    result = pd.read_csv(os.path.join(output, metric + '_mean_abs_diff_' +
                                 str(years1[0]) + str(years1[-1]) + '_' +
                                 str(years2[0]) + str(years2[-1]) + '_' +
                                 str(years3[0]) + str(years3[-1]) + '.csv'))

    # throw away unimportant columns
    result['month'] = result.iloc[:, 2]
    result['month_number'] = result.index + 1
    result = result.iloc[:, 6:10]

    print(result)

    # names of columns
    string_1 = str(years2[0]) + str(years2[-1]) + '_to_' + str(years1[0]) + str(years1[-1])
    string_2 = str(years3[0]) + str(years3[-1]) + '_to_' + str(years1[0]) + str(years1[-1])
    string_name_list = [string_1, string_2]
    col_name_1 = string_1 + '_diff'
    col_name_2 = string_2 + '_diff'
    col_name_list = [col_name_1, col_name_2]

    # plot by month over the two comparison time periods
    for i in range(0, 1+1):

        g = ggplot(result, aes(x='month_number', y=col_name_list[i])) + \
            geom_point() + \
            geom_hline(y=0) + \
            xlab('Month') + \
            ylab('Absolute change') + \
            ylim(low=0, high=3) + \
            ggtitle('Absolute change in ' + metric + ' from ' + string_name_list[i])

        # create recursive directory
        output_path = output
        recursive_directory(output_path)
        print(output_path)

        g.save(filename=os.path.join(output_path, metric + '_' + col_name_list[i] + '_plot.pdf'))


def plot_knmi_scenarios_yearly(metric, input, output, years1, years2, years3):
    """isolates years of data and finds the mean over a period of time
    then plots it
    """

    result = data_prep_knmi_scenarios_monthly(metric, input, output, years1, years2, years3)

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

    result = data_prep_knmi_scenarios_monthly(metric, input, output, years1, years2, years3)

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

def plot_correlation_elnino(metric, elnino, input, output,):
    """chooses a el nino metric and plots the output of the scaled values
    """

    # load el nino metric
    metric = pd.read_csv(ps.path.join(elnino,'tsiersst_'))

    # merge el nino metric with the weather variable for each month

