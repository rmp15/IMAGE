%multi location inverse nscore transformation
function s=mloc_inscore_sp(sz,o_nscore,nsp)

nt=size(sz,1);
nEns=size(sz,2);
nlocs=size(sz,3);
[~,ntsp,~,spr]=subPeriodBounds(nt,nsp);

s=[];
for sp=1:nsp
    szsp=sz(spr{sp},:,:);
    slz=reshape(szsp, ntsp(sp)*nEns,nlocs);   
    for l=1:nlocs
        sl(:,l)=iNQT(slz(:,l),o_nscore{l,sp});
    end
    ssp=reshape(sl,ntsp(sp),nEns,nlocs);
    s=[s;ssp];
    sl=[];
end
    