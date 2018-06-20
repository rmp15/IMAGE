% go to correct directory
cd '~/data/IMAGE/CORDEX/euro_cordex/'

% load fiveyear_filereader for processing CORDEX files
addpath('~/git/IMAGE/prog/01_extract_files/');

% load the year start and end values
start_year = 2071
end_year = 2100
tot_years = end_year-start_year
sy_str = int2str(start_year)
ey_str = int2str(end_year)

% load the model details
model_grid = '_EUR-44'
gcm = '_MPI-M-MPI-ESM-LR'
scen = '_rcp45'
ens = '_r2i1p1'
rcm = '_MPI-CSC-REMO2009_v1'
time_res = '_day'

% not sure what this does at the moment...
soil_mois_test_file = strcat('../zz_legacy/mrso',model_grid,gcm,'_historical',ens,rcm,time_res,'_','19660101-19701231.nc')
soil_mois_test = ncread(soil_mois_test_file,'mrso');
soil_mois_day = soil_mois_test(:,:,1);

var_names = {'tasmax','huss'}
lbound = {NaN,0}
ubound = {NaN,NaN}

for vn = 1:2
    clear v
    var_name = var_names{vn}

    file_prefix = strcat(var_name,'/raw/',var_name,model_grid,gcm,scen,ens,rcm,time_res,'_')
    file_start_years = linspace(1951,2096,30);
    first_file_sy_i = max(find(file_start_years < start_year));
    first_file_sy = file_start_years(first_file_sy_i);
    first_file_ey = first_file_sy + 4;
    start_year_gap = start_year - first_file_sy;
    v.name = var_name
    v.lbound = lbound{vn}
    v.ubound = ubound{vn}
    v.gridded = 0
    v.sLat = 0
    v.sLon = 0
    v.dims = {'nDaysinYear','nYears','nLocations'}
    all_data = {}
    new_lons = []
    new_lats = []
    for j = 1:7
        sy = first_file_sy + ((j-1)*5);
        ey = first_file_ey + ((j-1)*5);
        filename = strcat(file_prefix,int2str(sy),'0101-',int2str(ey),'1231.nc')

        [new_lons, new_lats, all_data{j}] = CORDEX_fiveyear_filereader_ehw_r(filename,var_name,soil_mois_day);
    end
    data_chunk = [];
    data_chunk = cat(2,all_data{1:7});
    save_data = data_chunk(:,start_year_gap:(start_year_gap+tot_years),:);
    v.o = save_data;
    savefn = strcat(var_name,'/processed/',var_name,gcm,scen,ens,rcm,int2str(start_year),int2str(end_year),'.mat');
    save(savefn,'v','-v7')
    save('lonlat/nobc_lons','new_lons','-v7')
    save('lonlat/nobc_lats','new_lats','-v7')
end

% this stuff below is to create apparent temperature if desired

%huss_file = strcat('huss/huss',gcm,scen,ens,rcm,int2str(start_year),int2str(end_year),'.mat');
%tas_file = strcat('tas/tas',gcm,scen,ens,rcm,int2str(start_year),int2str(end_year),'.mat');
%ps_file = strcat('sfc',gcm,scen,ens,rcm,int2str(start_year),int2str(end_year),'.mat');

%load(tas_file);
%tas = v.o - 273.15;
%load(huss_file);
%huss = save_data;
%load(ps_file);
%ps = v.o / 100;

%e = (ps.*huss)./(0.622 + 0.378*huss);
%dpt = (log(e/6.112) * 243.5) ./ (17.67 - log(e/6.112));
%appt = (0.0153*(dpt.*dpt)) +(0.994*tas) - 2.653;

%appt_sf = strcat('appt',gcm,scen,ens,rcm,int2str(start_year),int2str(end_year),'.mat');

%clear v
%v.name = var_name
%v.lbound = NaN;
%v.ubound = NaN;
%v.gridded = 0
%v.sLat = 0
%v.sLon = 0
%v.dims = {'nDaysinYear','nYears','nLocations'}
%v.o = appt;

%save(appt_sf,'v');




