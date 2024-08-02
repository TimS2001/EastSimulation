#const
#Energy_bins
BIN_E = 0.05 #MeV
MAX_E = 5.0 #MeV
MIN_E = 1.0 #MeV

ENERGY_ID = 0
LIGHT_ID = 0
AMOUNT_ID = 1
LEN = 4. #cms

from AD_pip.Detectors.EJ301_EAST import BIN_L, MAX_L, MIN_L
from AD_pip.Detectors.EJ301_EAST import LightConv, EnergyConv, GetResolution

KOEF = 0.

#cross section for carbon
import numpy as np
EfHist = np.genfromtxt('sys_data/Carbon_cross_section.txt', dtype=[('E', '<f8'), ('S', '<f8')])
