% inverse Normal Quantile Transform
% sz is Normal score data, iNQTdat is generated sduring the forward transform in NQT_GPt 

function [s]=iNQT(sz,iNQTdat)

oq=iNQTdat.q;
o=iNQTdat.o;

oz=norminv(oq,0,1);
 s=interp1(oz,o,sz);
 s(sz>max(oz))=max(o);
 s(sz<min(oz))=min(o);
 