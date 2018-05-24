% calculate the bounds of each subtime period and number of t steps within
% each period.

function [spbounds,ntsp,spi,spr]=subPeriodBounds(nt,nsp)

stlen=nt/nsp;
spbounds=round([[1 (1:(nsp-1))*stlen+1] ; ...
          [((1:(nsp-1))*stlen) nt]])';
ntsp=spbounds(:,2)-spbounds(:,1)+1;


spi=nan(nt,1);  %subperiod index by t
for sp=1:nsp
    spi(spbounds(sp,1):spbounds(sp,2))=sp;
    spr{sp}=spbounds(sp,1):spbounds(sp,2);
end