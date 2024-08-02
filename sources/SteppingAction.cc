#include "SteppingAction.hh"

#include "G4Step.hh"
#include "G4Track.hh"
#include "G4RunManager.hh"
#include "G4UnitsTable.hh"

#include "Run.hh"
#include "Parameters.hh"
#include "G4ParticleTable.hh"


MySteppingAction::MySteppingAction(MyDetectorConstruction* detConstruction)  : fDetConstruction(detConstruction){
}

// Collect energy and track length step by step
void MySteppingAction::UserSteppingAction(const G4Step* step){
    G4String name = step->GetTrack()->GetDefinition()->GetParticleName();
    
    //update Time (in runData it makes only once time)
    //as a neutron makes a first step in detector, it`s a null of time for protons 
    if((name == "neutron")){ //||(name == "gamma")){
        const G4VPhysicalVolume* volume = step->GetPreStepPoint()->GetTouchableHandle()->GetVolume();
        const G4VPhysicalVolume* fDetVolume = fDetConstruction->GetDetector();
    
        //check detector volume
        if(volume != fDetVolume){
            return;
        }

        G4double time = step->GetPreStepPoint()->GetGlobalTime();
        MyRun* runData = static_cast<MyRun*> (G4RunManager::GetRunManager()->GetNonConstCurrentRun());
        runData->UpdateLocalTime(name, time);
    }

    //collect information
    else if((name == "proton")){ //||(name == "e-")){
        
        // get volume of the current step
        const G4VPhysicalVolume* volume = step->GetPreStepPoint()->GetTouchableHandle()->GetVolume();
        const G4VPhysicalVolume* fDetVolume = fDetConstruction->GetDetector();
    
        //check detector volume
        if (volume != fDetVolume){
            return;
        }

        //parameters
        G4double bornTime = step->GetPreStepPoint()->GetGlobalTime();
        G4double energy = step->GetPreStepPoint()->GetKineticEnergy();
        
        
        if(energy <= 0.001){
            return;
        }
        MyRun* runData = static_cast<MyRun*> (G4RunManager::GetRunManager()->GetNonConstCurrentRun());
        //there is a error, when neutron dosn`t interect with main detector
        //for example with aluminium box
        //and after it creates a protons in main detector
        //we can`t calculate time and get a error
        if(runData->AddSecondary(energy, bornTime, name) == -1){
            
            //std::cout << step->GetTrack()->GetParentID() << '\n';

        }
        
        //kill
        step->GetTrack()->SetTrackStatus(fStopAndKill);
    }
}
