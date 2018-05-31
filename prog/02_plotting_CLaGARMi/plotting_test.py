import scipy.io
from data.objects.objects import *
from data.file_paths.file_paths import *

section = '01'
year_num = 300
area = 'euro'
scenario = '45'
year_start = 2021
year_end = 2050

# CHECK THE BELOW LINK FOR HOW TO PLOT
# https://stackoverflow.com/questions/17316880/reading-v-7-3-mat-file-in-python

# get file paths for .mat output files
file_path = os.path.join(image_output_local, 'out_' + section + '_y' + str(year_num) + '_' + area + '_' + scenario +
                         '_' + str(year_start) + '_' + str(year_end) + '.mat')


# load files and perform analysis of average rainfall
data_real = scipy.io.loadmat(file_path)
