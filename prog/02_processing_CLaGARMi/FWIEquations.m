

%
% MATLAB Translation of FWI.vba
%
%'*******************************************************************************************
%'*
%'* Description: VBA module containing functions to calculate the components of
%'*              the Canadian Fire Weather Index system, as described in
%'*
%'*      Van Wagner, C.E. 1987. Development and structure of the Canadian Forest Fire
%'*      Weather Index System. Can. For. Serv., Ottawa, Ont. For. Tech. Rep. 35. 37 p.
%'*
%'*      Equation numbers from VW87 are listed throughout, to the right of the equations in
%'*      in the code.
%'*   
%'*      An more recent technical description can be found in:
%'*      http://www.cawcr.gov.au/publications/technicalreports/CTR_010.pdf
%'*
%'*      This module is essentially a direct C to VBA translation of Kerry Anderson's
%'*      fwi84.c code. The latitude adjustments were developed by Marty Alexander, and used
%'*      over Indonesia in the paper:
%'*
%'*      Field, R.D., Y. Wang, O. Roswintiarti, and Guswanto. A drought-based predictor of
%'*      recent haze events in western Indonesia. Atmospheric Environment, 38, 1869-1878, 2004.
%'* 
%'*      A technical description of the latitude adjustments can be found in Appendix 3 of:
%'*      http://cfs.nrcan.gc.ca/pubwarehouse/pdfs/29152.pdf
%'*
%'*      Robert Field, robert.field@utoronto.ca
%'*******************************************************************************************


%'*******************************************************************************************
%'* Function Name: FFMC
%'* Description: Calculates today's Fine Fuel Moisture Code
%'* Parameters:
%'*    TEMP is the 12:00 LST temperature in degrees celsius
%'*    RH is the 12:00 LST relative humidity in %
%'*    WIND is the 12:00 LST wind speed in kph
%'*    RAIN is the 24-hour acculumalted rainfall in mm, calculated at 12:00 LST
%'*    FFMCo is the previous day's FFMC
%'*******************************************************************************************
function FFMC = FFMCCalc(TEMP,RH,WIND,RAIN,FFMCPrev)
    
%    Dim Mo, rf, Mr, Ed, Ew, ko, kd, kl, kw, m, F As Double
          
    Mo = 147.2 * (101.0 - FFMCPrev) / (59.5 + FFMCPrev);               %'''/* 1  '*/
    if (RAIN > 0.5) 
        rf = RAIN - 0.5;                                      %'''/* 2  '*/
        if (Mo <= 150.0) 
           Mr = Mo + ...
            42.5 * rf * (exp(-100.0 / (251.0 - Mo))) * (1 - exp(-6.93 / rf)); %'''/* 3a '*/
        else
           Mr = Mo + ...
                42.5 * rf * (exp(-100.0 / (251.0 - Mo))) * (1 - exp(-6.93 / rf)) + ...
                0.0015 * (Mo - 150.0) ^ 2 * (rf) ^ (0.5); %'''/* 3b '*/
        end 
        if (Mr > 250.0) 
           Mr = 250.0;
        end 
        Mo = Mr;
    end
    Ed = 0.942 * (RH) ^ (0.679) + ...
           11.0 * exp((RH - 100.0) / 10.0) + 0.18 * (21.1 - TEMP) * (1.0 - exp(-0.115 * RH)); %'''/* 4  '*/
    if (Mo > Ed) 
        ko = 0.424 * (1.0 - (RH / 100.0) ^ 1.7) + ...
              0.0694 * (WIND) ^ (0.5) * (1.0 - (RH / 100.0) ^ 8.0); %'''/* 6a '*/
        kd = ko * 0.581 * exp(0.0365 * TEMP);                %'''/* 6b '*/
        m = Ed + (Mo - Ed) * (10.0) ^ (-kd);                %'''/* 8  '*/
    else
        Ew = 0.618 * (RH) ^ (0.753) + ...
           10.0 * exp((RH - 100.0) / 10.0) + ...
           0.18 * (21.1 - TEMP) * (1.0 - exp(-0.115 * RH));   %'''/* 5  '*/
        if (Mo < Ew) 
           kl = 0.424 * (1.0 - ((100.0 - RH) / 100.0) ^ 1.7) + ...
            0.0694 * (WIND) ^ 0.5 * (1 - ((100.0 - RH) / 100.0) ^ 8.0); %'''/* 7a '*/
           kw = kl * 0.581 * exp(0.0365 * TEMP);             %'''/* 7b '*/
           m = Ew - (Ew - Mo) * (10.0) ^ (-kw);             %'''/* 9  '*/
        else
           m = Mo;
        end
    end
    FFMC = 59.5 * (250.0 - m) / (147.2 + m);                    %'''/* 10 '*/

end

%'*******************************************************************************************
%'* Function Name: DMC
%'* Description: Calculates today's Duff Moisture Code
%'* Parameters:
%'*    TEMP is the 12:00 LST temperature in degrees celsius
%'*    RH is the 12:00 LST relative humidity in %
%'*    RAIN is the 24-hour acculumalted rainfall in mm, calculated at 12:00 LST
%'*    DMCPrev is the previous day's DMC
%'*    Lat is the latitude in decimal degrees of the location for which calculations are being made
%'*    Month is the month of Year (1..12) for the current day's calculations.
%'*******************************************************************************************
function DMC = DMCCalc(TEMP,RH,RAIN,DMCPrev,MONTH,LAT)


 %   Dim re, Mo, Mr, K, B, P, Pr, Dl As Double
 
    if (RAIN > 1.5) 
        re = 0.92*RAIN - 1.27;                                %'''/* 11  '*/
        Mo = 20.0 + exp(5.6348 - DMCPrev / 43.43);               %   '''/* 12  '*/
        if (DMCPrev <= 33.0) 
           B = 100.0 / (0.5 + 0.3 * DMCPrev);                    %   '''/* 13a '*/
        else
           if (DMCPrev <= 65.0) 
              B = 14.0 - 1.3 * (log(DMCPrev));                   %   '''/* 13b '*/
           else
              B = 6.2 * log(DMCPrev) - 17.2;                    %   '''/* 13c '*/
           end
        end
        Mr = Mo + 1000.0 * re / (48.77 + B * re);              %'''/* 14  '*/
        Pr = 244.72 - 43.43 * log(Mr - 20.0);                  %'''/* 15  '*/
        if (Pr > 0.0) 
           DMCPrev = Pr;
        else
           DMCPrev = 0.0;
        end
    end
    
    if (TEMP > -1.1)
        Dl = DayLength(LAT, MONTH);
        K = 1.894 * (TEMP + 1.1) * (100.0 - RH) * Dl * 0.000001;
    else
        K = 0;
    end
    DMC = DMCPrev + 100.0 * K;                                      % '''/* 17  '*/
    

end


%*******************************************************************************************
%* Function Name: DC
%* Description: Calculates today's Drought Code
%* Parameters:
%*    TEMP is the 12:00 LST temperature in degrees celsius
%*    RAIN is the 24-hour acculumalted rainfall in mm, calculated at 12:00 LST
%*    DCPrev is the previous day's DC
%*    Lat is the latitude in decimal degrees of the location for which calculations are being made
%*    Month is the month of Year (1..12) for the current day's calculations.
%*******************************************************************************************
function DCNew = DCCalc(TEMP, RAIN, DCPrev,MONTH ,LAT)

    %Dim rd, Qo, Qr, V, D, Dr, Lf As Double
    

    if (RAIN > 2.8) 
        rd = 0.83*(RAIN) - 1.27;                              %'/* 18  */
        Qo = 800*exp(-DCPrev/400);                         % '/* 19  */
        Qr = Qo + 3.937*rd;                                % '/* 20  */
        Dr = 400*log(800/Qr);                          % '/* 21  */
        if (Dr > 0) 
           DCPrev = Dr;
        else
           DCPrev = 0;
        end
    end

    Lf = DayLengthFactor(LAT, MONTH);
     
    if (TEMP > -2.8) 
        V = 0.36*(TEMP + 2.8) + Lf;                          %  '/* 22  */
    else
        V = Lf;
    end 
     
    if (V < 0) 
        V = 0;
    end
    D = DCPrev + 0.5 * V;                                      %  '/* 23  */

    DCNew = D;

end




%'*******************************************************************************************
%'* Function Name: ISI
%'* Description: Calculates today's Initial Spread Index
%'* Parameters:
%'*    WIND is the 12:00 LST wind speed in kph
%'*    FFMC is the current day's FFMC
%'*******************************************************************************************

function ISI = ISICalc(WIND,FFMC)


%    Dim fWIND, m, fF, R As Double
     
    fWIND = exp(0.05039 * WIND);                                   %'''/* 24  '*/
    m = 147.2 * (101 - FFMC) / (59.5 + FFMC);                      %'''/* 1   '*/
    fF = 91.9 * exp(-0.1386 * m) * (1.0 + (m) ^ 5.31 / 49300000.0); %'''/* 25  '*/
    ISI = 0.208 * fWIND * fF;                                     %'''/* 26  '*/
     
end

%'*******************************************************************************************
%'* Function Name: BUI
%'* Description: Calculates today's Buildup Index
%'* Parameters:
%'*    DMC is the current day's Duff Moisture Code
%'*    DC is the current day's Drought Code
%'*******************************************************************************************
function BUI = BUICalc(DMC,DC)

%    Dim U As Double
    
    if (DMC <= 0.4 * DC) 
        U = 0.8 * DMC * DC / (DMC + 0.4 * DC);                      %'''/* 27a '*/
    else
        U = DMC - (1.0 - 0.8 * DC / (DMC + 0.4 * DC)) ...
           * (0.92 + (0.0114 * DMC) ^ 1.7);                  %'''/* 27b '*/
    end
    
    BUI = U;

end

%'*******************************************************************************************
%'* Function Name: FWI
%'* Description: Calculates today's Fire Weather Index
%'* Parameters:
%'*    ISI is current day's ISI
%'*    BUI is the current day's BUI
%'*******************************************************************************************

function FWI = FWICalc(ISI,BUI)
    
%    Dim fD, B, S As Double

    if (BUI <= 80.0) 
        fD = 0.626 * (BUI) ^ 0.809 + 2.0 ;                    %'''/* 28a '*/
    else
        fD = 1000.0 / (25.0 + 108.64 * exp(-0.023 * BUI));        %'''/* 28b '*/
    end
    B = 0.1 * ISI * fD ;                                      % '''/* 29  '*/
    if (B > 1.0) 
        S = exp(2.72 * (0.434 * log(B)) ^ 0.647);         %'''/* 30a '*/
    else
        S = B ;                                               %'''/* 30b '*/
    end
    
    FWI = S;


end


%'*******************************************************************************************
%'* Function Name: DSR
%'* Description: Calculates today's Daily Severity Rating
%'* Parameters:
%'*    FWI is current day's FWI
%'*******************************************************************************************

function DSR =  DSRCalc(FWI)
    
    DSR = 0.0272 * (FWI ^ 1.77);             %'''/* 41 '*/

end





%*******************************************************************************************
%'* Function Name: DayLengthFactor
%'* Description: Calculates latitude/date dependent day length factor for Drought Code
%'* Parameters:
%'*      Latitude is latitude in decimal degrees of calculation location
%'*      Month is integer (1..12) value of month of year for which calculation is being made
%'*
%'*******************************************************************************************
function DLF= DayLengthFactor(Latitude,MONTH)

    LfN = [-1.6, -1.6, -1.6, 0.9, 3.8, 5.8, 6.4, 5, 2.4, 0.4, -1.6, -1.6];
    LfS = [6.4, 5, 2.4, 0.4, -1.6, -1.6, -1.6, -1.6, -1.6, 0.9, 3.8, 5.8];


%    '/* Use Northern hemisphere numbers */
    if (Latitude > 15)
        retVal = LfN(MONTH);
    
%'    '/* Use Equatorial numbers */
    elseif (Latitude <= 15 & Latitude > -15)
        retVal = 1.39;

%    '/* Use Southern hemisphere numbers */
    elseif (Latitude <= -15)
        retVal = LfS(MONTH);
    end

    DLF = retVal;

end



%'*******************************************************************************************
%'* Function Name: DayLength
%'* Description: Calculates latitude/date dependent day length for DMC calculation
%'* Parameters:
%'*      Latitude is latitude in decimal degrees of calculation location
%'*      Month is integer (1..12) value of month of year for which calculation is being made
%'*
%'*******************************************************************************************

function DL = DayLength(Latitude,MONTH)

    %'''/* Day Length Arrays for four diff't latitude ranges '*/
    DayLength46N = [6.5, 7.5, 9, 12.8, 13.9, 13.9, 12.4, 10.9, 9.4, 8, 7, 6];
    DayLength20N = [7.9, 8.4, 8.9, 9.5, 9.9, 10.2, 10.1, 9.7, 9.1, 8.6, 8.1, 7.8];
    DayLength20S = [10.1, 9.6, 9.1, 8.5, 8.1, 7.8, 7.9, 8.3, 8.9, 9.4, 9.9, 10.2];
    DayLength40S = [11.5, 10.5, 9.2, 7.9, 6.8, 6.2, 6.5, 7.4, 8.7, 10, 11.2, 11.8];

    %''/* default to return error code '*/
    retVal = NaN;
    
    %''/*
    %'    Use four ranges which respectively span:
    %'        - 90N to 33 N
    %'        - 33 N to 0
    %'        - 0 to -30
    %'        - -30 to -90
    %'*/
    if ((Latitude <= 90) & (Latitude > 33)) 
        retVal = DayLength46N(MONTH);
    elseif ((Latitude <= 33) & (Latitude > 15)) 
        retVal = DayLength20N(MONTH);
    elseif ((Latitude <= 15) & (Latitude > -15)) 
        retVal = 9;
    elseif ((Latitude <= -15) & (Latitude > -30)) 
        retVal = DayLength20S(MONTH);
    elseif ((Latitude <= -30) & (Latitude >= -90)) 
        retVal = DayLength40S(MONTH);
    end

    DL = retVal;
end


