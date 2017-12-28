function [rs,SIG]=MVNgen_iter(r,SIG,o,s,nYears)

nt=size(r,1);
nmp=size(r,2);
nlocs=size(r,3);

if isempty(SIG)  %first iteration
    rp=permute(r,[3 1 2]);
    rp=rp(:,:)';
    SIG=nancov(rp,'pairwise');
else 
    [osp,~,~]=deseason(o);
    [ssp,~,~]=deseason(s);
    o_c=corr(reshape(osp,size(osp,1)*size(osp,2),size(osp,3)),'rows','pairwise');
    s_c=corr(reshape(ssp,size(ssp,1)*size(ssp,2),size(ssp,3)),'rows','pairwise');
    %save('clagarm_o_c','o_c');
    %save('clagarm_s_c','s_c');
    d_c=s_c-o_c;
    SIG=SIG-d_c;
    SIG=nearestSPD(SIG);
end

rs=mvnrnd_eigs(zeros(nYears*nt,nlocs),SIG);
rs=reshape(rs,nt,nYears,nlocs);



