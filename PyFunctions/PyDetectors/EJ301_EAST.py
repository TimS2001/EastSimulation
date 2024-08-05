'''
File with detector constants and addition function
Light convertion and energy convertion will be differented
Because there are a resolution of detector and multi scattering of neutron
'''

#libraries
import math
##########

#constants
BIN_L = 2 #light
MAX_L = 500  #light
MIN_L = 20 #light
LEN = 4. #cm #Len of detector
##########

#Energy into Light
def LightConv(Energy): #convert Energy[Mev] to Light
    #k = [0.231, 0.3, 0.49097, 1.88055]
    #Light = k[0] * Energy - k[1] * (1.0 - math.exp(- k[2] * math.pow(Energy, k[3])))
    
    A = 0.3304
    B = 0.23348

    Light = A * ((Energy) ** 1.5) - B
    if(Light < 0):
        Light = 0
    return Light * 100
##################

#Light into Energy
def EnergyConv(Light):#[MeV]
    A = 3.0266
    B = 0.2335
    C = 0.3
    Tmp = A * (Light / 100 + B)
    Energy = Tmp ** (2 / 3) - C
    
    if(Energy < 0):
        return 0 
    return Energy
##################

#Resolution in proportion
def GetResolution(Light):
    
    Energy = EnergyConv(Light)#this can be wrong but, I don`t know, how change this step
    if(Energy == 0):
        return 0
    B = [14.29, 126, 81]
    Power = [-1.5, -3.0]
    
    Resolution = math.sqrt(B[0] + B[1] * math.pow(Energy, Power[0]) + B[2] * math.pow(Energy, Power[1])) #percent
    #Resolution = 10
    return Resolution / 100 #proportion
#########################
    
