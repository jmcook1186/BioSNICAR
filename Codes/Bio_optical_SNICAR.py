# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 09:09:57 2017

@author: Joseph Cook
"""
# Code designed to provide the imaginary part of the refractive index for algal cells
# to feed into a Mie solver (Mie.m) and determine the optical properties of algal cells
# for BIOSNICAR

# Written by Joseph Cook, University of Sheffield, UK, February 2017

# Dependencies are numpy, matplotlib, pandas (packages) plus bioutils.py and 
# cells.py which are separate scripts to be saved in the working directory

import bioutils
import cells
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# set wavelength range

min_wl = 300
max_wl = 750
WLnano = bioutils.wavelength_array_nm(min_wl, max_wl)


# call cells.py to mix pigments according to values defined below:

cell = cells.generate_species('algae1', 300, 750)
cell = cells.fully_pigmented_cell_generator(size=15, chlorophylla_mf=0.015,
                                            chlorophyllb_mf=0.015,
                                            chlorophylld_mf=0.0,
                                            chlorophyllf_mf=0.0,
                                            photoprotective_carotenoids_mf=0.05,
                                            photosynthetic_carotenoids_mf=0.05,
                                            phycocyanin_mf=0.00,
                                            phycoerythrin_mf=0.0,
                                            allophycocyanin_mf=0.0,
                                            min_wl=min_wl,
                                            max_wl=max_wl
                                            )

# Pull output back from cells.py and pad to full wavelength range for compatibility
# with BIOSNICAR. Replace zeros with negligible positive value to avoid /zero error

KK = np.array(cell.K)
KK = np.lib.pad(KK, (0,4550), 'constant', constant_values=(0, 0.000001))

#Optional smoothing function: change window width to smooth more or less
KK = pd.rolling_mean(KK,10,min_periods=1)


# save KK as csv for reading into Mie solver 

#KK = pd.DataFrame(KK)
#KK.to_csv('KK.csv')

# plot and print checks
print('length of KK = ',len(KK)) # should be 5001
print('data type KK = ', type(KK)) # should be pandas dataframe

plt.plot(KK)
plt.xlim(0,750)

