
import numpy as np
import os
import logging


def wavelength_array_m(min_wl, max_wl):
    return np.arange(min_wl, max_wl + 1, dtype=np.float64) * 1E-9


def wavelength_array_nm(min_wl, max_wl):
    return np.arange(min_wl, max_wl + 1, dtype=np.int)



def load_pigment_file(filename, min_pigment_wavelength, max_pigment_wavelength):
    '''
    loads absorbances from file, assumes that the end of the file is the max_pigment_wavelength

    :param filename:
    :param min_pigment_wavelength:
    :param max_pigment_wavelength:
    :return:
    '''
    filepath = os.path.join('data', filename)
    # loaddata from csvfile into float64 array
    csvdata = np.loadtxt(filepath, np.float64, delimiter=',')
    wavelength_bands = max_pigment_wavelength - min_pigment_wavelength + 1
    logging.getLogger('load_pigment_file').warn('''
        from file: {}
        loaded {} rows as absorbances between {}nm and {}nm
        '''.format(filename,
                   len(csvdata), max_pigment_wavelength - len(csvdata) + 1, max_pigment_wavelength,
                   )
                                                )

    if len(csvdata) > wavelength_bands:
        # trim to number of bands
        logging.getLogger('Load_Pigment_File').warn(
            'truncated pigment files between {} and {}'.format(max_pigment_wavelength - len(csvdata), csvdata[0]))
        csvdata = csvdata[-wavelength_bands:]

    elif len(csvdata) < wavelength_bands:
        logging.getLogger('Load_Pigment_File').warn(
            'left padding {} values between {} and {} with {}'.format(wavelength_bands - len(csvdata),
                                                                      min_pigment_wavelength,
                                                                      max_pigment_wavelength - len(csvdata),
                                                                      csvdata[0]))
        # pad the loaded data to arraylen rows. using the value from the first row.
        csvdata = np.pad(csvdata, (wavelength_bands - len(csvdata), 0),
                         'linear_ramp')

    return csvdata

