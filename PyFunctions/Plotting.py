'''
This file has a plot function
'''

#libraries
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
##########

#constants
X_AXIS_ID = 0
Y_AXIS_ID = 1
##########

#function to plot Hist and unfolded Hist
def plotSimpleHist(Hist = [[0], [0]], DHist = [[0], [0]], MyAxes = [], Graph_Name = 'Simple', modSave = 0):
    
    fig, ax = plt.subplots(figsize=(5, 5), layout='constrained')
    k = np.max(Hist[1]) / np.max(DHist[1])

    plt.plot(Hist[0], Hist[1], '.', color ='skyblue', label = 'Data')
    plt.plot(DHist[0], DHist[1] * k, color = 'navy', label = 'unfolded_Data')

    
    ax.set_xlim(0, np.max(Hist[0]))
    ax.set_ylim(0, np.max(Hist[1]))
    if(len(MyAxes) == 2):
        ax.set_xlim(MyAxes[X_AXIS_ID][0], MyAxes[X_AXIS_ID][1])
        ax.set_ylim(MyAxes[Y_AXIS_ID][0], MyAxes[Y_AXIS_ID][1])

    ax.grid(which='major')
    ax.set_ylabel('Amount', fontsize = 14)
    ax.set_xlabel('Energy', fontsize=14)
    ax.set_title(Graph_Name, fontsize=14)
    matplotlib.rc('font', size=14)
    plt.legend(loc='upper right')

    plt.show()
    if(modSave == 1):
        fig.savefig('Picturtes\\' + Graph_Name + '.png', bbox_inches='tight', pad_inches=0, dpi=600)
########################################

#function to plot Hist, unfolded Hist and Approximation Hist
def plotAnalisis(Hist = [[0], [0]], DHist = [[0], [0]], AprxHist = [[0], [0]], vecSolution = [0, 0, 0], MyAxes = [], Graph_Name = 'Simple', modSave = 0):

    fig, ax = plt.subplots(figsize=(5, 5), layout='constrained')
    
    k = 0.4 * np.max(Hist[1]) / np.max(AprxHist[1])

    ax.set_xlim(0, np.max(Hist[0]))
    ax.set_ylim(0, np.max(Hist[1]))

    if(len(MyAxes) != 0):
        ax.set_xlim(MyAxes[X_AXIS_ID][0], MyAxes[X_AXIS_ID][1])
        ax.set_ylim(MyAxes[Y_AXIS_ID][0], MyAxes[Y_AXIS_ID][1])
        k = 0.4 * MyAxes[Y_AXIS_ID][1] / np.max(AprxHist[1])

    E = "{:.2f}".format(vecSolution[0])
    R = "{:.0f}".format(vecSolution[1] / vecSolution[0] * 100)

    str = 'aprx_Data'+ '\n<Ex> = ' + E + '\n' + r'$\sigma$' + '/<Ex> = ' + R + '%'

    plt.plot(Hist[0], Hist[1], '.', color ='skyblue', label = 'Data')
    plt.plot(DHist[0], DHist[1] * k, color = 'navy', label = 'unfolded_Data')
    plt.plot(AprxHist[0], AprxHist[1] * k, label = str, color = 'red')
    


    ax.grid(which='major')
    ax.set_ylabel('Amount', fontsize = 14)
    ax.set_xlabel('Energy', fontsize=14)
    ax.set_title(Graph_Name, fontsize=14)
    matplotlib.rc('font', size=14)
    plt.legend(loc='upper right')

    plt.show()
    if(modSave == 1):
        fig.savefig('Picturtes\\' + Graph_Name + '.png', bbox_inches='tight', pad_inches=0, dpi=600)
############################################################