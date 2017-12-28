% assign ranking to 0 days beased on local temporal running average (when bound exists)

function [ozb]=bound_ranking(o,oz,lb)
nt=size(o,1);
nmp=size(o,2);
nlocs=size(o,3);

for i=1:nlocs
    if isfinite(lb(i))
        %% linearize o for this loc
        oi=o(:,:,i);
        oil=oi(:);
        ozi=oz(:,:,i);
        ozil=ozi(:);
        oils=smooth(oil,150,'lowess');
        bsx=oils<=lb(i);
        oz0m=mean(ozil(bsx));
        
        
        bx=oil<=lb(i);  %index of 0-elements
        
        [~, oilssx]=sort(oils(bx));
        or=[];
        or(oilssx)=1:length(oilssx);%or is rank of 0s in oil.
        
        ozilbx=sort(ozil(bx)); %transformed values of 0-elements
        
        %ozil(bx)=nan;
        ozil(bx)=ozilbx(or);
        ozil(bsx)=oz0m;
        ozib=reshape(ozil,nt,nmp);       
        oz(:,:,i)=ozib;
    end
end
ozb=oz;

%%
%{
pr=1:5000;
figure(1);clf
subplot(2,1,1);
 plot([oil(pr) oils(pr)]);
 
 subplot(2,1,2);
 plot([ozil(pr)]);

 
 %
 figure(2);clf
 hist(ozil,100)
%}

 
 
 
 