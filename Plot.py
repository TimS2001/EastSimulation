from AD_pip.ReaderFromGeant import ReadAndBlur
from AD_pip.Converter import GetDerivative, GetElectronEquivalent, GetCorrection
from AD_pip.Analysis import GetLinearSmoothing, GetAprHist, ErrorSquare, GetMainPeak, Convert_To_Energy, FindOptimalSolution
from AD_pip.Plotting import plotSimpleHist, plotAnalisis

str = 'data/detector_data.txt' # read file   

Hist = ReadAndBlur(str)

#Calibration_vector= [1.0, 0]
#Hist = GetElectronEquivalent(Hist, Calibration_vector) 

Hist = Convert_To_Energy(Hist)
#Hist = GetCorrection(Hist)

DHist = GetDerivative(Hist)
#plotSimpleHist(Hist, DHist, 'simple')
EnergyOfPeak = [2.4, 3.0]
Peak = GetMainPeak(GetLinearSmoothing(DHist, 2), EnergyOfPeak, GetDerivative)
#'''
if(len(Peak[0]) > 1):
    solution = FindOptimalSolution(Peak, ErrorSquare)
    Aprox = GetAprHist(Peak, solution)

    Axes = [[0, 5], [0, 4e4]] #[X_axis, Y_axis]
    plotAnalisis(Hist, DHist, Aprox, solution, 'DD', Axes, modSave = 0)
