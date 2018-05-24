function output=CORDEX_input_file_creator_europe_heatwave2(variable_name,lbound,ubound,file_prefix,start_year,end_year,save_file_suffix)

%load('Danube_coords.mat')

clear v

%file_prefix = 'rsds_EUR-11-bc_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-wfdei_day_';
file_ext = '.nc';

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

eurhw_y = [35.17 38.00 36.60 34.32 41.10 47.16 71.58 71.44 59.33 52.45 35.05]
eurhw_x = [-5.56 8.47 13.79 27.08 30.40 39.23 33.65 8.85 -7.41 -15.91 -12.95]

start_year_str = int2str(start_year);

example_file = strcat(variable_name,'_',file_prefix,start_year_str,file_ext);

if strcmp(variable_name,'rh')
    example_file = strcat('tas','_',file_prefix,start_year_str,file_ext);
end


model_lons = ncread(example_file,'lon');
model_lats = ncread(example_file,'lat');
model_pr = ncread(example_file,variable_name);

new_lons = zeros(65,39);
new_lats = zeros(65,39);
new_var = zeros(65,39,365);


for i = 1:65
    for j = 1:39
        old_i_coord = (i*4)-2;
        old_j_coord = (j*4)-2;
        lat4s(1) = model_lats(old_i_coord,old_j_coord);
        lat4s(2) = model_lats(old_i_coord+1,old_j_coord);
        lat4s(3) = model_lats(old_i_coord,old_j_coord+1);
        lat4s(4) = model_lats(old_i_coord+1,old_j_coord+1);
        lon4s(1) = model_lons(old_i_coord,old_j_coord);
        lon4s(2) = model_lons(old_i_coord+1,old_j_coord);
        lon4s(3) = model_lons(old_i_coord,old_j_coord+1);
        lon4s(4) = model_lons(old_i_coord+1,old_j_coord+1);
        new_lats(i,j) = mean(lat4s);
        new_lons(i,j) = mean(lon4s);
        new_var4s = [];
        new_var4s(1,:) = model_pr(old_i_coord,old_j_coord,1:365);
        new_var4s(2,:) = model_pr(old_i_coord+1,old_j_coord,1:365);
        new_var4s(3,:) = model_pr(old_i_coord,old_j_coord+1,1:365);
        new_var4s(4,:) = model_pr(old_i_coord+1,old_j_coord+1,1:365);
        nan_gcs = [];
        new_var_data = [];
        for gc = 1:4
            if(isequal(sum(isnan(new_var4s(gc,:))),0))
            else
                nan_gcs = [nan_gcs gc];

            end
        end
        size_nan_gcs = size(nan_gcs);
        no_non_nan = 4 - size_nan_gcs(2);
        new_var_data = nan(no_non_nan,365);
        gc_count = 1;
        for gc = 1:4
           if(isequal(sum(isnan(new_var4s(gc,:))),0))
               new_var_data(gc_count,:) = new_var4s(gc,:);
               gc_count = gc_count + 1;
           end
        end
        if size_nan_gcs(2) >= 3
            new_var(i,j,:) = nan(1,1,365);
        else
            snvd = size(new_var_data);
            new_var(i,j,:) = mean(new_var_data);
        end
        
        %new_var(i,j,:) = model_pr(old_i_coord,old_j_coord,1:365);
    end
end

no_lons = size(new_lons,1);
no_lats = size(new_lons,2);
days_in_file = size(model_pr,3);

if days_in_file > 365
    no_of_days_in_year = 365
else
    no_of_days_in_year = days_in_file
end

num = 0;
xlist = [];
ylist = [];
europe_heatwave_lats = [];
europe_heatwave_lons = [];
nannum = 0;
for x = 1:no_lons
    for y = 1:no_lats
        

            if(isequal(sum(isnan(new_var(x,y,:))),0))
                if(inpolygon(new_lons(x,y),new_lats(x,y),eurhw_x,eurhw_y)==1)
                    %disp(new_var(x,y,1))
                    num = num+1;

                    xlist = [xlist;x];
                    ylist = [ylist;y];
                    europe_heatwave_lats = [europe_heatwave_lats;new_lats(x,y)];
                    europe_heatwave_lons = [europe_heatwave_lons;new_lons(x,y)];
            
                end
            end
        
    end
end
nannum
no_of_gcs = size(xlist,1);
no_of_years = end_year - start_year + 1

concatted_vari = zeros(no_of_days_in_year,no_of_years,no_of_gcs);

for year = start_year:end_year
    
    year_str = num2str(year);
    target_file = strcat(variable_name,'_',file_prefix,year_str,file_ext);
    year_index = year - start_year + 1

    model_pr = ncread(target_file,variable_name);
    


    
    days_in_file = size(model_pr,3);
    if days_in_file > 365
        model_pr = model_pr(:,:,1:365);
    end
        
    new_var = zeros(65,39,365);


    for i = 1:65
        for j = 1:39
            old_i_coord = (i*4)-2;
            old_j_coord = (j*4)-2;
            new_var4s(1,:) = model_pr(old_i_coord,old_j_coord,1:365);
            new_var4s(2,:) = model_pr(old_i_coord+1,old_j_coord,1:365);
            new_var4s(3,:) = model_pr(old_i_coord,old_j_coord+1,1:365);
            new_var4s(4,:) = model_pr(old_i_coord+1,old_j_coord+1,1:365);
            nan_gcs = [];
        new_var_data = [];
        for gc = 1:4
            if(isequal(sum(isnan(new_var4s(gc,:))),0))
            else
                nan_gcs = [nan_gcs gc];

            end
        end
        size_nan_gcs = size(nan_gcs);
        no_non_nan = 4 - size_nan_gcs(2);
        new_var_data = nan(no_non_nan,365);
        gc_count = 1;
        for gc = 1:4
           if(isequal(sum(isnan(new_var4s(gc,:))),0))
               new_var_data(gc_count,:) = new_var4s(gc,:);
               gc_count = gc_count + 1;
           end
        end
        if size_nan_gcs(2) >= 3
            new_var(i,j,:) = nan(1,1,365);
        else
            snvd = size(new_var_data);
            new_var(i,j,:) = mean(new_var_data);
       
        end
        end
    end
    

    
    cordex_danube_pr = zeros(num,days_in_file);

    for indx = 1:no_of_gcs
        concatted_vari(:,year_index,indx) = new_var(xlist(indx),ylist(indx),:);
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

if strcmp(variable_name,'rsds')
    [concatted_vari, rsds_ulim] = rsds_prescale(concatted_vari);
    rsds_ulim_name = 'rsds_ulim';
    rsds_ulim_save_file = strcat(rsds_ulim_name,save_file_suffix);
    save(rsds_ulim_save_file,'rsds_ulim','-v7.3');
end

v.o = concatted_vari;

eh_lats = zeros(num,1);
eh_lons = zeros(num,1);

for i = 1:num
    eh_lats(i,1) = new_lats(xlist(i),ylist(i));
    eh_lons(i,1) = new_lons(xlist(i),ylist(i));
end


save_file = strcat(variable_name,save_file_suffix)
save(save_file,'v','-v7.3')

lat_save_file = strcat('lat',save_file_suffix)
lon_save_file = strcat('lon',save_file_suffix)

save(lat_save_file,'eh_lats','-v7.3')
save(lon_save_file,'eh_lons','-v7.3')
output = 1
