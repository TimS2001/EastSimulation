from scipy.io import loadmat
import math
import numpy as np
#time in sec

from AD_pip.Constants import LEN 

#change channel scale to Energy scale in Histogram
def GetElectronEquivalent(MainHist, Calibration):
    Hist = [[], []]
    N = len(MainHist[0])
    for i in range(0, N):

        Energy = Calibration[0] * MainHist[0][i] + Calibration[1]
        Amount = MainHist[1][i]
        
        if(Energy > 0):
            Hist[0].append(Energy)
            Hist[1].append(Amount)
    
    return np.array(Hist)

#Min value to calculate derivative
MIN_ = 0.
#Central derivative
def GetDerivative(Hist):
    N = len(Hist[0])
    DHist = [[0], [0]]
    
    for i in range(1, N - 1):
        k = 0.
        if(Hist[0][i] > MIN_):
            dx = Hist[0][i + 1] - Hist[0][i - 1]
            dy = Hist[1][i + 1] - Hist[1][i - 1]
            
            k = -1. * dy / dx #multiply by -1
        DHist[1].append(k)
        DHist[0].append(Hist[0][i])

    DHist[1].append(0)
    DHist[0].append(Hist[0][N - 1])

    DHist = np.array(DHist)
    #Normalize Amount by maximum of origin Hist
    K1 = np.max(Hist[1])
    K2 = np.max(DHist[1])
    #print(K2)
    DHist[1] *= K1 / K2

    return np.array(DHist)

#Correction by cross_section
def GetCorrection(Hist):
    Cross_section_Carbon = np.genfromtxt('sys_data/Carbon_cross_section.txt', dtype=[('Energy', '<f8'), ('Value', '<f8')])
    
    def Efficient(Energy):#Energy should be in a MeV
        #Carbon
        N = len(Cross_section_Carbon['Energy'])
        i = 1
        while((Cross_section_Carbon['Energy'][i] <= Energy)and(i < N - 1)):
            i += 1
        delta_V = Cross_section_Carbon['Value'][i] - Cross_section_Carbon['Value'][i - 1]
        delta_E = Cross_section_Carbon['Energy'][i] - Cross_section_Carbon['Energy'][i - 1]

        k = delta_V / delta_E
        b = Cross_section_Carbon['Value'][i] - k * Cross_section_Carbon['Energy'][i]
        sig_C = k * Energy + b
        
        #Hydrogen
        sig_H = 0.
        if(Energy <= 3.8):
            sig_H = 53.86 * math.pow(Energy, -0.366)
        elif(Energy <= 4.0):
            sig_H = -0.00986 * math.pow(Energy, 0.631) + 4.9162
        else:
            sig_H = 42.69 * math.pow(Energy, -0.316) - 0.587

        k = sig_H / (sig_H + sig_C) * (1. - math.exp(- (sig_H + sig_C)* LEN))
        return  1./ k 

    Hist1 =[[], []]
    N = len(Hist[0])
    for i in range(0, N):
        Hist1[0].append(Efficient(Hist[0][i] / 1000))
        Hist1[1].append(Hist[1][i])

    return np.array(Hist1)

    
