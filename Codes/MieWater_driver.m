% Driver for mieWATER.m
% inputs are particle radius (r, mm)
% Written by Joseph Cook, Feb 2017, University of Sheffield, UK

extinction=0;
scattering = 0;
absorption = 0;
asymmetry = 0;
q_ratio = 0;
ssa = 0;

r = 1100; % cell radius in um 
XSArea = pi*((r)^2); % cross sectional area in meters
WatDensity = 999; % density of water at 1 degree C in kg m-3
WatVol = 4/3* pi * (r/1E-3)^3; % cell vol m3

wvl=0.305:0.01:5;

for i = (1:1:470)
   [qext, qsca, qabs, qb, asy, qratio]=mieWATER(wvl(i),r);
   wvl(i) % report wavelength as check
   extinction(i)=qext;
   scattering(i) = qsca;
   absorption(i) = qabs;
   backscattering(i) = qb;
   asymmetry(i) = asy;
   q_ratio(i) = qratio;
   ssa(i) = qsca/qext;
end


ExtXC = (extinction.*XSArea);
ScaXC = (scattering.*XSArea);
AbsXC = (absorption.*XSArea);

ExtXCvol = (extinction.*WatVol);
ScaXCvol = (scattering.*WatVol);
AbsXCvol = (absorption.*WatVol);

ExtXCmass = (ExtXCvol./WatDensity);
ScaXCmass = (ScaXCvol./WatDensity);
AbsXCmass = (AbsXCvol./WatDensity);



plot(ExtXCmass)
xlabel('Wavelength')
ylabel('Cext')

figure
plot(ssa)
xlabel ('wavelength')
ylabel('ssa')

figure
plot(extinction)
xlabel ('wavelength')
ylabel('extinction efficiency')

figure
plot(scattering)
xlabel ('wavelength')
ylabel('scattering efficiency')

figure
plot(absorption)
xlabel ('wavelength')
ylabel('absorption efficiency')

figure
plot(asymmetry)
xlabel ('wavelength')
ylabel('asymmetry parameter (g)')