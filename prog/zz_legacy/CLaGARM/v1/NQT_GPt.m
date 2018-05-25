% Normal Quantile Transform with Gen Pareto tails
% o is data to be transforms, th is tail threshold quantile, dmult is tail
% data density multiplier. Set to 0 for no tails.

function [oz,iNQTdat]=NQT_GPt(o,th,dmult)

n_orig = length(o);
nan_inds = find(isnan(o));
[o,osx]=sort(o);
no_nans = length(nan_inds);
o(isnan(o)) = [];
n=length(o);
[o,osx_no_nans]=sort(o);

%q=1/(n+1):1/(n+1):1-1/(n+1);
oq=1/(2*n):1/n:1-1/(2*n);
oz(osx(1:n))=norminv(oq,0,1);
oz(nan_inds) = NaN;

if dmult>1
    %create synthetic GP tails with quantiles
    uthq=th;
    lthq=1-th;
    %dmult=100; % tail density multiplier
    uth=prctile(o,100*uthq);
    lth=prctile(o,100*lthq);
    
    lbound=0;
    if lth==0; lbound=1; end
    
    oq=1/(2*n):1/n:1-1/(2*n);
    ou=o(o>uth)-uth;
    ol=-(o(o<lth)-lth);
    
    %fit gp to tails
    oc=o(o<=uth & o>=lth);
    oqc=oq(o<=uth & o>=lth);
    
    fu=gpfit(ou);
    if ~lbound;
        fl=gpfit(ol);
    end
    nu=length(ou);
    nl=length(ol);
    
    %resample tails
    dq=1/(nu*dmult);
    xu=dq/2:dq:1-dq/2;
    qu=xu*(1-uthq)+uthq;
    ousyn=gpinv(xu,fu(1),fu(2))+uth;
    
    if ~lbound
        dq=1/(nl*dmult);
        xl=dq/2:dq:1-dq/2;
        ql=(1-xl)*lthq;
        olsyn=-(gpinv(xl,fl(1),fl(2)))+lth;
    else
        ql=[];
        olsyn=[];
    end
    
    %build values and quantiles for inverse transform
    osyn=[oc;olsyn';ousyn'];
    qsyn=[oqc';ql';qu'];
    
    iNQTdat.o=osyn;
    iNQTdat.q=qsyn;
else
    iNQTdat.o=o;
    iNQTdat.q=oq';
end