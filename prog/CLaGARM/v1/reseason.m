function [o]=reseason(od,Sm,Sv)

nt=size(od,1);
nmp=size(od,2);
nlocs=size(od,3);

Smr=reshape(Sm,nt,1,nlocs);
Svr=reshape(Sv,nt,1,nlocs);
Smrr=repmat(Smr,[1 nmp 1]);
Svrr=repmat(Svr,[1 nmp 1]);

o=od.*Svrr+Smrr;