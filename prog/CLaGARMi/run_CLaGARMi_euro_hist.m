% Loads Euro CORDEX historical data and then runs CLaGARMi

clear

addpath('~/git/IMAGE/prog/01_extract_files/');
addpath('../../data/CORDEX_nobc_clagarm_input/')
addpath('../../prog/CLaGARMi/v1')

var_names = {'tasmax','huss','sfcWindmax'};

% generalise loading process
load /home/rmp15/data/IMAGE/CORDEX/euro_cordex/tasmax/processed/tasmax_MPI-M-MPI-ESM-LR_historical_r2i1p1_MPI-CSC-REMO2009_v119712000.mat
mv(1)=v;
load /home/rmp15/data/IMAGE/CORDEX/euro_cordex/huss/processed/huss_MPI-M-MPI-ESM-LR_historical_r2i1p1_MPI-CSC-REMO2009_v119712000.mat
mv(2)=v;
load /home/rmp15/data/IMAGE/CORDEX/euro_cordex/sfcWindmax/processed/sfcWindmax_MPI-M-MPI-ESM-LR_historical_r2i1p1_MPI-CSC-REMO2009_v119712000.mat
mv(3)=v;
clear v

% ClaGARMi will save its output in 'sroot' folder, also AR fits and Cholesky
% decomp of AR fits get saved her for improved re-run time
sroot='~/data/IMAGE/CLaGARMi/euro_cordex_output/';

nyrs=300; % simulation length
nmnths=12; % no 'months' per year
niters=10; % no. iterations on residual convariance matrix
split=1; %used to split very long runs into smaller chunks
savefilename = strcat('out_',num2str(split,'%02d'),'_y',int2str(nyrs),'_euro_hist_1971_2000');

tic
mv=CLaGARMi(nyrs,nmnths,niters,mv,sroot);
toc

disp('Saving...');
save(strcat(sroot,'combined_output/',savefilename),'mv','-v7.3');

% save individual outputs of variables
tasmax_s_fn = strcat(sroot,'tasmax/',savefilename,'_tasmax_s');
tasmax_o_fn = strcat(sroot,'tasmax/',savefilename,'_tasmax_o');
tasmax_s = mv(1).s;
tasmax_o = mv(1).o;
save(tasmax_s_fn,'tasmax_s','-v7.3');
save(tasmax_o_fn,'tasmax_o','-v7.3');

huss_s_fn = strcat(sroot,'huss/',savefilename,'_huss_s');
huss_o_fn = strcat(sroot,'huss/',savefilename,'_huss_o');
huss_s = mv(2).s;
huss_o = mv(2).o;
save(huss_s_fn,'huss_s','-v7.3');
save(huss_o_fn,'huss_o','-v7.3');

sfcWindmax_s_fn = strcat(sroot,'sfcWindmax/',savefilename,'_huss_s');
sfcWindmax_o_fn = strcat(sroot,'sfcWindmax/',savefilename,'_huss_o');
sfcWindmax_s = mv(3).s;
sfcWindmax_o = mv(3).o;
save(sfcWindmax_s_fn,'sfcWindmax_s','-v7.3');
save(sfcWindmax_o_fn,'sfcWindmax_o','-v7.3');