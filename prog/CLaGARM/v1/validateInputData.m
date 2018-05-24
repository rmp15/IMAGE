%% Data input validation
% 
% Check n data sources have correct metadata
% Record length matches.

function validateInputData(mv)

%required fields for gridded and station data
grid_fields={'name','gridded','nLat','nLon','gLat','gLon','gridinds','o','dims','lbound','ubound'};
stat_fields={'name','gridded','sLat','sLon','o','dims','lbound','ubound'};

nV=length(mv); %number of variable structures passed

for i=1:nV;
    v=mv(i);
    
    % compare dims 1 & 2 to v1, call error if mismatch
    if i==1
        dims1=size(v.o);
    else
        dimsv=size(v.o);
        if dims1(2)~=dimsv(2)
            error(['Dimension 2 (nYears) of var ' num2str(i) ' does not match var 1']);
        end
        if dims1(1)~=dimsv(1)
            error(['Dimension 1 (nDaysinYear) of var ' num2str(i) ' does not match var 1']);
        end
    end
    
    % check all fields are present in current var
    if (v.gridded) 
        vfields=isfield(v, grid_fields);
        if min(vfields)==0
            error(['Missing field(s) in var.' num2str(i) ':' grid_fields{~vfields}]);
        end
    elseif ~(v.gridded)
        vfields=isfield(v, stat_fields);
        if min(vfields)==0
            error(['Missing field(s) in var.' num2str(i) ':' stat_fields{~vfields}]);
        end
    end
    
    % display variable info
    disp(['Variable ' num2str(i)]);
    disp(['Name= ' v.name]);

    disp(['Dims= ' v.dims{1} ' ' v.dims{2} ' ' v.dims{3}]);
    disp(['Dims= ' num2str(size(v.o))]);
    disp(['Gridded= ' num2str(v.gridded)]);
    if v.gridded
        disp(['nLat= ' num2str(v.nLat)]);
        disp(['nLon= ' num2str(v.nLon)]);
    end
    disp(['Lower bound= ' num2str(v.lbound)]);
    disp(['Upper bound= ' num2str(v.ubound)]);
    disp('--------------------');
end

disp('Variables seem alright...');
        
 