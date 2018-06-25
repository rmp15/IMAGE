% Loads Euro CORDEX historical data and then runs CLaGARMi

clear

addpath('~/git/IMAGE/prog/01_extract_files/');
addpath('../../data/CORDEX_nobc_clagarm_input/')
addpath('../../prog/CLaGARMi/v1')

% fix the following
load /home/rmp15/data/IMAGE/CORDEX/euro_cordex/tasmax/processed/tasmax_MPI-M-MPI-ESM-LR_historical_r2i1p1_MPI-CSC-REMO2009_v119712000.mat
mv(1)=v;
load /home/rmp15/data/IMAGE/CORDEX/euro_cordex/huss/processed/huss_MPI-M-MPI-ESM-LR_historical_r2i1p1_MPI-CSC-REMO2009_v119712000.mat
mv(2)=v;
load /home/rmp15/data/IMAGE/CORDEX/euro_cordex/sfcWindmax/processed/sfcWindmax_MPI-M-MPI-ESM-LR_historical_r2i1p1_MPI-CSC-REMO2009_v119712000.mat
mv(3)=v;
clear v
sroot='~/data/IMAGE/CLaGARMi/euro_cordex/';
% ClaGARMi will save its output in 'sroot' folder, also AR fits and Cholesky
% decomp of AR fits get saved her for improved re-run time

nyrs=300; % simulation length
nmnths=12; % no 'months' per year
niters=10; % no. iterations on residual convariance matrix
split=1; %used to split very long runs into smaller chunks
savefilename = strcat(sroot,'out_',num2str(split,'%02d'),'_y',int2str(nyrs),'_euro_hist_1971_2000');

tic
mv=CLaGARMi(nyrs,nmnths,niters,mv,sroot);
toc

disp('Saving...');
save(savefilename,'mv','-v7.3');

% save individual outputs of variables
% GENERALISE TO ANY VARIABLE NAMEAS IT'S CLUMSY RIGHT NOW
tasmax_s_fn = strcat(savefilename,'_tasmax_s');
tasmax_o_fn = strcat(savefilename,'_tasmax_o');
tasmax_s = mv(1).s;
tasmax_o = mv(1).o;
save(tasmax_s_fn,'tasmax_s','-v7.3');
save(tasmax_o_fn,'tasmax_o','-v7.3');

appt_s_fn = strcat(savefilename,'_appt_s');
appt_o_fn = strcat(savefilename,'_appt_o');
appt_s = mv(2).s;
appt_o = mv(2).o;
save(appt_s_fn,'appt_s','-v7.3');
save(appt_o_fn,'appt_o','-v7.3');


%% 
% quick check of intra variable correlations to demonstrate effect of
% iteration, compare nIter=1 to 10
%i=3;
%o=mv(i).o;
%s=mv(i).s;
%o=reshape(o,[],size(o,3));
%s=reshape(s,[],size(s,3));
%oc=corr(o);
%sc=corr(s);
%plot(oc(:),sc(:),'k.');
