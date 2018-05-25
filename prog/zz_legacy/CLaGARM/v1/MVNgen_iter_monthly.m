function [rs,SIG]=MVNgen_iter(r,SIG,o,s,nYears)
save('MVNgen_SIG_in.mat','SIG');
nt=size(r,1);
nmp=size(r,2);
nlocs=size(r,3);


nsp=12;
[spbs,ntsp,spi]=subPeriodBounds(nt,nsp);

o_ds = deseason(o);
s_ds = deseason(s);



if isempty(SIG)  %first iteration
    SIG = zeros(nsp,nlocs,nlocs);
    rs = zeros(nt,nYears,nlocs);
    
%     rp=permute(r,[3 1 2]);
%     rp=rp(:,:)';
%     SIG=cov(rp);
    for sp=1:nsp
        r_sp = r(spbs(sp,1):spbs(sp,2),:,:);
        nt_sp = size(r_sp,1);
        rp=permute(r_sp,[3 1 2]);
        rp=rp(:,:)';
        trfn = strcat('rsp_in',int2str(sp),'.mat');
        
        [rz,rz_dat]=mloc_nscore(rp,'linlim');
        save(trfn,'rp');
        SIG_sp = cov(rz);
        SIG(sp,:,:) = SIG_sp;
        r_sp=mloc_inscore(rz,rz_dat);
        
        r_sp=mvnrnd(zeros(nYears*nt_sp,nlocs),SIG_sp);
        r_sp=reshape(r_sp,nt_sp,nYears,nlocs);
        
        rs(spbs(sp,1):spbs(sp,2),1:nYears,:) = r_sp;
    end
else
    rs = zeros(nt,nYears,nlocs);
    for sp=1:nsp
        size_rs = size(r);
        SIG_sp = squeeze(SIG(sp,:,:));
        osp_ds = o_ds(spbs(sp,1):spbs(sp,2),:,:);
        ssp_ds = s_ds(spbs(sp,1):spbs(sp,2),:,:);
        rsp = r(spbs(sp,1):spbs(sp,2),:,:);
        [rz,rz_dat]=mloc_nscore(rsp,'linlim');
        o_c=corr(reshape(osp_ds,size(osp_ds,1)*size(osp_ds,2),size(osp_ds,3)));
        s_c=corr(reshape(ssp_ds,size(ssp_ds,1)*size(ssp_ds,2),size(ssp_ds,3)));
        tofn = strcat('o_c',int2str(sp),'.mat');
        tsfn = strcat('s_c',int2str(sp),'.mat');
        
        tr2fn = strcat('rsp_out',int2str(sp),'.mat');
        save(tofn,'o_c');
        save(tsfn,'s_c');
        
        d_c=s_c-o_c;
        
        SIG_sp=SIG_sp-d_c;
        %save('MVNgen_d_c.mat','d_c');
        SIG_sp=nearestSPD(SIG_sp);
        SIG(sp,:,:) = SIG_sp;
        nt_sp = size(osp_ds,1);
        r_sp=mvnrnd(zeros(nYears*nt_sp,nlocs),SIG_sp);
        r_sp=reshape(r_sp,nt_sp,nYears,nlocs);
        r_sp=mloc_inscore(r_sp,rz_dat);
        save(tr2fn,'r_sp');
        rs(spbs(sp,1):spbs(sp,2),1:nYears,:) = r_sp;
    end
end

%save('MVNgen_SIG_i.mat','SIG');


rs=reshape(rs,nt,nYears,nlocs);



