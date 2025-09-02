import os
from factory import myfactory
 
def printGreeting(pet):
  print(pet.name + " kaze: " + pet.greet())
def printMenu(pet):
  print(pet.name + " jede: " + pet.menu())

def test():
  pets=[]
  for mymodule in os.listdir('plugins'):
    moduleName, moduleExt = os.path.splitext(mymodule)
    if moduleExt=='.py':
      ljubimac=myfactory(moduleName)('Ljubimac '+str(len(pets)))
      pets.append(ljubimac)

  # ispiši ljubimce
  for pet in pets:
    printGreeting(pet)
    printMenu(pet)

test()