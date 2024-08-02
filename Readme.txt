About project

I devide this project to 2 parts, the thirst about geant4 calculation
The second about python analising

Geant4 part:

    Main.cc - the main file of compilation, in this you can change flux and time for neutrons

    EnergyDistribution.hh - about neutron Energy function. You can change path to data file with distribution,
    data - first row is a number of (rows + 1) for whole file. Other rows consist of a 2 column - fisrt is
    a Energy, second is a prediction. Data should be in dioposone of [0, 1] in a prediction scale. Can be wrong,
    if the minimum more than 0, and maxsimum less than 1. Data between points in file find as a lineral approximation,
    between two near points.

    Constraction.hh - file where you can change a detector size
    CreateLogicalVolume.cc - adition file, where you can change materials of detector

    StepingAction.cc - main file to detect particles, change particle`s name or minimum energy in this file

    generator.hh - file with neutron generator, you can change Energy, custom you distribution, for example 
    you can create a simple peak

Python part:
    main file to make and plot analisis is a Plot.py

    AD_pip directory for adition files