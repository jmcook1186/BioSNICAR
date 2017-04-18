% Driver software for determining the mie optical parameters for biological
% cells to feed into BioSNICAR. Calls mie.m, which should be available in
% workspace. Written by Joseph Cook (University of Sheffield, UK), Feb 2017.

%User defined inputs = CELL DIAMETER (line 12) AND ABSORPTION COEFFICIENT
%(PROVIDE BY IMPORTING RELEVANT FILE TO WORKSPACE AND NAMING 'KK') 

% OUTPUTS: extinction efficiency (extinction), backscattering efficiency
% (backscattering), absorption efficiency (absorption), asymmetry parameter
% (asymmetry), backscattering:scattering ratio (q_ratio), single scattering
% albedo (ssa),extinction cross section (ExtXC), scttering cross section
% (ScaXC), absorption cross section (AbsXC), volume extinction coefficient
% (ExtXCvol), volume scattering coefficient (ScaXCvol, volume absorption
% coefficient (AbsXCvol), mass extinction coefficient (ExtXCmass), mass
% scattering coefficient (ScaXCmass), mass absorption coefficient
% (AbsXCmass)


%define wavelength range
WL = 0.305:0.001:5;

%define cell dimensions
d = 30; % cell diameter in um (consistent with WL unit in mie.m)
CellDensity = 1400; % density 1400 kg m-3
CellVol = 4/3* pi * ((d*1e-6)/2)^3; % cell vol m3
XSArea = pi*((d*1e-6)/2)^2; % cell XS area m2

%Calculate Mie size parameter
XX = pi * d ./ WL

%call mie.m with XX and KK values
for i = 1:1:2500
    m = complex(1.5,KK(i)); % adjust real part of the RI if necessary (default for cells is 1.5 after Dauchet et alk. 2005)
    x = XX(i); %read in size parameter
    [qext qsca qabs qb asy qratio] = Mie(m,x); % send size param and imaginary RI to mie.m for each wavelength
    extinction(i)=qext;
    scattering(i) = qsca;
    absorption(i) = qabs;
    backscattering(i) = qb;
    asymmetry(i) = asy;
    q_ratio(i) = qratio;
    ssa(i) = qsca/qext;
end

%subsample to appropriate resolution for loading into SNICAR
extinction= extinction(1:5:2350);
scattering = scattering(1:5:2350);
backscattering = backscattering(1:5:2350);
absorption = absorption(1:5:2350);
asymmetry = asymmetry(1:5:2350);
q_ratio = q_ratio(1:5:2350);
ssa = ssa(1:5:2350);

% Calculate Cross Sections (efficiency = cross section / mass, area or volume).
% Since Q is already expressed as per unit area (see Matzler 2002), first multiply by area
% then normalise to geometry of choice

ExtXC = (extinction);
ScaXC = (scattering);
AbsXC = (absorption);

ExtXCvol = (extinction/XSArea).*CellVol;
ScaXCvol = (scattering/XSArea).*CellVol;
AbsXCvol = (absorption/XSArea).*CellVol;

ExtXCmass = (((extinction*XSArea)./(CellVol*CellDensity))); % MAC in kg m-3
ScaXCmass = (((scattering*XSArea)./(CellVol*CellDensity))); % MAC in kg m-3
AbsXCmass = (((absorption*XSArea)./(CellVol*CellDensity))); % MAC in kg m-3


% Plots 

plot(ExtXCmass)
xlabel('Wavelength')
ylabel('Cext')

% figure
% plot(ssa)
% xlabel ('wavelength')
% ylabel('ssa')
% 
% figure
% plot(extinction)
% xlabel ('wavelength')
% ylabel('extinction efficiency')
% 
% figure
% plot(scattering)
% xlabel ('wavelength')
% ylabel('scattering efficiency')
% 
% figure
% plot(absorption)
% xlabel ('wavelength')
% ylabel('absorption efficiency')
% 
% figure
% plot(asymmetry)
% xlabel ('wavelength')
% ylabel('asymmetry parameter (g)')