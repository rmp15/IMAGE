%Correlated LAtent Gaussian Auto-Regressive Model

% use correlated gaussians to model 1-year of monthly AR parameters (2 per
% site per variable)
% use corrrelated gaussians to model daily residuals
% use iterative approach to improve monthly and daily scale correlations
% separately

function mv=CLaGARMi(nYears,nsp,nIters,mv,sroot)
tic; st=[]; %init section timer for toc_section calls

%% Model options
PREDESEAS=0; %pre transform deseason
DESEASON=1; % post transform deseason
%ARCOEFF=.0; % 0-1, Weight to generated AR coeffs. 0 is mean. 1 is generated.
%XPX=0; %number of overlapping subperiods in XPX gen, 0 is off.
%XPXnEns=100; %no. of ensembles used in XPX minimization
SAVE_ALL=0; % save all model calcs, params...


%% Combine Variables
nVars=length(mv);
o=[];   % obs data  [nDays in year, nYears, nLocations]
lbound=[];   % lower bound of data [nLocs]  e.g. 0 for rain, this enables special treatment of these values during transform
for i=1:nVars
    o=cat(3,o,mv(i).o);
    lbound=[lbound, repmat(mv(i).lbound,1,size(mv(i).o,3))];
end
disp(['Combined var dims= ' num2str(size(o))]);

st=toc_section(st,'Setup');


%% Pre transform Deseason
if PREDESEAS; [op,Smp,Svp]=pre_deseason(o,lbound); end
%if PREDESEAS; [op,Smp,Svp]=deseason(o); end;
if ~PREDESEAS; op=o;Smp=NaN;Svp=NaN; end

%% Forward n-score, deal with bounded cases - e.g. 0s for rain
disp('Transforming');

[opz,oz_dat]=mloc_nscore_sp(op,12); %should try paretotails ecdf method
%[opz,oz_dat]=mloc_nscore(op,'GPtails');
%opzb=opz;
[opzb]=bound_shuffle(o,opz,lbound);
%[opzb]=bound_ranking(o,opz,lbound);
%[opzb]=bound_preserve_mean(o,opz,lbound);% mean or median replacement gives singular
%[opzb]=bound_med(o,opz,lbound);

st=toc_section(st,'n-score');

%% De-seasonalize
if DESEASON; [opzbd,Sm,Sv]=deseason(opzb);end
if ~DESEASON; opzbd=opzb;end

%% Calc AR coeffs + resids
% ![uses hash value to determine whether fitting has been performed
% previously]
% does not use hashing anymore, probs with ettting hash from large data.
% just use filemane now so clear dirs for full refit

hdir=[sroot 'ARfitdat/'];
h=[hdir 'ARfitdat'];
%hdir='interm_data/'; % dir to store intermediate files with hashed filnames
if ~exist([h '.mat'])
    disp('Performing model fitting');
    [c,p,r]=calc_AR1_per_loc_sp_par(opzbd,nsp);  %returns c=constant, p=coefficient, r=resid.
    mkdir(hdir);
    save([h],'c','p','r','-v7.3')
else
    disp('Loading precalculated fitting params');
    load([h '.mat'])
end
%identify fitting failures by comparing theoretical AR mean mu with actual
%mean,opzbd_spm
[c,p]=fixARfit(c,p,opzbd,nsp);

st=toc_section(st,'AR fitting');

%iterate to improve correlation
SIG=[];
%SIGar=[];
s=[];
disp('Simulating...');
for i=1:nIters
    disp(['Iteration: ' num2str(i)]);
    
    %% Generating AR parameters
    %hAR=strcat(hashfilename,'AR',num2str(nYears));
    if i==1
        %         if  1%~exist([hAR '.mat'],'file')
        disp('Generating AR parameters');
        
        %model c,p as correlated random gaussian vars. use mu=c/(1-p) to
        %simplify dependence relationship before normal quantile transf.
        
        mu=c./(1-p);
        mup=cat(3,mu,p);
        [mupz,mupz_dat]=mloc_nscore(mup,'linlim'); %use ll for now. GP requires applying limPXARcoef correction. Later try paretotails ecdf function with kernal smoothing
        
        %[mupsz,SIGar]=PMVNgen_iter(mupz,SIGar,o,s,nYears);
        [mupsz]=PMVNgen(mupz,nYears,sroot);
        mups=mloc_inscore(mupsz,mupz_dat);
        muspu=mups(:,:,1:size(c,3));
        pspu=mups(:,:,1+size(c,3):end);
        
        cspu=muspu.*(1-pspu);
        
        % save([hAR],'cspu','pspu','-v7.3')
        %         else
        %             disp('Loading precalculated AR params');
        %             load([hAR '.mat'])
        %         end
        %[csp,psp]=limPXARcoef(opzbd,cspu,pspu,.1); %scales cs to limit AR means,
        %caps ps below 1 to prevent divergence, Now only required to modify pareto
        %tail extraps of p when using GPtails.
        csp=cspu;psp=pspu;
        
        %{

%%
% l=89;
% muo=c(:,:,l)./(1-p(:,:,l));
% po=p(:,:,l);
% mus=cspu(:,:,l)./(1-pspu(:,:,l));
% ps=pspu(:,:,l);
% mul=csp(:,:,l)./(1-psp(:,:,l));
% pl=psp(:,:,l);
% figure(2);clf
% subplot(1,2,1)
% plot(ps(:),mus(:),'.');hold on
% plot(po(:),muo(:),'.');
% subplot(1,2,2)
% plot(ps(:),mus(:),'.');hold on
% plot(pl(:),mul(:),'.');
% %%
% %[sub1,sub2,sub3]=ind2sub(size(p),7538); %so check o(2,44,10)
% %%
% opzbd_spm=sp_mean(opzbd,nsp);
% figure(4);clf
% plot(opzbd(:,44,10)); hold on
% plot(15+30.5*[0:11],opzbd_spm(:,44,10));
% plot(15+30.5*[0:11],mu(:,44,10));

%%
        %}
        %allow relaxation to clim means of mu
        
        % calc mean across years of c,p
        mu=c./(1-p);
        mum=repmat(mean(mu,2),[1 nYears 1]); %mu[nsp,nlocs]
        %csm=repmat(mean(c,2),[1 nYears 1]);  %cm[nsp,nlocs]
        %psm=repmat(mean(p,2),[1 nYears 1]);  %pm[nsp,nlocs]
        
        musp=csp./(1-psp);
        
        %load P %
        % ARC=repmat(P,nsp,nYears,1);
        ARC=1;
        % create weighted coeffs
        mus=ARC.*musp+(1-ARC).*mum;
        %ps=PXCOEFF.*psp+(1-PXCOEFF).*psm;
        ps=psp;
        cs=mus.*(1-ps);
    end
    st=toc_section(st,'Simming coeffs.');
    
    % %% Re-infer residuals
    %r=reinfer_res(o,c,p);
    
    %% Generate resids.
    %h=DataHash({r,nsp,nYears,'MVAREOF'});
    %if ~exist([hdir h '.mat']) || 1
    disp('Generating residuals');
    
    %if i==1; %for testing AR iteration keep rs constant
    [rz,rz_dat]=mloc_nscore(r,'linlim');
    [rs,SIG]=MVNgen_iter(r,SIG,o,s,nYears);
    
    %[rsz,rsz_dat] =mloc_nscore(rsz,'linlim');
    rs=mloc_inscore(rs,rz_dat);
    %end
    st=toc_section(st,'Gen. resids.');
    
    %% Simulate (by t)
    spzd=simAR_sp(cs,ps,rs);
    st=toc_section(st,'Main sim.');
    
    %[css,pss,rss]=calc_AR1_per_loc_sp_par(spzd,nsp); %fitting to simulation output
    %save('cpr5s','cs','ps','rs');
    
    %% Re-seasonalize
    if DESEASON; [spz]=reseason(spzd,Sm,Sv); end
    if ~DESEASON; spz=spzd; end
    
    %% Inverse n-score using mixed model back trans data.
    disp('Back Transforming');
    [spz,~] = mloc_nscore_sp(spz,12);
    sp=mloc_inscore_sp(spz,oz_dat,12);
    st=toc_section(st,'Back n-score');
    
    %% Post back transform reseason
    if PREDESEAS; s=reseason(sp,Smp,Svp); end
    if ~PREDESEAS; s=sp; end
    
    %     %% test convergence of mm
    %     ospm=sp_mean(o(:,:,:),nsp);
    %     sspm=sp_mean(s(:,:,:),nsp);
    %     opm=permute(ospm,[2 1 3]);
    %     opm=opm(:,:);
    %     spm=permute(sspm,[2 1 3]);
    %     spm=spm(:,:);
    %     o_c=corr(opm);
    %     s_c=corr(spm);
    %     figure(2);
    %     subplot(2,5,i)
    %     plot(o_c(:),s_c(:),'k.');
    %     xlim([-1 1]);ylim([-1 1]);
    %     subplot(2,5,i+5)
    %     hist(o_c(:)-s_c(:),100);
    
    
    %%
    
end

%% Separate Data
st=toc_section(st,'Finishing');
disp('Separating variables');
lCount=1;
for i=1:length(mv)
    nlocsi=size(mv(i).o,3);
    mv(i).s=single(s(:,:,lCount:lCount+nlocsi-1));
    mv(i).nsp=nsp;
    mv(i).timing=st;
    %mv(i).Sm=Sm;
    %mv(i).Sv=Sv;
    %mv(i).Smp=Smp;
    %mv(i).Svp=Svp;
    mv(i).PREDESEAS=PREDESEAS;
    mv(i).DESEASON=DESEASON;
    %mv(i).PXCOEFF=ARCOEFF;
    %mv(i).XPX=XPX;
    %mv(i).XPXnEns=XPXnEns;
    
    if SAVE_ALL
        mv(i).sp=single(sp(:,:,lCount:lCount+nlocsi-1));
        mv(i).spz=single(spz(:,:,lCount:lCount+nlocsi-1));
        mv(i).spzd=single(spzd(:,:,lCount:lCount+nlocsi-1));
        mv(i).op=op(:,:,lCount:lCount+nlocsi-1);
        mv(i).opz=opz(:,:,lCount:lCount+nlocsi-1);
        mv(i).opzb=opzb(:,:,lCount:lCount+nlocsi-1);
        mv(i).opzbd=opzbd(:,:,lCount:lCount+nlocsi-1);
        mv(i).c=c(:,:,lCount:lCount+nlocsi-1);
        mv(i).p=p(:,:,lCount:lCount+nlocsi-1);
        mv(i).r=r(:,:,lCount:lCount+nlocsi-1);
        mv(i).rs=rs(:,:,lCount:lCount+nlocsi-1);
        mv(i).cs=cs(:,:,lCount:lCount+nlocsi-1);
        mv(i).ps=ps(:,:,lCount:lCount+nlocsi-1);
        %         mv(i).rss=rss(:,:,lCount:lCount+nlocsi-1);
        %         mv(i).css=css(:,:,lCount:lCount+nlocsi-1);
        %         mv(i).pss=pss(:,:,lCount:lCount+nlocsi-1);
        mv(i).cspu=cspu(:,:,lCount:lCount+nlocsi-1);
        mv(i).pspu=pspu(:,:,lCount:lCount+nlocsi-1);
        mv(i).o_nscore=oz_dat(lCount:lCount+nlocsi-1);
        % mv(i).o_nscore_mixed=o_nscore_mixed(lCount:lCount+nlocsi-1);
    end
    lCount=lCount+nlocsi;
end