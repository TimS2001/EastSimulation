#ifndef GENERATOR_HH
#define GENERATOR_HH

#include "G4VUserPrimaryGeneratorAction.hh"
#include "EnergyDistribution.hh"


#include "G4ParticleGun.hh"
#include "G4SystemOfUnits.hh"
#include <cmath>
#include <vector>

#include "construction.hh"

//You can use distribution from your file
const int is_MySpect = 1; // 1 - Uses Energy Distribution; more in headers\EnergyDistribution.hh


//if isn`t a my spectr will be a ideal Gauss distribution
//sigma will find for DT/DD reaction from ion temperature

//ion temperature
const G4double Ti = 20.0; // keV
const int is_DT = 0; // 1 - DT reaction; 0 - DD - reaction

class MyPrimaryGenerator : public G4VUserPrimaryGeneratorAction{
    public:
    MyPrimaryGenerator(MyDetectorConstruction* detConstruction);
    ~MyPrimaryGenerator();

    virtual void GeneratePrimaries(G4Event*);

    // method to access particle gun
    const G4ParticleGun* GetParticleGun() const { return nParticleGun; }

    private:
        
    /////////////////////////////////
    G4ParticleGun* nParticleGun = nullptr;
    G4int step;
    MyDetectorConstruction* fDetConstruction = nullptr;
        
    /////////////////////////////////
    //G4double 
    G4double RandEnergy();
    G4ThreeVector StartPosition();
    G4ThreeVector MomDirection(G4ThreeVector);

    //dist to detector
    const G4double distance = 30. * cm;
    
    //for thermal ions
    /////////////////////////////////
    G4double sigma = sqrt(Ti) / 1000. * MeV;
    G4double Energy_neutron;
    const G4double Energy_DT = (14.1 * MeV);
    
    const G4double Energy_DD = 2.45 *MeV; //(2.45 * MeV);
    const G4double C_DT = 75.1; // sqrt(kEv)
    const G4double C_DD = 35.05;
    MyEnergyDistribution* REnergy = nullptr;
    
};


#endif