#include "G4DecayPhysics.hh"
#include "G4RadioactiveDecayPhysics.hh"
#include "G4EmStandardPhysics_option4.hh"
#include "G4EmExtraPhysics.hh"
#include "G4IonPhysics.hh"
#include "G4IonElasticPhysics.hh"
#include "G4StoppingPhysics.hh"
#include "G4HadronElasticPhysicsHP.hh"

#include "Physics.hh"
#include "G4HadronPhysicsQGSP_BIC_HP.hh"

MyPhysics::MyPhysics(G4int ver)
{
  if(ver > 0) {
    G4cout << "<<< Geant4 Physics List simulation engine: QGSP_BIC_HP"<<G4endl;
    G4cout <<G4endl;
  }
  //defaultCutValue = 0.7*CLHEP::mm;  
  SetCutValue(0, "proton");  
  SetVerboseLevel(ver);

  // EM Physics
  RegisterPhysics( new G4EmStandardPhysics_option4(ver) );

  // Decays
  RegisterPhysics( new G4DecayPhysics(ver) );
  RegisterPhysics( new G4RadioactiveDecayPhysics(ver) );

  // Hadron Elastic scattering
  RegisterPhysics( new G4HadronElasticPhysicsHP(ver) );

  // Hadron Physics
  //RegisterPhysics(  new G4HadronPhysicsQGSP_BIC_HP(ver)); //can remove it (less accurance)
}