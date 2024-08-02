#ifndef EVENTACTION_HH
#define EVENTACTION_HH

#include "G4UserEventAction.hh"
#include "G4SystemOfUnits.hh"
#include "G4UnitsTable.hh"


class MyEventAction : public G4UserEventAction{
public:
  MyEventAction(G4double tau) {
    fTau = tau; //born`s period for neutrons 
  }
  ~MyEventAction() = default;

  void BeginOfEventAction(const G4Event* event) override;
  void EndOfEventAction(const G4Event* event) override;

private:
  G4double fTau = 50. * ns;//default time for neutron flux
};

#endif


