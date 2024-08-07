#ifndef PHYSICS_HH
#define PHYSICS_HH 1

#include "globals.hh"
#include "G4VModularPhysicsList.hh"

class MyPhysics : public G4VModularPhysicsList
{
public:
  MyPhysics(G4int ver = 1);
  virtual ~MyPhysics()=default;

  // delete copy constructor and assignment operator
  MyPhysics(const MyPhysics &)=delete;
  MyPhysics & operator=(const MyPhysics &right)=delete;

};

#endif