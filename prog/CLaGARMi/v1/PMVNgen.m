function rs=PMVNgen(r,nYears,sroot)

nsp=size(r,1);
%nmp=size(r,2);
nlocs=size(r,3);

rp=permute(r,[2 1 3]);
rp=rp(:,:);

SIG=cov(rp);
rs=mvnrnd_eigs_save(zeros(nYears,nlocs*nsp),SIG,[sroot 'cholcov_precalc\']);
rs=reshape(rs,nYears,nsp,nlocs);
rs=permute(rs,[2 1 3]);


