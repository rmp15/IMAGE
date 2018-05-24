% test multi var input validation func.
clear
% % load Pressure_l45_y60
% % load Tmin_l45_y60
% %  load ObsData/Wong_l50_y30
% load ObsData/Wong_l196_y30
% % load ATRD_l58_y401
% % load Tmin_l50_y30
% vin1=v;
%%mv=v;

for scen = 2:5
    clearvars -except scenario_years scen
    model_name = '_MPI_nobc'
    scen_name = {'_hist19712000','_4520212050','_8520212050','_4520712100','_8520712100'}
    scenario_years = strcat(model_name,scen_name{1,scen})

    
   
variable_names = {'tasmax','appt','tas','tdps'}

for i = 1:2

        file_name = strcat(variable_names{1,i},scenario_years,'.mat')
        load(file_name)
        mv(i)=v;
        mv(i).o = v.o(:,:,:);


end

file_leader = strcat('nobc_10k', '_')

hashfilename = strcat('nobc_10k_','EUR_hw_',scenario_years);
savefilename = strcat(file_leader,'EUR_hw_',scenario_years);
%  load ObsData/Tmax_l163_y65_22x15
%  mv(2)=v;
% load ObsData/Rain_l152_y65_22x15
% mv(3)=v;

% load ObsData/SE_Tmin_l115_y65_14x12
% mv(1)=v;
% load ObsData/SE_Tmax_l115_y65_14x12
% mv(2)=v;
% load ObsData/SE_Rain_l115_y65_14x12
% mv(3)=v;

clear v
validateInputData(mv);

tic
rng default
[mv]=CLaGARM_nohash(10000,12,mv,hashfilename);
disp('Saving...');

save(savefilename,'mv','-v7.3');

tasmax_s_fn = strcat('10k_',scenario_years,'tasmax_s_',savefilename);
tasmax_o_fn = strcat('10k_',scenario_years,'tasmax_o_',savefilename);
appt_s_fn = strcat('10k_',scenario_years,'appt_s_',savefilename);
appt_o_fn = strcat('10k_',scenario_years,'appt_o_',savefilename);
tasmax_s = mv(1).s(121:273,:,:);
tasmax_o = mv(1).o(121:273,:,:);
save(tasmax_s_fn,'tasmax_s','-v7.3');
save(tasmax_o_fn,'tasmax_o','-v7.3');

appt_s = mv(2).s(121:273,:,:);
appt_o = mv(2).o(121:273,:,:);
save(appt_s_fn,'appt_s','-v7.3');
save(appt_o_fn,'appt_o','-v7.3');
%save(['v3out/out_wong_shuf_ll'],'mv','-v7.3');
%save(['v3out/out_wong50_shuf_ll'],'mv','-v7.3');
toc
clear mv
end
