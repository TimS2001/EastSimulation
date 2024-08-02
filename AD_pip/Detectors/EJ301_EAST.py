import math

BIN_L = 2 #light
MAX_L = 500  #light
MIN_L = 20 #light

AA = 1.5

BB = 1.06 / 4.54

def LightConv(Energy):
    #k = [0.231, 0.3, 0.49097, 1.88055]
    #Light = k[0] * Energy - k[1] * (1.0 - math.exp(- k[2] * math.pow(Energy, k[3])))
    
    A = AA / 4.54
    B = BB
    Light = A * ((Energy) ** 1.5) - B
    if(Light < 0):
        Light = 0
    return Light * 100

def EnergyConv(Light):
    #power = 0.7009
    #koef = 0.02547
    #Energy = koef * math.pow(Light, power)
    
    A = AA / 4.54
    B = BB
    Tmp = Light / 100 + B
    Tmp /= A
    Energy = Tmp ** (2 / 3) - 350
    if(Energy <= 0):
        return 1 
    return Energy


#doesn't work
def GetResolution(Light):
    
    Energy = EnergyConv(Light)

    B = [14.29, 126, 81]
    Power = [-1.5, -3.0]
    
    Resolution = math.sqrt(B[0] + B[1] * math.pow(Energy, Power[0]) + B[2] * math.pow(Energy, Power[1]))
    #Resolution = 10
    return Resolution / 100 #percent