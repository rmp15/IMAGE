model_scenario = 'MPI_hist'


start_year = 1970
end_year = 1999
sy_str = int2str(start_year)
ey_str = int2str(end_year)
save_file_suffix = strcat(model_scenario,sy_str,ey_str)



if strcmp(model_scenario,'MPI_REMO_85')
    variable_names = {'rsds','tasmax','tasmin','pr'}
    file_prefixs = {'EUR-11-bc_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-wfdei_day_','EUR-11-bc_MPI-M-ESM-LR_rcp85_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-eobs9_day_','EUR-11-bc_MPI-M-ESM-LR_rcp85_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-eobs9_day_','EUR-11-bc_MPI-M-ESM-LR_rcp85_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-eobs9_day_'}
    lbounds = {0,NaN,NaN,0}
    ubounds = {NaN,NaN,NaN,NaN}
end

if strcmp(model_scenario,'ICHEC_KNMI_85')
    variable_names = {'rsds','tasmax','tasmin','pr'}
    file_prefixs = {'EUR-11-bc_ICHEC-EC-EARTH_rcp85_r1i1p1_KNMI-RACMO22E_v1-bc-qm-wfdei_day_','EUR-11-bc_ICHEC-EC-EARTH_rcp85_r1i1p1_KNMI-RACMO22E_v1-bc-qm-eobs9_day_','EUR-11-bc_ICHEC-EC-EARTH_rcp85_r1i1p1_KNMI-RACMO22E_v1-bc-qm-eobs9_day_','EUR-11-bc_ICHEC-EC-EARTH_rcp85_r1i1p1_KNMI-RACMO22E_v1-bc-qm-eobs9_day_'}
    lbounds = {0,NaN,NaN,0}
    ubounds = {NaN,NaN,NaN,NaN}
end

if strcmp(model_scenario,'ICHEC_KNMI_45')
    variable_names = {'rsds','tasmax','tasmin','pr'}
    file_prefixs = {'EUR-11-bc_ICHEC-EC-EARTH_rcp45_r1i1p1_KNMI-RACMO22E_v1-bc-qm-wfdei_day_','EUR-11-bc_ICHEC-EC-EARTH_rcp45_r1i1p1_KNMI-RACMO22E_v1-bc-qm-eobs9_day_','EUR-11-bc_ICHEC-EC-EARTH_rcp45_r1i1p1_KNMI-RACMO22E_v1-bc-qm-eobs9_day_','EUR-11-bc_ICHEC-EC-EARTH_rcp45_r1i1p1_KNMI-RACMO22E_v1-bc-qm-eobs9_day_'}
    lbounds = {0,NaN,NaN,0}
    ubounds = {NaN,NaN,NaN,NaN}
end

if strcmp(model_scenario,'ICHEC_KNMI_hist')
    variable_names = {'rsds','tasmax','tasmin','pr'}
    file_prefixs = {'EUR-11-bc_ICHEC-EC-EARTH_historical_r1i1p1_KNMI-RACMO22E_v1-bc-qm-wfdei_day_','EUR-11-bc_ICHEC-EC-EARTH_historical_r1i1p1_KNMI-RACMO22E_v1-bc-qm-eobs9_day_','EUR-11-bc_ICHEC-EC-EARTH_historical_r1i1p1_KNMI-RACMO22E_v1-bc-qm-eobs9_day_','EUR-11-bc_ICHEC-EC-EARTH_historical_r1i1p1_KNMI-RACMO22E_v1-bc-qm-eobs9_day_'}
    lbounds = {0,NaN,NaN,0}
    ubounds = {NaN,NaN,NaN,NaN}
end

if strcmp(model_scenario,'ICHEC_SMHI_85')
    variable_names = {'rsds','tasmax','tasmin','pr'}
    file_prefixs = {'EUR-11-bc_ICHEC-EC-EARTH_rcp85_r12i1p1_SMHI-RCA4_v1-bc-qm-wfdei_day_','EUR-11-bc_ICHEC-EC-EARTH_rcp85_r12i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_','EUR-11-bc_ICHEC-EC-EARTH_rcp85_r12i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_','EUR-11-bc_ICHEC-EC-EARTH_rcp85_r12i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_'}
    lbounds = {0,NaN,NaN,0}
    ubounds = {NaN,NaN,NaN,NaN}
end

if strcmp(model_scenario,'ICHEC_SMHI_45')
    variable_names = {'rsds','tasmax','tasmin','pr'}
    file_prefixs = {'EUR-11-bc_ICHEC-EC-EARTH_rcp45_r12i1p1_SMHI-RCA4_v1-bc-qm-wfdei_day_','EUR-11-bc_ICHEC-EC-EARTH_rcp45_r12i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_','EUR-11-bc_ICHEC-EC-EARTH_rcp45_r12i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_','EUR-11-bc_ICHEC-EC-EARTH_rcp45_r12i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_'}
    lbounds = {0,NaN,NaN,0}
    ubounds = {NaN,NaN,NaN,NaN}
end

if strcmp(model_scenario,'ICHEC_SMHI_hist')
    variable_names = {'rsds','tasmax','tasmin','pr'}
    file_prefixs = {'EUR-11-bc_ICHEC-EC-EARTH_historical_r12i1p1_SMHI-RCA4_v1-bc-qm-wfdei_day_','EUR-11-bc_ICHEC-EC-EARTH_historical_r12i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_','EUR-11-bc_ICHEC-EC-EARTH_historical_r12i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_','EUR-11-bc_ICHEC-EC-EARTH_historical_r12i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_'}
    lbounds = {0,NaN,NaN,0}
    ubounds = {NaN,NaN,NaN,NaN}
end

if strcmp(model_scenario,'MOHC_SMHI_85')
    variable_names = {'rsds','tasmax','tasmin','pr'}
    file_prefixs = {'EUR-11-bc_MOHC-HadGEM2-ES_rcp85_r1i1p1_SMHI-RCA4_v1-bc-qm-wfdei_day_','EUR-11-bc_MOHC-HadGEM2-ES_rcp85_r1i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_','EUR-11-bc_MOHC-HadGEM2-ES_rcp85_r1i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_','EUR-11-bc_MOHC-HadGEM2-ES_rcp85_r1i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_'}
    lbounds = {0,NaN,NaN,0}
    ubounds = {NaN,NaN,NaN,NaN}
end

if strcmp(model_scenario,'MOHC_SMHI_45')
    variable_names = {'rsds','tasmax','tasmin','pr'}
    file_prefixs = {'EUR-11-bc_MOHC-HadGEM2-ES_rcp45_r1i1p1_SMHI-RCA4_v1-bc-qm-wfdei_day_','EUR-11-bc_MOHC-HadGEM2-ES_rcp45_r1i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_','EUR-11-bc_MOHC-HadGEM2-ES_rcp45_r1i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_','EUR-11-bc_MOHC-HadGEM2-ES_rcp45_r1i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_'}
    lbounds = {0,NaN,NaN,0}
    ubounds = {NaN,NaN,NaN,NaN}
end

if strcmp(model_scenario,'MOHC_SMHI_hist')
    variable_names = {'rsds','tasmax','tasmin','pr'}
    file_prefixs = {'EUR-11-bc_MOHC-HadGEM2-ES_historical_r1i1p1_SMHI-RCA4_v1-bc-qm-wfdei_day_','EUR-11-bc_MOHC-HadGEM2-ES_historical_r1i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_','EUR-11-bc_MOHC-HadGEM2-ES_historical_r1i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_','EUR-11-bc_MOHC-HadGEM2-ES_historical_r1i1p1_SMHI-RCA4_v1-bc-qm-eobs9_day_'}
    lbounds = {0,NaN,NaN,0}
    ubounds = {NaN,NaN,NaN,NaN}
end

if strcmp(model_scenario,'MPI_hist')
    variable_names = {'rsds','tasmax','tasmin','pr'}
    file_prefixs = {'EUR-11-bc_MPI-M-MPI-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-wfdei_day_','EUR-11-bc_MPI-M-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-eobs9_day_','EUR-11-bc_MPI-M-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-eobs9_day_','EUR-11-bc_MPI-M-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-eobs9_day_'}
    lbounds = {0,NaN,NaN,0}
    ubounds = {NaN,NaN,NaN,NaN}
end

if strcmp(model_scenario,'MPI_45')
    variable_names = {'rsds','tasmax','tasmin','pr'}
    file_prefixs = {'EUR-11-bc_MPI-M-MPI-ESM-LR_rcp45_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-wfdei_day_','EUR-11-bc_MPI-M-ESM-LR_rcp45_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-eobs9_day_','EUR-11-bc_MPI-M-ESM-LR_rcp45_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-eobs9_day_','EUR-11-bc_MPI-M-ESM-LR_rcp45_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-eobs9_day_'}
    lbounds = {0,NaN,NaN,0}
    ubounds = {NaN,NaN,NaN,NaN}
end

if strcmp(model_scenario,'MPI_85')
    variable_names = {'rsds','tasmax','tasmin','pr'}
    file_prefixs = {'EUR-11-bc_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-wfdei_day_','EUR-11-bc_MPI-M-ESM-LR_rcp85_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-eobs9_day_','EUR-11-bc_MPI-M-ESM-LR_rcp85_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-eobs9_day_','EUR-11-bc_MPI-M-ESM-LR_rcp85_r1i1p1_MPI-CSC-REMO2009_v1-bc-qm-eobs9_day_'}
    lbounds = {0,NaN,NaN,0}
    ubounds = {NaN,NaN,NaN,NaN}
end

for i =2:2

    variable_name = variable_names{1,i}
    lbound = lbounds{1,i}
    ubound = ubounds{1,i}
    file_prefix = file_prefixs{1,i}


    output=CORDEX_input_file_creator_europe_heatwave(variable_name,lbound,ubound,file_prefix,start_year,end_year,save_file_suffix)
    
end