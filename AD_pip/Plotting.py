import matplotlib.pyplot as plt
import numpy as np
import matplotlib

def plotSimpleHist(Hist, DHist, Graph_Name):
    
    fig, ax = plt.subplots(figsize=(5, 5), layout='constrained')
    k = np.max(Hist[1]) / np.max(DHist[1])

    plt.plot(Hist[0], Hist[1], '.', color ='skyblue', label = 'данные')
    plt.plot(DHist[0], DHist[1] * k, color = 'navy', label = 'производная')



    #ax.set_ylim(0, np.max(Hist[1]))
    ax.set_xlim(0, np.max(Hist[0]))

    ax.grid(which='major')
    ax.set_ylabel('Amount', fontsize = 14)
    ax.set_xlabel('Energy', fontsize=14)
    ax.set_title(Graph_Name, fontsize=14)
    matplotlib.rc('font', size=14)
    plt.legend(loc='upper right')

    plt.show()


#levels - where is a peak, limits - sizes of graph
def plotAnalisis(Hist, DHist, AprxHist, vector, Graph_Name, Limits, modSave = 0): 
    X_AXIS_ID = 0
    Y_AXIS_ID = 1

    fig, ax = plt.subplots(figsize=(5, 5), layout='constrained')
   
    k = 0.4 * Limits[Y_AXIS_ID][1] / np.max(AprxHist[1])

    E = "{:.1f}".format(vector[0])
    R = "{:.0f}".format(vector[1] / vector[0] * 100)

    str = 'approximation'+ '\nL = ' + E + '\n' + r'$\sigma$' + '/L = ' + R + '%'

    plt.plot(Hist[0], Hist[1], '.', color ='skyblue', label = 'data')
    plt.plot(DHist[0], DHist[1] * k, color = 'navy', label = 'restored')
    plt.plot(AprxHist[0], AprxHist[1] * k, label = str, color = 'red')
    

    ax.set_ylim(Limits[Y_AXIS_ID][0], Limits[Y_AXIS_ID][1])
    ax.set_xlim(Limits[X_AXIS_ID][0], Limits[X_AXIS_ID][1])

    ax.grid(which='major')
    ax.set_ylabel('Amount', fontsize = 14)
    ax.set_xlabel('Energy', fontsize=14)
    ax.set_title(Graph_Name, fontsize=14)
    matplotlib.rc('font', size=14)
    plt.legend(loc='upper right')

    plt.show()
    if(modSave == 1):
        fig.savefig('Picturtes\\' + Graph_Name + '.png', bbox_inches='tight', pad_inches=0, dpi=600)