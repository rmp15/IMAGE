function output=CORDEX_input_file_creator_Eobs(variable_name,lbound,ubound,file_prefix,start_year,end_year,save_file_suffix)

load('Danube_coords.mat')

clear v

%file_prefix = 'rsds_EUR-11-bc_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-wfdei_day_';
file_ext = '.nc4';

%variable_name = 'rsds';
v.name = variable_name
v.lbound = lbound
v.ubound = ubound
v.gridded = 0
v.sLat = 0
v.sLon = 0
v.dims = {'nDaysinYear','nYears','nLocations'}
%start_year = 2051;
%end_year = 2100;

start_year_str = int2str(start_year);

example_file = strcat(file_prefix,file_ext);

model_lons = ncread(example_file,'longitude');
model_lats = ncread(example_file,'latitude');
model_pr = ncread(example_file,variable_name);

time_units = ncreadatt(example_file,'time','units')


t1 = datetime(1978,12,31)
t2 = datetime(start_year,01,01)
day_gap = between(t1,t2,'days')
start_day = caldays(day_gap)

no_lons = size(model_lons,1);
no_lats = size(model_lats,1);
days_in_file = size(model_pr,3);

if days_in_file > 365
    no_of_days_in_year = 365
else
    no_of_days_in_year = days_in_file
end

num = 0;
xlist = [];
ylist = [];
cordex_danube_lats = [];
cordex_danube_lons = [];

for x = 1:no_lons
    for y = 1:no_lats

        if(inpolygon(model_lons(x,1),model_lats(y,1),Danube_x,Danube_y) == 1)

            num = num+1;
            xlist = [xlist;x];
            ylist = [ylist;y];
            cordex_danube_lats = [cordex_danube_lats;model_lats(y,1)];
            cordex_danube_lons = [cordex_danube_lons;model_lons(x,1)];

        end
    end
end

no_of_gcs = size(xlist,1);
no_of_years = end_year - start_year + 1

concatted_vari = zeros(no_of_days_in_year,no_of_years,no_of_gcs);

for year = start_year:end_year
    
    year_str = num2str(year);
    %target_file = strcat(variable_name,'_',file_prefix,year_str,file_ext);
    year_index = year - start_year + 1

    model_pr = ncread(example_file,variable_name);
    

    t1 = datetime(year-1,01,01);
    t2 = datetime(year,01,01);
    days_in_year = between(t1,t2,'days');
    days_in_year = caldays(days_in_year);
    days_in_file = size(model_pr,3);
    if days_in_file > 365
        year_var = model_pr(:,:,start_day:start_day+364);
    end
        
    start_day = start_day + days_in_year
    

    
    cordex_danube_pr = zeros(num,days_in_file);

    for indx = 1:no_of_gcs
        concatted_vari(:,year_index,indx) = year_var(xlist(indx),ylist(indx),:);
    end
    
%     indx = 1;
%     for x = 1:no_lons
%         for y = 1:no_lats
% 
%             if(inpolygon(model_lons(x,y),model_lats(x,y),Danube_x,Danube_y) == 1)
%                 cordex_danube_lats(indx,1) = model_lats(x,y);
%                 cordex_danube_lons(indx,1) = model_lons(x,y);
%                 cordex_danube_pr(indx,:) = model_pr(x,y,:);
% 
%                 indx = indx+1;
%             end
%         end
%     end
    
      
end

%save_file_suffix = 'MPI_REMO2009'

if strcmp(variable_name,'var2')
    concatted_vari = concatted_vari ./ 8.64;
    [concatted_vari, rsds_ulim] = rsds_prescale(concatted_vari);
    rsds_ulim_name = 'rsds_ulim';
    rsds_ulim_save_file = strcat(rsds_ulim_name,save_file_suffix);
    save(rsds_ulim_save_file,'rsds_ulim','-v7.3');
end

v.o = concatted_vari;



save_file = strcat(variable_name,save_file_suffix)
save(save_file,'v','-v7.3')

lat_save_file = strcat('lat',save_file_suffix)
lon_save_file = strcat('lon',save_file_suffix)

save(lat_save_file,'cordex_danube_lats','-v7.3')
save(lon_save_file,'cordex_danube_lons','-v7.3')
output = 1
