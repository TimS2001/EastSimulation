import math
import numpy as np
from scipy.integrate import quad

#constants
from AD_pip.Constants import LIGHT_ID, AMOUNT_ID
from AD_pip.Constants import BIN_L, MAX_L, MIN_L
#functions
from AD_pip.Constants import LightConv, GetResolution


#Gauss Func normalized by sigma
def Gauss(Ex, sigma):
    k = 1. / (sigma * math.sqrt(2*math.pi))
    s = -0.5 / (sigma * sigma)
    def f(x):
        return k * math.exp(s * (x - Ex)*(x - Ex))
    return f

#Func to Blur detector data by influance of resolution
def BlurByResolution(Hist):

    N = len(Hist[LIGHT_ID])

    #make Hist's copy
    HistBlur = np.array([Hist[LIGHT_ID], np.zeros(N)])

    #get i bin in Hist 
    #calc contribution in HistBlur
    for i in range(0, N):
        bin_now = Hist[LIGHT_ID][i]
        amount_now = Hist[AMOUNT_ID][i]


        if(amount_now > 0):
            #Resoution for Energy = bin_now
            Res = GetResolution(bin_now)

            sigma = bin_now * Res / 2.35 #sigma for current Energy
            
            #find contribution's bin
            #99% in 3*sigma
            #number bins for blur by current step
            n = int(3. * sigma / BIN_L)

            if(n > 1):

                #min bin
                if(i - n < 0):
                    min_ = 0
                else:
                    min_ = i - n

                #max bin
                if(i + n > N):
                    max_ = N
                else:
                    max_ = i + n

                veckoef = []

                #blur_vec
                for m in range(min_, max_):
                    #calc sum of 3 points
                    x0 = m * BIN_L
                    x2 = (m + 1) * BIN_L
                    
                    f = quad(Gauss(bin_now, sigma), x0, x2)
                    
                    veckoef.append(f[0])
                
                #normalize vecKoef
                veckoef = np.array(veckoef)
                sum_ = np.sum(veckoef)
                veckoef /= sum_
                
                
                tmp = 0
                for indx in range(min_, max_):
                    HistBlur[AMOUNT_ID][indx] += veckoef[tmp] * amount_now
                    tmp += 1

                
            else:
                HistBlur[AMOUNT_ID][i] += amount_now

    return HistBlur

#Func to Convert Array[read Geant data from .txt file] to Histogram
def ConvertToHist(Particles):
    bin_ = BIN_L
    max_ = MAX_L
    N = int(max_ / bin_)
    
    Light = []
    Amount = []
    
    tmp = 0
        
    for i in range(0, N):

        bin_now = (i + 0.5) * bin_#bin_now
        bin_next = (i + 1.) * bin_#maxs Light of bin_now
        amount = 0

        #add Light in Hist
        #tmp - index for all
        size_all = len(Particles)
        while((size_all - 1 > tmp)and(Particles[tmp] <= bin_next)):
            amount += 1 #add particle in column
            tmp += 1 #go to next particle
        
        #add bin
        Light.append(bin_now)
        Amount.append(amount)
    Light = np.array(Light)
    Amount = np.array(Amount)
    i = 0 
    while(Light[i] < MIN_L):
        Amount[i] = 0
        i += 1

    #Hist = (np.array([Light, Amount]))
    return np.array([Light, Amount])

#Complex Function of Reader
def ReadAndBlur(str):
    #arrays for different partycles
    #Name - amount of borned protons at one neutron
    once = []
    twice = []
    triple = []
    multi = []

    f = open(str, 'r')
    
    interactions = 1 
    LightLocal = 0
    
    PrevNeutronTime = 0.
    NowNeutronTime = 0.
    f.readline()
    for line in f:
        Energy, ProtonBornTime, NeutronBornTime, Type = line.split('\t')
        Light = LightConv(float(Energy)) #/ 1000. # MeV
        ProtonBornTime = float(ProtonBornTime) #ns
        NeutronBornTime = float(NeutronBornTime) #ns
        Type = np.str_(Type) #p/e
        PrevNeutronTime = NowNeutronTime
        NowNeutronTime = NeutronBornTime

        
        #You can change which particle will be in Histogram
        if(PrevNeutronTime == NowNeutronTime):
            interactions += 1
            LightLocal += Light
        else:
            if(interactions == 1):
                once.append(LightLocal)
            elif(interactions == 2):
                twice.append(LightLocal)
            elif(interactions == 3):
                triple.append(LightLocal)
            else:
                multi.append(LightLocal)
            interactions = 1
            LightLocal = Light
    
    f.close()
    
    #time = 0.1
    #print((once + twice) / 1000 / 1000 / time, ' * 10^6 N / sec')
    
    
    #once.sort()
    #twice.sort()
    #triple.sort()
    #multi.sort()

    Particles = []
    for Light in once:
        Particles.append(Light)
    for Light in twice:
        Particles.append(Light)      
    for Light in triple:
        Particles.append(Light)    
    for Light in multi:
        Particles.append(Light)    

    Particles.sort()


    Hist = ConvertToHist(Particles)
    Hist = BlurByResolution(Hist)
    return Hist

