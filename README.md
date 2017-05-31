# README #

### What is this repository for? ###

This repository contains all the necessary code and data files to run Bio-SNICAR.

### How do I get set up? ###

The essential scripts are all written for Matlab. This includes the driver software, the radiative transfer code, which are all that are needed to run model experiments using our existing impurity lookup library. However, if new impurities are to be created additional scripts are used. A few of these are currently coded in Python, but will be translated for Matlab. All the necessary data files and scripts are included in this repository. Basic usage guidelines are provided below, but for detailed instructions we direct the user to the instruction manual available in the repo.

The software versions used to write the codes were Matlab R2016b and Python 3.4 using the Anaconda 3.4.3 distribution (Windows 64bit). 


### Contribution guidelines ###

We welcome collaborations and contributions from other developers. We highlight the incorporation of grain shape effects and translation of BioSNICAR into Python as particularly useful development goals.

### Who do I talk to? ###

Please direct queries to Joseph Cook (University of Sheffield) at the following email address: joe.cook@sheffield.ac.uk

### Usage Guidelines ###

To run this model, open 'BioSNICAR_driver_MASTER.m'. This is the driver software where the model parameters are defined and formatted so that they can be read by the radiative transfer code (snicar_8d.m). When the driver is run, the user-defined input values are sent to the radiative transfer model. The spectral albedo is plotted in a new window and a numeric value for the broadband albedo is printed in the command window.

By default, the incoming solar irradiance is for a mid-latitude site with a 60 degree zenith angle. The snow grain size in each vertical layer is defined in an array in line 84. The impurity concentrations in each layer are defined in lines 112 - 125. The model is run simply by pressing F5 or clicking the green 'run' arrow in the toolbar.

### Disclaimer ###

This software is in active development. We provide free and open access to this software on the understanding that the authors assume no responsibility for downstream usage and, while we welcome collaboration, we are not obliged to provide training or support for users. We hope that this code and data will be useful and encourage collaboration, but we provide it without warranty or guarantee, nor the implied warranty of merchantability or fitness for any particular purpose.