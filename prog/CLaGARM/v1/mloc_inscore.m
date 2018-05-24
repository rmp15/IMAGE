%multi location inverse nscore transformation
function s=mloc_inscore(sz,z_dat)

nt=size(sz,1);
nEns=size(sz,2);
nlocs=size(sz,3);

slz=reshape(sz, nt*nEns,nlocs);

parfor l=1:nlocs
    sl(:,l)=iNQT(slz(:,l),z_dat{l});
end
s=reshape(sl,nt,nEns,nlocs);
