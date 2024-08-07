'''
File with constants for project
Also here can be changed the detector
'''

#constants of Energy Graph
#Energy bins
BIN_E = 0.05 #MeV
MAX_E = 5.0 #MeV
MIN_E = 1.0 #MeV
##########################

#just addtion constants for simple work
ENERGY_ID = 0
LIGHT_ID = 0
AMOUNT_ID = 1
#######################################

#you can change detector files here
from PyFunctions.PyDetectors.EJ301_EAST import BIN_L, MAX_L, MIN_L, LEN
from PyFunctions.PyDetectors.EJ301_EAST import LightConv, EnergyConv, GetResolution
###################################

#cross section for carbon
import numpy as np
EfHist = np.genfromtxt('sys_data/Carbon_cross_section.txt', dtype=[('E', '<f8'), ('S', '<f8')])
#########################
