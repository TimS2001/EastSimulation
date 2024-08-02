#ifndef ENERGYDISTRIBUTION_HH
#define ENERGYDISTRIBUTION_HH

#include "G4SystemOfUnits.hh"
#include "G4UnitsTable.hh"
#include <cmath>
#include <vector>
#include <string>

class MyEnergyDistribution{
    public:
    MyEnergyDistribution();
    ~MyEnergyDistribution();

    G4double GetEnergyRand();


    private:
    int fileSize;
    std::vector<double> Energy;
    std::vector<double> Probability; //[0, 1]
    //file path to Energy distribution
    std::string name = "..\\..\\sys_data\\EnergyDependanceDD_EAST\\Flux1.txt";
};
#endif