% set all bounded values (when bound exists) to mean

function [ozb]=bound_preserve_mean(o,oz,lb)
nt=size(o,1);
nmp=size(o,2);
nlocs=size(o,3);

for i=1:nlocs
    if isfinite(lb(i))
        %linearize o & oz for this loc
        oi=o(:,:,i);
        oil=oi(:);
        ozi=oz(:,:,i);
        ozil=ozi(:);
        
        %rand permute of bound values
        bx=oil<=lb(i);
        ozilbx=ozil(bx);         
        ozil(bx)=repmat(mean(ozilbx),1,length(ozilbx))+randn(1,length(ozilbx))./100;
        ozib=reshape(ozil,nt,nmp);       
        oz(:,:,i)=ozib;
    end
end
ozb=oz;



