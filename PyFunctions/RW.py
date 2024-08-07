#libraries
import numpy as np
##########

#function to print
#print Hist in file (name = str)
def MyWrite(Hist, str):
    N = len(Hist[0])
    with open(str, "w") as file:
        for i in range(0, N - 1):
            file.write(np.str_(Hist[0][i])) #Energy
            file.write("\t")
            file.write(np.str_(Hist[1][i])) #Amount
            file.write("\n")
###################


#function to read
def MyRead(str):
    Hist = [[], []]
    f = open(str, 'r')
    for line in f:
        Energy, Amount = line.split('\t')
        Energy = float(Energy)
        Amount = float(Amount)
        Hist[0].append(Energy)
        Hist[1].append(Amount)
    f.close()
    return Hist
##################