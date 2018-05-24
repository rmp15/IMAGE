function rs=MVNgen(r,nYears)

nsp=size(r,1);
nmp=size(r,2);
nlocs=size(r,3);

rp=permute(r,[2 1 3]);
rp=rp(:,:);

SIG=cov(rp);
rs=mvnrnd(zeros(nYears,nlocs*nsp),SIG);
rs=reshape(rs,nYears,nsp,nlocs);
rs=permute(rs,[2 1 3]);


