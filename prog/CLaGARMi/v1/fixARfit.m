function [cfix,pfix]=fixARfit(c,p,o,nsp)

data_mu=sp_mean(o,nsp);
ar_mu=c./(1-p);
dmu=ar_mu-data_mu;

t=1; %error threshold

%where error exceeds thresh, replace p with clim mean, ar_mu with data_mu
x=abs(dmu)>t; %error index
%sum(x(:))
pfix=p;
pfix(x)=nan;
pmean=repmat(nanmean(pfix,2),1,size(p,2),1);
pfix(x)=pmean(x);

ar_mu(x)=data_mu(x);

%calc new c
cfix=ar_mu.*(1-pfix);

%ar_mu_fix=cfix./(1-pfix);
%dmu_f=ar_mu_fix-data_mu;





% %%
% [x1,x2,x3]=ind2sub(size(dmu),find(abs(dmu)>1));
% x=[x1 x2 x3];
% figure(1);clf
% hist(x1);
