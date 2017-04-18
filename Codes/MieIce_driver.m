% Driver software for determining Mie optical parameters for ice grains by
% calling MieIce.m
% The purpose of this is to expand the lookup library for various sizes of
% ice grains to be incorporated in SNICAR. 

% Written by Joseph Cook (University of Sheffield), December 2016. 

% User defined inputs = CELL RADIUS (line 27)

% OUTPUTS: extinction efficiency (extinction), backscattering efficiency
% (backscattering), absorption efficiency (absorption), asymmetry parameter
% (asymmetry), backscattering:scattering ratio (q_ratio), single scattering
% albedo (ssa),extinction cross section (ExtXC), scttering cross section
% (ScaXC), absorption cross section (AbsXC), volume extinction coefficient
% (ExtXCvol), volume scattering coefficient (ScaXCvol, volume absorption
% coefficient (AbsXCvol), mass extinction coefficient (ExtXCmass), mass
% scattering coefficient (ScaXCmass), mass absorption coefficient
% (AbsXCmass)

extinction=0;
scattering = 0;
absorption = 0;
asymmetry = 0;
q_ratio = 0;
ssa = 0;

r = 10000; % cell radius in um 
XSArea = pi*(r^2); % cross sectional area in meters
IceDensity = 934; % density of ice in kg m-3
IceVol = 4/3*pi*(r^3); % cell vol m3

wvl=0.305:0.01:5;

for i = (1:1:470)
   [qext, qsca, qabs, qb, asy, qratio]=MieIce(wvl(i),r);
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

ExtXCvol = (extinction.*IceVol); % extinction cross section by volume um-3
ScaXCvol = (scattering.*IceVol);
AbsXCvol = (absorption.*IceVol);

ExtXCmass = (ExtXCvol./IceDensity);
ScaXCmass = (ScaXCvol./IceDensity);
AbsXCmass = (AbsXCvol./IceDensity);



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