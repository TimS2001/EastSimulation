#ifndef ACTIONINITIALIZATION_HH
#define ACTIONINITIALIZATION_HH

#include "G4VUserActionInitialization.hh"
#include "construction.hh"
#include "RunAction.hh"
#include "Parameters.hh" 



class ActionInitialization : public G4VUserActionInitialization {
    public:
    ActionInitialization(MyDetectorConstruction* Detector_Volume, G4double Data_Array);
    ~ActionInitialization(){
        //clear data
        size_t size = fdata->size();
        for(int i = 0; i < size; i++){
           fdata->at(i)->clear();
        }
        fdata->clear();
    }

    virtual void Build() const;
    virtual void BuildForMaster() const;
private:
    std::vector<std::vector<MyMainData*>*> *fdata = nullptr; // vector for all data
    MyDetectorConstruction* fDetVolume = nullptr;
    G4double fTau = 0.; // period for neutron flux
};




#endif