function [od,Sm,Sv]=deseason(o)

nt=size(o,1);
nmp=size(o,2);
nlocs=size(o,3);

m=squeeze(nanmean(o,2));
v=squeeze(nanstd(o,0,2));

m3=cat(1, m,m,m);
v3=cat(1, v,v,v);

clear Sm Sv

for i=1:nlocs
    Sm(:,i)=smooth(m3(:,i),0.1,'loess');  %loess span value picked by eye...
    Sv(:,i)=smooth(v3(:,i),0.1,'loess');
end
Sm=Sm(nt+1:2*nt,:,:);
Sv=Sv(nt+1:2*nt,:,:);

Smr=reshape(Sm,nt,1,nlocs);
Svr=reshape(Sv,nt,1,nlocs);
Smrr=repmat(Smr,[1 nmp 1]);
Svrr=repmat(Svr,[1 nmp 1]);

od=(o-Smrr)./Svrr;



%{
figure(1);clf
plot(squeeze(m));hold on
plot(Sm);


figure(2);clf
plot(squeeze(v));hold on
plot(Sv);
%}


