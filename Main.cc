#include <iostream>

#include "G4MTRunManager.hh"
#include "G4RunManager.hh"
#include "G4UImanager.hh"
#include "G4VisExecutive.hh"
#include "G4UIExecutive.hh"

////////////////////////
#include "Construction.hh"
#include "ActionInitialization.hh"

#include "G4VPhysicalVolume.hh"


////////////////////////
#include "QGSP_BIC_HP.hh" //“QGSP_BIC_HP.hh
////////////////////////
  

//change to 1 and visual will work, 0 - will not
int Vis = 0;

//constants for current simulation
G4double flux = 5.e7 / s;
G4double tau = 0.1 * s;
G4int N = (G4int)(flux * tau); // particle amount

int main(int argc,char** argv){
    //For creating random ivents
    CLHEP::HepRandom::setTheEngine(new CLHEP::RanecuEngine);
    CLHEP::HepRandom::setTheSeed(int(time(NULL)));
    //

    //
    //Construct	the	run	manager	
    #ifdef G4MULTITHREADED
        G4MTRunManager* runManager = new G4MTRunManager;
        runManager->SetNumberOfThreads(G4Threading::G4GetNumberOfCores());
    #else
        G4RunManager* runManager = new G4RunManager;
    #endif

    
    //phys
    /////////////////////////////////////
    G4VModularPhysicsList* physicsList = new QGSP_BIC_HP;
    runManager->SetUserInitialization(physicsList);
    /////////////////////////////////////

    //detector
    /////////////////////////////////////
    MyDetectorConstruction* detConstruction = new MyDetectorConstruction();
    runManager->SetUserInitialization(detConstruction);
    /////////////////////////////////////

    //actionInit
    /////////////////////////////////////
    runManager->SetUserInitialization(new ActionInitialization(detConstruction, 1./ flux));
    /////////////////////////////////////

    
    /////////////////////////////////////
    G4UIExecutive* ui = 0;
    if(Vis == 1){
        ui = new G4UIExecutive(argc, argv);
    }

    //visMan
    /////////////////////////////////////
    G4VisManager* visManager = new G4VisExecutive;
    visManager->Initialize();
    /////////////////////////////////////

    
    
    G4UImanager* UImanager = G4UImanager::GetUIpointer();
    
    runManager->Initialize();

    if(ui){
        UImanager->ApplyCommand("/control/execute ../vis.mac");
        ui->SessionStart();
        
    }else{
        UImanager->ApplyCommand("/run/initialize");
        UImanager->ApplyCommand("/run/beamOn " + std::to_string(N));
    }
    //////////////////////////
    delete runManager;
    
    return 0;
}
