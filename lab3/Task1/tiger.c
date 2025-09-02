#include "animal.h"
#include <stdlib.h>

typedef struct Tiger {
    Animal animal;
    char const* ime;
} Tiger;


char const* tigerGreet(void){
  return "Grrrrrrrrr";
}
char const* tigerMenu(void){
  return "svjeze gazele, njaaam";
}
char const* tigerName(void* self){
    return ((Tiger*)self)->ime;
}

void* tigerVTable[] = {
    (void*)tigerName,
    (void*)tigerGreet,
    (void*)tigerMenu
};

void construct(Tiger* self, char const* name) {
    self->ime = name;
    self->animal.vptr = tigerVTable;
};

// nepotrebno 
void* create(char const* name) {
    Tiger* p = malloc(sizeof(Tiger));
    construct(p, name);
    return p;
};

int size() {
    return sizeof(Tiger);
}