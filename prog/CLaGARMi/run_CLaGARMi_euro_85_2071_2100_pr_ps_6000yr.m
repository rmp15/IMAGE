% Loads Euro CORDEX historical data and then runs CLaGARMi

clear

addpath('~/git/IMAGE/prog/01_extract_files/');
addpath('../../data/CORDEX_nobc_clagarm_input/')
addpath('../../prog/CLaGARMi/v1')

% loading process
load /home/rmp15/data/IMAGE/CORDEX/euro_cordex/pr/processed/pr_MPI-M-MPI-ESM-LR_rcp85_r2i1p1_MPI-CSC-REMO2009_v120712100.mat
mv(1)=v;
load /home/rmp15/data/IMAGE/CORDEX/euro_cordex/ps/processed/ps_MPI-M-MPI-ESM-LR_rcp85_r2i1p1_MPI-CSC-REMO2009_v120712100.mat
mv(2)=v;
clear v

% ClaGARMi will save its output in 'sroot' folder, also AR fits and Cholesky
% decomp of AR fits get saved her for improved re-run time
sroot='~/data/IMAGE/CLaGARMi/euro_cordex_output/';

output_label='pr_ps';

nyrs=6000; % simulation length
nmnths=12; % no 'months' per year
niters=10; % no. iterations on residual convariance matrix
split=1; %used to split very long runs into smaller chunks
savefilename = strcat('out_',num2str(split,'%02d'),'_y',int2str(nyrs),'_euro_rcp85_2021_2050_',output_label);

scen        = 'hist';
starty      = '2021';
endy        = '2050';
var_names   = 'pr_ps';

tic
mv=CLaGARMi(nyrs,nmnths,niters,mv,sroot,scen,starty,endy,var_names);
toc

disp('Saving...');
save(strcat(sroot,'combined_output/',savefilename),'mv','-v7.3');

% reuse savefilename for the isolated outputs
savefilename = strcat('out_',num2str(split,'%02d'),'_y',int2str(nyrs),'_euro_rcp85_2021_2050');

% save individual outputs of variables
pr_s_fn = strcat(sroot,'pr/',savefilename,'_pr_s');
pr_o_fn = strcat(sroot,'pr/',savefilename,'_pr_o');
pr_s = mv(1).s;
pr_o = mv(1).o;
save(pr_s_fn,'pr_s','-v7.3');
save(pr_o_fn,'pr_o','-v7.3');

ps_s_fn = strcat(sroot,'ps/',savefilename,'_ps_s');
ps_o_fn = strcat(sroot,'ps/',savefilename,'_ps_o');
ps_s = mv(2).s;
ps_o = mv(2).o;
save(ps_s_fn,'ps_s','-v7.3');
save(ps_o_fn,'ps_o','-v7.3');