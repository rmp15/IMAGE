% Calculate AR params - 1 fit per location, implement sub per. later

function [Const,AR1c,AR1v,resids,exitflag]=fit_AR1(x)

mod_AR1=arima('ARLags',1);
lenx = length(x);

xval_inds = ~isnan(x);
xnan_inds = isnan(x);
try
    [model_arima_fit]= estimate(mod_AR1,x,'display','off');
    [resids,~] = infer(model_arima_fit,x);

    Const = model_arima_fit.Constant;     %AR constant, c
    AR1c = cell2mat(model_arima_fit.AR);  %AR coefficient, phi
    AR1v= model_arima_fit.Variance;
    resids(xval_inds) = resids;
    resids(xnan_inds) = NaN;
    
    
catch
    Const = 0;
    AR1c = 0;
    AR1v = 0;
    resids = NaN(lenx,1);
    
    
end
%model_arima_fit = estimate(mod_AR1,x);

