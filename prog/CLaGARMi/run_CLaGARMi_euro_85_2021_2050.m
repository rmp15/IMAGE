% Loads Euro CORDEX rcp8.5 2021-2050 data and then runs CLaGARMi

clear

addpath('../../data/CORDEX_nobc_clagarm_input/')
addpath('../../prog/CLaGARMi/v1')

% fix the following
load data/CORDEX_nobc_clagarm_input/tasmax_MPI_nobc_8520212050.mat
mv(1)=v;
load data/CORDEX_nobc_clagarm_input/appt_MPI_nobc_8520212050.mat
mv(2)=v;
clear v
sroot='~/data/IMAGE/CLaGARMi/euro_cordex/';
% ClaGARMi will save its output in 'sroot' folder, also AR fits and Cholesky
% decomp of AR fits get saved her for improved re-run time

%validateInputData(mv); %I never really developed this validation so skip it.

nyrs=300; % simulation length
nmnths=12; % no 'months' per year
niters=10; % no. iterations on residual convariance matrix
split=1; %used to split very long runs into smaller chunks
savefilename = strcat(sroot,'out_',num2str(split,'%02d'),'_y',int2str(nyrs),'_euro_85_2021_2050');

tic
mv=CLaGARMi(nyrs,nmnths,niters,mv,sroot);
toc

disp('Saving...');
save(savefilename,'mv','-v7.3');


%% 
% quick check of intra variable correlations to demonstrate effect of
% iteration, compare nIter=1 to 10
i=3;
o=mv(i).o;
s=mv(i).s;
o=reshape(o,[],size(o,3));
s=reshape(s,[],size(s,3));
oc=corr(o);
sc=corr(s);
plot(oc(:),sc(:),'k.');
