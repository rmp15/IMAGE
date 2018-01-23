from prog.functions.data.data_tools import *
from data.objects import *

# station ids for brazil
weather_stations_brazil = ['83589CMatoDentro', '86781Diamantina']
stations_brazil = ['1843002', '1943003', '1943025', '1943035']

# elnino metrics
elninos = ['nino12a', 'nino3a', 'nino3.4a', 'nino4a', 'soi_a']

# years of analysis for brazil
year_past_start = 1980
year_past_end = 2000
year_future_start_1 = 2030
year_future_end_1 = 2050
year_future_start_2 = 2040
year_future_end_2 = 2060

# list of years
years_past = list(range(year_past_start, year_past_end + 1))
years_future_1 = list(range(year_future_start_1, year_future_end_1 + 1))
years_future_2 = list(range(year_future_start_2, year_future_end_2 + 1))

# headers for ascii files from knmi
header_knmi_raw = ['Year', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# metric under observation
metrics = ('pr')
metric = 'pr'

# threshold value for zero precipitation NEED TO FINALISE WITH RALF
pr_threshold = 1

# gauges column names
col_names_gauges = ('gauge', 'date', str('total_' + metric), str('num_days_' + metric),
                    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14',
                    "15", '16', '17', '18', '19', '20', '21', '22', '23', '24', '25',
                    '26', '27', '28', '29', '30', '31')
weather_station_names = ('gauge', 'date', 'time', 'pr', 'tmax', 'tmin')

# gauges chosen columns
col_chosen_gauges = (0, 2, 5, 7, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                     27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43)
weather_station_chosen_gauges = (0, 1, 2, 3, 4, 5)

# month values
month_numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

# column names for building elnino metrics
r_names = ['station', 'elnino_metric', 'month', 'n', 'r_value', 'p_value']

# treshold for number of days to drop to leave out a month
threshold_drop_days = 5

# relative lengths of months
day_months_long = [1, 3, 5, 7, 8, 10, 12]
day_months_medium = [4, 6, 8, 11]
day_months_short = [2]