#include "animal.h"
#include <stdlib.h>

typedef struct Parrot {
    Animal animal;
    char const* ime;
} Parrot;


char const* parrotGreet(void){
  return "Ka Ka Ja sam papiga! Ja sam papiga! Ka Ka";
}
char const* parrotMenu(void){
  return "kukce i crve";
}
char const* parrotName(void* self){
    return ((Parrot*)self)->ime;
}

void* parrotVTable[] = {
    (void*)parrotName,
    (void*)parrotGreet,
    (void*)parrotMenu
};

void construct(Parrot* self, char const* name) {
    self->ime = name;
    self->animal.vptr = parrotVTable;
};

// nepotrebno
void* create(char const* name) {
    Parrot* p = malloc(sizeof(Parrot));
    construct(p, name);
    return p;
};

int size() {
    return sizeof(Parrot);
}