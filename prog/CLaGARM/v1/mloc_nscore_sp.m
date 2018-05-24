%multi location nscore transformation
function [dz,o_nscore]=mloc_nscore_sp(d,nsp)

nt=size(d,1);
nmp=size(d,2);
nlocs=size(d,3);

[~,ntsp,~,spr]=subPeriodBounds(nt,nsp);
o_nscore={};
dz=[];
for sp=1:nsp
    
    dsp=d(spr{sp},:,:);
    dl=reshape(dsp,ntsp(sp)*nmp,nlocs);

    for l=1:nlocs
        dll=dl(:,l);
        %dll(isnan(dll)) = [];
        [dlz(:,l),o_nscore{l,sp}]=NQT_GPt(dll,0.99,0);
    end
    dz=[dz;reshape(dlz,ntsp(sp),nmp,nlocs)];
    dlz=[];
end

