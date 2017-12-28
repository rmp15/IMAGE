%multi location nscore transformation

function [dz,z_dat]=mloc_nscore(d,style)
nt=size(d,1);
nmp=size(d,2);
nlocs=size(d,3);

dl=reshape(d,nt*nmp,nlocs);
z_dat={};
for l=1:nlocs
     dll=dl(:,l);
    if strcmp(style,'linlim')  % use original style for transform data
 [dlz(:,l),z_dat{l}]=NQT_GPt(dll,0.99,0);
    elseif strcmp(style,'GPtails') %use my GPtail method. Must be used in back trans also
        [dlz(:,l),z_dat{l}]=NQT_GPt(dll,0.95,1000);
    end
end
dz=reshape(dlz,nt,nmp,nlocs);

%save('mixed_model_nscore_test_data','d')