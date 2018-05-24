function [c,p,r]=calc_AR1_per_loc_sp_par(o,nsp)

nt=size(o,1);
nmp=size(o,2);
nlocs=size(o,3);

c=nan(nsp,nmp,nlocs);   % AR constant for each sp, yr and loc.
p=nan(nsp,nmp,nlocs);   % AR coeff. for each sp, yr and loc.
r=nan(size(o));         % residuals for each t,yr and loc

[spbd,ntsp,spi]=subPeriodBounds(nt,nsp);

parfor i=1:nlocs
    ic = i
    %disp(['Fitting AR1 for loc. ' num2str(i)]);
    ri=nan(nt,nmp);
    for y=1:nmp
        yc = y
        ry=nan(1,nt);
        for sp=1:nsp
           sp_c = sp
           
           x=o(spbd(sp,1):spbd(sp,2),y,i); % need special cases for sp=1 to ensure no lost data on sp transitions


           [ARcon,ARcoe,~,ARres]=fit_AR1(x);


           c(sp,y,i)=ARcon;
           p(sp,y,i)=ARcoe;
           lb=spbd(sp,1);
           ub=spbd(sp,2);
           ry(lb:ub)=ARres;          
        end
        ri(:,y)=ry; 
    end 
    r(:,:,i)=ri;
    
end