#include "EventAction.hh"

#include "G4Event.hh"
#include "G4RunManager.hh"

#include "Run.hh"

//Event means that one neutron has been created and interacted


void MyEventAction::BeginOfEventAction(const G4Event*){
    //reset energy to calc to new neutron
    MyRun* runData = static_cast<MyRun*> (G4RunManager::GetRunManager()->GetNonConstCurrentRun());
    runData->UpdateGlobalTime(fTau);
}


void MyEventAction::EndOfEventAction(const G4Event*){
    //record data in end of neutron`s interection
    MyRun* runData = static_cast<MyRun*> (G4RunManager::GetRunManager()->GetNonConstCurrentRun());
    runData->FillAndReset();
}
