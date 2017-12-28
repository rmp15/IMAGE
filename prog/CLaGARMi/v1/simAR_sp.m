function s=simAR_sp(c,p,r)

nt=size(r,1);
nYears=size(r,2);
nlocs=size(r,3);

nsp=size(c,1);

r=permute(r,[3,2,1]);  %make nlocs first dim for simpler formulae
c=permute(c,[3 2 1]);
p=permute(p,[3 2 1]);
s=nan(nlocs,nYears,nt);

[spbd,ntsp,spi]=subPeriodBounds(nt,nsp);

for y=1:nYears
    for t=1:nt
        sp=spi(t);
        
        if t==1 && y==1
            %% first day of first year init.
            s(:,y,t) = c(:,y,sp)+r(:,y,t);
        elseif t==1 && y>1
            %% new year
            s(:,y,t) = c(:,y,sp)+p(:,y,sp).*s(:,y-1,nt) + r(:,y,t);
        elseif t>1
            %% just an ordinary day...
            s(:,y,t) = c(:,y,sp)+p(:,y,sp).*s(:,y,t-1) + r(:,y,t);
        end
%        [ms,mx]=max(abs(s(:,y,t)));
%         if ms>5;
%             disp(['p=' num2str(p(mx,y,sp))]);
%             disp(['c=' num2str(c(mx,y,sp))]);
%             
%             figure(1);clf
%             plot(squeeze(s(mx,y,:)));hold on
%             plot(squeeze(r(mx,y,:)));
%             disp('divergence?')
%         end
    end
end

s=permute(s,[3 2 1]); %return s in canonical form: [nt,nmp,nlocs]
        
            