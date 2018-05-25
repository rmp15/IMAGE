% scale cs to limit PX genned AR mu to within n std devs of observed lims.
function [cs,ps]=limPXARcoef(o,cs,ps,n)

% cap p vals below 1 to prevent divergence
pslim=0.99;
ps(ps>pslim)=pslim;
ps(ps<-pslim)=-pslim;


%calc obs means, mu and theoretical AR means, mucp
mu=sp_mean(o,12);
mucp=cs./(1-ps);

%lims of observed means
mumax=max(mu(:));
mumin=min(mu(:));

%n=1;  %no. of std deviations in excess of observed lims allowed
% +ve exceedance case
e=mucp-mumax;  %excess
ex=e>0;     %positive excess cases
ec=n*(1-exp(-e/n)); %corrected excess, tends to n as e>n
cs(ex)=cs(ex).*((mumax+ec(ex))./mucp(ex)); %scales cs such that muAR is mumax+ec


% % -ve exceedance case
e=mumin-mucp;  %excess
ex=e>0;     %negative excess cases
ec=n*(1-exp(-e/n));  %corrected excess
cs(ex)=cs(ex).*((mumin-ec(ex))./mucp(ex)); %apply correction