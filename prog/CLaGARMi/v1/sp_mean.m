%Calc subperiod mean
function [sp_mean]= sp_mean(d,nsp)
nt=size(d,1);
nlocs=size(d,3);
nmp=size(d,2);
spbs=subPeriodBounds(nt,nsp);
sp_mean=nan(nlocs,nsp,nmp);
for sp=1:nsp
    sp_mean(:,sp,:)=permute(mean(d(spbs(sp,1):spbs(sp,2),:,:),1),[3 1 2]);
end
sp_mean=permute(sp_mean,[2 3 1]);

