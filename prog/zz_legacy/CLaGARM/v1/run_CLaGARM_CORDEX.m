
scen = 1;
model_name = 'ICHEC_KNMI';
scen_name = {'_hist19701999','_4520202049','_8520202049','_4520702099','_8520702099'};
scenario_years = strcat(model_name,scen_name{1,scen});
path_root='/net/wrfstore6-10/disk1/srh110/Danube_CORDEX_input/';

split = 1;
clearvars -except split scenario_years scen path_root
variable_names = {'pr','rsds','tasmax','tasmin'};
hashfilename = scenario_years;
savefilename = strcat('out_',scenario_years);

for i = 1:4
    file_name =[path_root strcat(variable_names{1,i},scenario_years,'.mat')];
    load(file_name)
    mv(i)=v;
end

clear v
validateInputData(mv);
tic
savefilename = strcat(savefilename,int2str(split));
hashfilename = strcat(hashfilename,int2str(split));
rng default
mv=CLaGARM_nohash(1000,12,mv,hashfilename);
disp('Saving...');
%save(['out_eobs_SE_tntxrr_shuf_ll_XPX'],'mv','-v7.3');
save(savefilename,'mv','-v7.3');
toc
