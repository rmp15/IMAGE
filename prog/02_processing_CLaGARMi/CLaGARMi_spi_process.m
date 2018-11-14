% this program
% takes output of CLaGARMi
% calculates SPI for each site

% go to correct directory
cd '~/data/IMAGE/CLaGARMi/euro_cordex_output/pr/'

% load fiveyear_filereader for processing CORDEX files
addpath('~/git/IMAGE/prog/02_processing_CLaGARMi/');

% load the desired version of precipitation file
data= load('out_01_y4000_euro_hist_1971_2000_pr_o') ;





