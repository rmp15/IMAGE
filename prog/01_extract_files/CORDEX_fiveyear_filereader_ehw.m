function [europe_heatwave_lons, europe_heatwave_lats, concatted_vari]=CORDEX_fiveyear_filereader_ehw(filename,var_name,soil_mois_day)

eurhw_y = [35.17 38.00 36.60 34.32 41.10 47.16 71.58 71.44 59.33 52.45 35.05]
eurhw_x = [-5.56 8.47 13.79 27.08 30.40 39.23 33.65 8.85 -7.41 -15.91 -12.95]


landmask = []


model_lons = ncread(filename,'lon');
model_lats = ncread(filename,'lat');

model_pr = ncread(filename,var_name);



var_size = size(model_pr);

mpr_dim1 = var_size(1);
mpr_dim2 = var_size(2);
mpr_dim3 = var_size(3);

for i = 1:mpr_dim1
    for j = 1:mpr_dim2
        if soil_mois_day(i,j) == 0
            model_pr(i,j,:) = nan(mpr_dim3,1);
        end
    end
end

new_lons = zeros(53,51);
new_lats = zeros(53,51);
new_var = zeros(53,51,var_size(3));



for i = 1:53
    for j = 1:51
        old_i_coord = (i*2)-1
        old_j_coord = (j*2)-1
        
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
        new_var4s(1,:) = model_pr(old_i_coord,old_j_coord,1:var_size(3));
        new_var4s(2,:) = model_pr(old_i_coord+1,old_j_coord,1:var_size(3));
        new_var4s(3,:) = model_pr(old_i_coord,old_j_coord+1,1:var_size(3));
        new_var4s(4,:) = model_pr(old_i_coord+1,old_j_coord+1,1:var_size(3));
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
        new_var_data = nan(no_non_nan,var_size(3));
        gc_count = 1;
        for gc = 1:4
           if(isequal(sum(isnan(new_var4s(gc,:))),0))
               new_var_data(gc_count,:) = new_var4s(gc,:);
               gc_count = gc_count + 1;
           end
        end
        if size_nan_gcs(2) >= 3
            new_var(i,j,:) = nan(1,1,var_size(3));
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
no_of_years = 5

concatted_vari = zeros(no_of_days_in_year,no_of_years,no_of_gcs);

for year_index = 1:no_of_years
for indx = 1:no_of_gcs
    concatted_vari(:,year_index,indx) = new_var(xlist(indx),ylist(indx),(365*(year_index-1))+1:(365*(year_index-1))+365);
end
end