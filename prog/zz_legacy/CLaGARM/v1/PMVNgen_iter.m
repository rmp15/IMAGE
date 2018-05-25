function [rs,SIG]=PMVNgen_iter(r,SIG,o,s,nYears)
save('PMVNgen_SIG_in.mat','SIG');
nsp=size(r,1);
nmp=size(r,2);
nlocs=size(r,3);
if isempty(SIG) %first iter
rp=permute(r,[2 1 3]);
rp=rp(:,:);
SIG=nancov(rp);
else
    ospm=sp_mean(o(:,:,:),nsp);
    sspm=sp_mean(s(:,:,:),nsp);
    
    op=permute(ospm,[2 1 3]);
    op=op(:,:);
    sp=permute(sspm,[2 1 3]);
    sp=sp(:,:);
    o_c=corr(op,'rows','pairwise');
    s_c=corr(sp);
    d_c=s_c-o_c;
    nsigmu=size(d_c,1);    
    SIG(1:nsigmu,1:nsigmu)=SIG(1:nsigmu,1:nsigmu)-2*d_c(1:nsigmu,1:nsigmu);
    SIG=nearestSPD(SIG);  
       
end

rs=mvnrnd(zeros(nYears,nlocs*nsp),SIG); %out of mem

rs=reshape(rs,nYears,nsp,nlocs);
rs=permute(rs,[2 1 3]);

% %%where do the mus go in reshaped matrix
% mu=ones(10,20,30);
% p=zeros(10,20,30);
% mup=cat(3,mu,p);
% mupp=permute(mup,[2 1 3]);
% mupp=mupp(:,:);
% %seems like they all end up at the start...good.


