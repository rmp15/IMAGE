% assign ranking to 0 days beased on local temporal running average (when bound exists)

function [ozb]=bound_shuffle(o,oz,lb)
nt=size(o,1);
nmp=size(o,2);
nlocs=size(o,3);

for i=1:nlocs
    if isfinite(lb(i))
        %linearize o for this loc
        oi=o(:,:,i);
        oil=oi(:);
        ozi=oz(:,:,i);
        ozil=ozi(:);
        
        %rand permute of bound values
        bx=oil<=lb(i);
        ozilbx=ozil(bx);
        ozil(bx)=ozilbx(randperm(length(ozilbx)));
        ozib=reshape(ozil,nt,nmp);       
        oz(:,:,i)=ozib;
    end
end
ozb=oz;



