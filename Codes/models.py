import logging
import bioutils
import numpy as np
import scipy.integrate
import os


class PigmentedCell:
    def __init__(self, size, water_fraction=0.8, dry_density=1400, nm=1.5, wavelengths=(300, 1300)):

        """

        :param size: size parameter x, calculated in separate code
        :param  water_fraction: water fraction in cell (can be assumed constant 0.8)
        :param dry_density: density of dry material (can be assumed constant 1400)
        :param nm: real part of RI
        """
        # Assign values for X, Xw, Rho and nm.
        # X is the size parameter calculated in a separate script
        # Xw is water fraction in cell. Dauchet et al (2015) shows it can be
        # assumed constant at 0.8.
        # Rho is density of dry material. Dauchet et al (2015) show this can be assumed
        # constant at 1400 for algal cells
        # nm is the real part of the refractive index of the surrounding medium, i.e. ice.
        self.log = logging.getLogger('PigmentedCell')


        self.min_pigment_wavelength = min(wavelengths)
        self.max_pigment_wavelength = max(wavelengths)

        # create a list of 1nm spaced wavelengths between min and max wavelengths inclusive
        #wl is in m, wlnano in nm
        self.WL = bioutils.wavelength_array_m(self.min_pigment_wavelength, self.max_pigment_wavelength)
        self.WLnano = bioutils.wavelength_array_nm(self.min_pigment_wavelength, self.max_pigment_wavelength)

        self.wavelength_bands = self.max_pigment_wavelength + 1 - self.min_pigment_wavelength

        self.x = size
        self.xw = water_fraction
        self.density = dry_density # Rho
        self.nm = nm # is the real part of the refractive index of the surrounding medium, i.e. ice.

        # this only needs to be done once.
        self.klist = calculate_K_list(self.WL, dry_density, water_fraction)

        # set up variables affected by pigmentation
        self.Kint = 0
        self.pigments = {}
        self.wlk = {}
        self.K = np.zeros(self.wavelength_bands)
        self.eww = np.zeros(self.wavelength_bands)

    def refractive_index_imag(self, wavelength_array):



        # n = index of array, wl = value of array. Iterate element-wise and
        # append to new_array K for each wavelength.

        k_at_wl = np.array([self.wlk[wl] for wl in wavelength_array])
        
        # for n, wl in enumerate(wavelength_array):
        #     new_array.append(wlk[wl])
        # convert new_array to numpy array
        #new_array = np.array(new_array)

        # for each wavelength, use the corresponding K value in RI calculation
        
        m_hulis = 1.5 - k_at_wl * 1j
        n = 1*(m_hulis ** 2 - 1) / (m_hulis ** 2 + 2)  # manually alter the multiplier (default = 1 for 20um cells) to experiment with cell size
        
        return n.imag


    def load_pigment_from_file(self, pigment, filename, mass_fraction=0, delay_update=False):

        ## sanity check
        # make sure the total mass fraction between 0 and 1
        current_mass_fraction = sum([pigment['mass_fraction'] for pigment in self.pigments.values()])
        if (mass_fraction + current_mass_fraction) > 1:
            raise ValueError('Cannot have mass fraction > 1 current={} + {}={}'.format(current_mass_fraction, pigment, mass_fraction))
        if mass_fraction < 0:
            raise ValueError('Cannot have a negative mass_fraction: {}'.format(mass_fraction))

        csvdata = bioutils.load_pigment_file(filename, self.min_pigment_wavelength, self.max_pigment_wavelength)

        self.pigments[pigment] = {'abs': csvdata, 'mass_fraction': mass_fraction}

        if not delay_update:
            self.update_pigment()


    def update_pigment(self):
        self.eww, self.K = calculate_pigmentation(self.wavelength_bands, self.pigments.values(), self.klist)

        # new variable wlk zips wavelength WL and K from Bio_Optical_Model
        self.wlk = dict(zip(self.WL, self.K))
        self.Kint = calculate_intergrated_k(self.K, self.wavelength_bands)




def calculate_K_list(WL, cell_density, xw):
    '''

    :param WL:
    :param cell_density:
    :param xw:
    :return: K_list (array containing K at every wavelength
    '''
    # for each wavelength, calculate the absorption index (using equations from
    # Pottier et al 2005). K is spectral and can be fed directly into the RTM or
    # integrated across the waveband using the code below
    #  for k at wl
    # k(wl)  = wl/4 PI    *  rho *    (1-xw) / xw

    # for i in self.WL:
    #     k = (i / (4 * np.pi)) * self.density * ((1 - self.xw) / self.xw)
    #     self.klist.append(k)
    return (WL / (4 * np.pi)) * cell_density * ((1 - xw) / xw)


def calculate_pigmentation(wavebands, pigments, klist):
    '''

    :param WL: wavelenths in m
    :param pigments: array of pigment dictionaries
    :param cell_density:
    :param water_content:
    :return:
    '''

    # Sum all pigments
    eww = np.zeros(wavebands)

    for pigment in pigments:
        eww += pigment['abs'] * pigment['mass_fraction']

    K = eww * klist

    return eww, K

def calculate_intergrated_k(K, wavebands):
    '''

    :param K:
    :param wavebands:
    :return:
    '''
    # Integrate K values across visible waveband using Simpson's method
    return scipy.integrate.simps(K) / wavebands
