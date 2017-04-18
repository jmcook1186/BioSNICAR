function [qext qsca qabs qb asy qratio] = MieIce (WL, r)

%% calcualtes the Mie scattering properties of ice
% uses the imbeded subfunctions Mie and Mie_ab and the external function
% refracICE

% INPUT
% WL = wavelength [um]
% r = effective grain radi [mm]
% T = snow temperature [k]

% OUTPUT 
% qext = Mie extinction efficiency
% qsca = Mie scattering efficiency  
% qabs = Mie absorption efficiency
% qb = Mie backscattering efficiency
% g = asymmetry parameter
% qratio = qb/qsca

%% FUNCTION
% dimensionless size parameter
d = 2*r;

x = pi * d / WL;

% retrieve the complex refractive index for ice
[RN CN] = refracICE(WL);
m = complex(RN, CN);

% calculate Mie Efficiencies;
[qext qsca qabs qb asy qratio] = Mie(m, x);
end

%% SUBFUNCTIONS
function [qext qsca qabs qb asy qratio] = Mie(m, x)

% Computation of Mie Efficiencies for given 

% complex refractive-index ratio m=m'+im" 

% and size parameter x=k0*a, where k0= wave number in ambient 

% medium, a=sphere radius, using complex Mie Coefficients

% an and bn for n=1 to nmax,

% s. Bohren and Huffman (1983) BEWI:TDD122, p. 103,119-122,477.

% Result: m', m", x, efficiencies for extinction (qext), 

% scattering (qsca), absorption (qabs), backscattering (qb), 

% asymmetry parameter (asy=<costeta>) and (qratio=qb/qsca).

% Uses the function "Mie_ab" for an and bn, for n=1 to nmax.

% C. Mätzler, May 2002, revised July 2002.



if x==0                 % To avoid a singularity at x=0

    [qext qsca qabs qb asy qratio] = [0 0 0 0 0 1.5];

elseif x>0              % This is the normal situation

    nmax=round(2+x+4*x.^(1/3));

    n1=nmax-1;

    n=(1:nmax);cn=2*n+1; c1n=n.*(n+2)./(n+1); c2n=cn./n./(n+1);

    x2=x.*x;

    f=Mie_ab(m,x);

    anp=(real(f(1,:))); anpp=(imag(f(1,:)));

    bnp=(real(f(2,:))); bnpp=(imag(f(2,:)));

    g1(1:4,nmax)=[0; 0; 0; 0]; % displaced numbers used for

    g1(1,1:n1)=anp(2:nmax);    % asymmetry parameter, p. 120

    g1(2,1:n1)=anpp(2:nmax);

    g1(3,1:n1)=bnp(2:nmax);

    g1(4,1:n1)=bnpp(2:nmax);   

    dn=cn.*(anp+bnp);

    q=sum(dn);

    qext=2*q/x2;

    en=cn.*(anp.*anp+anpp.*anpp+bnp.*bnp+bnpp.*bnpp);

    q=sum(en);

    qsca=2*q/x2;

    qabs=qext-qsca;

    fn=(f(1,:)-f(2,:)).*cn;

    gn=(-1).^n;

    f(3,:)=fn.*gn;

    q=sum(f(3,:));

    qb=q*q'/x2;

    asy1=c1n.*(anp.*g1(1,:)+anpp.*g1(2,:)+bnp.*g1(3,:)+bnpp.*g1(4,:));

    asy2=c2n.*(anp.*bnp+anpp.*bnpp);

    asy=4/x2*sum(asy1+asy2)/qsca;

    qratio=qb/qsca;

end
end

function result = Mie_ab(m,x)

% Computes a matrix of Mie Coefficients, an, bn, 

% of orders n=1 to nmax, for given complex refractive-index

% ratio m=m'+im" and size parameter x=k0*a where k0= wave number in ambient 

% medium for spheres of radius a;

% Eq. (4.88) of Bohren and Huffman (1983), BEWI:TDD122

% using the recurrence relation (4.89) for Dn on p. 127 and 

% starting conditions as described in Appendix A.

% C. Mätzler, July 2002



z=m.*x;

nmax=round(2+x+4*x.^(1/3));

nmx=round(max(nmax,abs(z))+16);

n=(1:nmax); nu = (n+0.5); 



sx=sqrt(0.5*pi*x);

px=sx.*besselj(nu,x);

p1x=[sin(x), px(1:nmax-1)];

chx=-sx.*bessely(nu,x);

ch1x=[cos(x), chx(1:nmax-1)];

gsx=px-i*chx; gs1x=p1x-i*ch1x;

dnx(nmx)=0+0i;

for j=nmx:-1:2      % Computation of Dn(z) according to (4.89) of B+H (1983)

    dnx(j-1)=j./z-1/(dnx(j)+j./z);

end;

dn=dnx(n);          % Dn(z), n=1 to nmax

da=dn./m+n./x; 

db=m.*dn+n./x;


an=(da.*px-p1x)./(da.*gsx-gs1x);

bn=(db.*px-p1x)./(db.*gsx-gs1x);


result=[an; bn];
end
