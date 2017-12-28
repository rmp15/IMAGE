from prog.functions.data.data_tools import *

# station ids for brazil
stations_brazil = ['1843002', '1943003', '1943025', '1943035']

# years of analysis for brazil
year_past_start = 1981
year_past_end = 2010
year_future_start_1 = 2030
year_future_end_1 = 2050
year_future_start_2 = 2040
year_future_end_2 = 2060

# list of years
years_past = list(range(year_past_start, year_past_end+1))
years_future_1 = list(range(year_future_start_1, year_future_end_1+1))
years_future_2 = list(range(year_future_start_2, year_future_end_2+1))

# headers for ascii files from knmi
header_knmi_raw = ['Year', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# metric under observation
metric = 'pr'