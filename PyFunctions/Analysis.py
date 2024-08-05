'''
File with functions for analysis
Here there are a Convertion to Energy function,
also a smoothing function,
and the some functions for make a approximation
'''

#libraries
import numpy as np
import math
from scipy.optimize import minimize
from scipy.integrate import quad as Integrall
##########

#constants
from PyFunctions.Constants import BIN_E, MAX_E, ENERGY_ID, AMOUNT_ID
from PyFunctions.Constants import BIN_L
from PyFunctions.Constants import EnergyConv
##########

#function to Energy Convertion
def Convert_To_Energy(LightHist):
    EnergyHist = [[],[]]
    N = int(MAX_E / BIN_E)
    for i in range(0, N):
        EnergyHist[0].append((i + 0.5) * BIN_E)
        EnergyHist[1].append(0)

    LIndx = 1
    EIndx = 1
    N1 = len(LightHist[0])
    while(EIndx < N - 1)and(LIndx < N1 - 1):
        LeftLight = BIN_L * (LIndx - 0.5)
        RightLight = BIN_L * (LIndx + 0.5)
        
        LeftEnergy = BIN_E * (EIndx - 0.5)
        RightEnergy = BIN_E * (EIndx + 0.5)

        #next Light Bin
        if(EnergyConv(RightLight) <= LeftEnergy):
        #if(RightLight <= LightConv(LeftEnergy)):
            LIndx += 1

        #next Energy Bin
        elif(LeftEnergy > EnergyConv(RightLight)):
            EIndx += 1

        #current Bin
        else:
            RightLightMore = 0
            
            LeftBord = EnergyConv(LeftLight)#default bord - Light bord
            if(EnergyConv(LeftLight) < LeftEnergy):#Energy left bord more than Light
                LeftBord = LeftEnergy         

            RightBord = EnergyConv(RightLight)#default bord - Light bord
            if(EnergyConv(RightLight) > RightEnergy):#Energy left board less than Light
                RightBord = RightEnergy 
                RightLightMore = 1 #we need to go to next bin    
            
            FullBin = (EnergyConv(RightLight) - EnergyConv(LeftLight))
            PartOfEnergy = (RightBord - LeftBord)
            k = 0
            if(FullBin != 0):
                k = PartOfEnergy/FullBin 
            
            EnergyHist[1][EIndx] += k * LightHist[1][LIndx]

            if(RightLightMore):
                EIndx += 1
            else:
                LIndx += 1
          
    return np.array(EnergyHist)
##############################

#Simple smoothing 
def GetLinearSmoothing(Hist, numb = 2):#this calculate avarege value at the 'numb' bins
    filter = np.ones(numb) / numb #vector of smoothing
    half_numb = numb // 2 
    resalt = np.convolve(Hist[AMOUNT_ID], filter, mode='same') #python method
    Hist1 = [(Hist[ENERGY_ID][half_numb:-half_numb]),(resalt[half_numb:-half_numb])]
    return np.array(Hist1)  
#################

#function for aproximation
#Gauss function
def Gauss(Ex, Sigma):
    if(Sigma == 0):
        def f(x):
            return 0
        return f
    k = 1. / (Sigma * math.sqrt(2*math.pi))
    s = -0.5 / (Sigma * Sigma)
    def f(x):
        return k * math.exp(s * (x - Ex)*(x - Ex))
    return f

#return Approximation Histogram
def GetAprHist(Hist, vector):
    N = len(Hist[0])
    Ex, Sigma, High = vector
    
    AprHist = [[], []]

    for m in range(1, N - 1):
        #calculate the integrall of ideal Gauss
        x_left_boundary = 0.5 * (Hist[ENERGY_ID][m - 1] + Hist[ENERGY_ID][m])
        x_right_boundary = 0.5 * (Hist[ENERGY_ID][m + 1] + Hist[ENERGY_ID][m])
        Energy = Hist[ENERGY_ID][m]
        Amount = (Integrall(Gauss(Ex, Sigma), x_left_boundary, x_right_boundary))[0]

        AprHist[ENERGY_ID].append(Energy)
        AprHist[AMOUNT_ID].append(Amount)

    AprHist = np.array(AprHist)
    Origin_Hist_Sum = np.sum(Hist[AMOUNT_ID])
    Apr_Sum = np.sum(AprHist[AMOUNT_ID])
    Normilize_Koef = High * Origin_Hist_Sum / Apr_Sum
    
    AprHist[AMOUNT_ID] *= Normilize_Koef


    return np.array(AprHist)

#LSM - Less Square Method
#return python function at 3 parameters - (e, s, h)
#e - optimal center of GaussPeak, s - optimal sigma, h - optimal high
#f - squarre difference between Aproximation in (e, s ,h) point and origin Histogram
def ErrorSquare(Hist):
    N = len(Hist[ENERGY_ID])
    bin_ = Hist[ENERGY_ID][1] - Hist[ENERGY_ID][0]
    
    def f(vector): # vector - (e, s, h)
        df = 0.
        AprHist = [[], []]

        if(vector[0] <= 0)or(vector[1] <= 0)or(vector[2] <= 0):
            return 1.e10 #(0, 0, 0) - bad solution, error also will be 0

        for m in range(0, N):
            x_left_boundary = Hist[ENERGY_ID][0] + (m - 0.5) * bin_
            x_right_boundary = Hist[ENERGY_ID][0] + (m + 0.5) * bin_
            Energy = m * bin_
            Amount = (Integrall(Gauss(vector[0], vector[1]), x_left_boundary, x_right_boundary))[0]

            AprHist[ENERGY_ID].append(Energy)
            AprHist[AMOUNT_ID].append(Amount)

        AprHist = np.array(AprHist)

        OriginSum = np.sum(Hist[AMOUNT_ID])
        AprSum = np.sum(AprHist[AMOUNT_ID])
        Normalize_koef = (vector[2] * OriginSum / AprSum)
        AprHist[AMOUNT_ID] *= Normalize_koef

        for m in range(0, N):
            df += ((AprHist[AMOUNT_ID][m] - Hist[AMOUNT_ID][m]) ** 2)
        return df
    return f

#Find peaks from Histogram
def findPeaks(Hist, GetDerivative):
    N = len(Hist[ENERGY_ID])
    DHist = GetDerivative(Hist)
    
    M = len(DHist[ENERGY_ID])
    peaks = [[0, 'n']]
    for i in range(1, M - 1):
        if(DHist[AMOUNT_ID][i - 1] < 0)and(DHist[AMOUNT_ID][i + 1] > 0):
            peaks.append([DHist[ENERGY_ID][i], 'r'])#rise
        
        elif(DHist[AMOUNT_ID][i - 1] > 0)and(DHist[AMOUNT_ID][i + 1] < 0):
            peaks.append([DHist[ENERGY_ID][i], 'f'])#fall
    peaks.append([DHist[ENERGY_ID][N - 1],'n'])

    
    tmpHist = [[],[]]
    Peaks = []
    k = 0
    for i in range(0, N):
        while(peaks[k][1] != 'r')and(k < len(peaks) - 1):
            k += 1

        if(Hist[ENERGY_ID][i] > peaks[k][0]):
            Peaks.append(tmpHist)
            tmpHist = [[],[]]
            k += 1
        else:
            tmpHist[ENERGY_ID].append(Hist[ENERGY_ID][i])
            tmpHist[AMOUNT_ID].append(Hist[AMOUNT_ID][i])
    Peaks.append(np.array(tmpHist))


    return Peaks 

#First approximation for Gauss distribution
#just uses momentum formuls
def FindKoefStatistic(Hist):
    N = len(Hist[ENERGY_ID])
    
    Ex0 = np.sum(Hist[AMOUNT_ID])
    if(Ex0 == 0):
        return 0.0, 0.0
    Ex1 = 0
    Ex2 = 0
    
    for i in range(0, N):
        Ex1 += Hist[1][i] * Hist[0][i]
        Ex2 += Hist[1][i] * (Hist[0][i] ** 2)

    #Normilize
    Ex1 /= Ex0
    Ex2 /= Ex0
        
    
    Dx = (Ex2 - Ex1 * Ex1)

    if(Dx <= 0):
        return 0, 0

    S = math.sqrt(N / (N - 1) * Dx) #square
   
    return Ex1, S
#####

#uses SciPy to find solution
def FindOptimalSolution(Hist, Error_function):
    High = 1.
    Ex, Sigma = FindKoefStatistic(Hist)
    vector_first_approach = np.array([Ex, Sigma, High])
    
    solution = minimize(Error_function(Hist), vector_first_approach)
    optimal_Ex = solution.x[0]
    optimal_Sigma = solution.x[1]
    optimal_High = solution.x[2]

    return optimal_Ex, optimal_Sigma, optimal_High

#find the main Peak
def GetMainPeak(Hist, Boundaries, GetDerivative):
    min_ = Boundaries[0]
    max_ = Boundaries[1]

    ################
    Peaks = findPeaks(Hist, GetDerivative)
    NUMBERS_OF_PEAKS_IN_MAIN_PEAK = []
    for i in range(0, len(Peaks)):
        Peak = Peaks[i]
        E1, S1 = FindKoefStatistic(Peak)
        if((min_ < E1 < max_)and(S1 > 0)):
            NUMBERS_OF_PEAKS_IN_MAIN_PEAK.append(i)
    
    MainPeak = [[],[]]
    N = len(NUMBERS_OF_PEAKS_IN_MAIN_PEAK)
    
    if(N > 1):
        Min_Peak = Peaks[NUMBERS_OF_PEAKS_IN_MAIN_PEAK[0]]
        Max_Peak = Peaks[NUMBERS_OF_PEAKS_IN_MAIN_PEAK[N - 1]]
        
        Energy_min = Min_Peak[ENERGY_ID][0]
        Energy_max = Max_Peak[ENERGY_ID][len(Max_Peak[ENERGY_ID]) - 1]
        
        i = 0
        while(Hist[ENERGY_ID][i] < Energy_min):
            i += 1
        while(Hist[ENERGY_ID][i + 1] < Energy_max):
            MainPeak[ENERGY_ID].append(Hist[ENERGY_ID][i])
            amount = Hist[AMOUNT_ID][i]
            if(amount > 0):
                MainPeak[AMOUNT_ID].append(amount)
            else:
                MainPeak[AMOUNT_ID].append(0)
            i += 1
    elif(N == 1):
        MainPeak = Peaks[NUMBERS_OF_PEAKS_IN_MAIN_PEAK[0]]
    
    else:
        print('NO PEAKS')
        return [[0],[0]]
    return np.array(MainPeak)
#########################