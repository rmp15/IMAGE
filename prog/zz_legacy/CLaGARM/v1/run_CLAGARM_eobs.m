for scen = 1:1
    model_name = 'Eobs'
    scen_name = {'','_4520202049','_8520202049','_4520702099','_8520702099'}
    scenario_years = strcat(model_name,scen_name{1,scen})

for split = 1:1
    
    clearvars -except split scenario_years scen

    
    variable_names = {'rr','var2','tx','tn'}
    %hashfilename = strcat(scenario_years,'_tiny');
    hashfilename = scenario_years
    savefilename = strcat('out_',scenario_years,'clagarm');

    for i = 1:4

        file_name = strcat(variable_names{1,i},scenario_years,'.mat')
        load(file_name)
        mv(i)=v;
        %mv(i).o = mv(i).o(:,1:20,650:680);

    end

    mv = mv(1);


    clear v
    %validateInputData(mv);
    tic


    %savefilename = strcat(savefilename,int2str(split))
    %hashfilename = strcat(hashfilename,int2str(split))
    rng default
    [mv]=CLaGARM_nohash(1000,12,mv,hashfilename);
    disp('Saving...');
    %save(['out_eobs_SE_tntxrr_shuf_ll_XPX'],'mv','-v7.3');
    save(savefilename,'mv','-v7.3');
    toc

end
end