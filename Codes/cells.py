# This script builds cells of user-defined species of microbiota to add to the
# snowpack.

from models import PigmentedCell
import logging

# fully_pigmented_cell_generator is a function that takes the mass fractions of each
# pigment, loads the pigment absorption spectrum and returns a single, pigmented cell

def fully_pigmented_cell_generator(size,
                                   chlorophylla_mf=0.013,
                                   chlorophyllb_mf=0.013,
                                   chlorophylld_mf=0.0015,
                                   chlorophyllf_mf=0.0,
                                   photoprotective_carotenoids_mf=0.045,
                                   photosynthetic_carotenoids_mf=0.0344,
                                   phycocyanin_mf=0.00,
                                   phycoerythrin_mf=0.0,
                                   allophycocyanin_mf=0.0,
                                   min_wl=300,
                                   max_wl=750
                                   ):
    cell = PigmentedCell(size=size, wavelengths=(min_wl, max_wl))

    # load pigment absorbance values from files left padding the data with the initial value.
    # Assign mass fraction of each pigment in cell (e.g. 1% = 0.01)

    cell.load_pigment_from_file('chlorophylla', 'Chlorophyll-a.csv', mass_fraction=chlorophylla_mf)
    cell.load_pigment_from_file('chlorophyllb', 'Chlorophyll-b.csv', mass_fraction=chlorophyllb_mf)
    cell.load_pigment_from_file('photoprotective_carotenoids', 'Photoprotective_carotenoids.csv',
                                mass_fraction=photoprotective_carotenoids_mf)
    cell.load_pigment_from_file('photosynthetic_carotenoids', 'Photosynthetic_carotenoids.csv',
                                mass_fraction=photosynthetic_carotenoids_mf)
    cell.load_pigment_from_file('phycocyanin', 'Phycocyanin.csv', mass_fraction=phycocyanin_mf)
    cell.load_pigment_from_file('phycoerythrin', 'phycoerythrin.csv', mass_fraction=phycoerythrin_mf)
    cell.load_pigment_from_file('allophycocyanin', 'Allophycocyanin.csv', mass_fraction=allophycocyanin_mf)
    cell.load_pigment_from_file('chlorophylld', 'chlorophyll-d.csv', mass_fraction=chlorophylld_mf)
    cell.load_pigment_from_file('chlorophyllf', 'chlorophyll-f.csv', mass_fraction=chlorophyllf_mf)
    return cell

# generate_species defines species as classes, using user-defined pigment mass fractions and the 
# function 'fully_pigmented_cell_generator'. This allows
# predefined pigment compositions to be called simply by using the species name rather
# than manually adjusting pigment mass fractions each model run. Different classes
# could be created for 'algae_week1', 'algae_week2', 'algae_week3' for example to 
# simulate changing pigmentation of the same algal species over time.


# manually alter pigment mass fractions 1.0 = 100% of total cell dry mass, 0.01 = 1% total cell dry mass.

def generate_species(species, wl_min, wl_max):
    logging.getLogger('generate_species').error('WARNING PIGMENTATION WEIGHTING IS INCORRECT FOR CELLS')
    
    if species == 'algae1':
        cell = fully_pigmented_cell_generator(size=40, chlorophylla_mf=0.01,
                                              chlorophyllb_mf=0.0,
                                              chlorophylld_mf=0.,
                                              chlorophyllf_mf=0,
                                              photoprotective_carotenoids_mf=0.00,
                                              photosynthetic_carotenoids_mf=0.0,
                                              phycocyanin_mf=0.02,
                                              phycoerythrin_mf=0.02,
                                              allophycocyanin_mf=0.0,
                                              min_wl=wl_min, max_wl=wl_max
                                              )
    elif species == 'algae2':
        cell = fully_pigmented_cell_generator(size=15, chlorophylla_mf=0.0194,
                                              chlorophyllb_mf=0.0120,
                                              chlorophylld_mf=0.0015,
                                              chlorophyllf_mf=0.0,
                                              photoprotective_carotenoids_mf=0.0,
                                              photosynthetic_carotenoids_mf=0.0,
                                              phycocyanin_mf=0.007,
                                              phycoerythrin_mf=0.0,
                                              allophycocyanin_mf=0.0,
                                              min_wl=wl_min, max_wl=wl_max
                                              )
    elif species == 'algae3':
        cell = fully_pigmented_cell_generator(size=15, chlorophylla_mf=0.0194,
                                              chlorophyllb_mf=0.0120,
                                              chlorophylld_mf=0.0015,
                                              chlorophyllf_mf=0.0,
                                              photoprotective_carotenoids_mf=0.0,
                                              photosynthetic_carotenoids_mf=0.0,
                                              phycocyanin_mf=0.007,
                                              phycoerythrin_mf=0.0,
                                              allophycocyanin_mf=0.0,
                                              min_wl=wl_min, max_wl=wl_max
                                              )

    else:
        raise ValueError('Unknown cell pigment concentrations for {}'.format(species))
    return cell
