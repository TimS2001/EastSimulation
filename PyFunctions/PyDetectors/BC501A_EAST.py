'''
File with detector constants and addition function
Light convertion and energy convertion will be differented
Because there are a resolution of detector and multi scattering of neutron
'''
#libraries
import math
##########

#constants
BIN_L = 5 #light
MAX_L =  1200  #light
MIN_L = 10 #light
LEN = 4. #cm #Len of detector
##########

#Energy into Light
def LightConv(Energy): #convert Energy[Mev] to Light
    k = [3.285, 103.4, 0.03017, 1.00428]
    Light = k[0] * Energy - k[1] * (1.0 - math.exp(- k[2] * math.pow(Energy, k[3])))
    return Light * 1000
##################

#Light into Energy
def EnergyConv(Light):#[MeV]
    power = 0.7
    koef = 0.02547
    C = 0.2
    Energy = koef * (Light ** power) - C
    if(Energy < 0):
        return 0
    return Energy
##################

#Resolution in proportion
def GetResolution(Light):
    Energy = EnergyConv(Light)#this can be wrong, but I don`t know how change this step
    if(Energy == 0):
            return 0
    B = [14.29, 126, 81]
    Power = [-1.5, -3.0]
    
    Resolution = math.sqrt(B[0] + B[1] * math.pow(Energy, Power[0]) + B[2] * math.pow(Energy, Power[1])) #percentage
    return Resolution / 100 #proportion
#########################