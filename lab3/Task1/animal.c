#include <stdio.h>
#include "animal.h"

typedef struct Animal {
    void** vptr;
    // vtable entries:
    // 0: char const* name(void* this);
    // 1: char const* greet();
    // 2: char const* menu();
} Animal;

void animalPrintGreeting(struct Animal* animal) {
    nameFun name = (nameFun)(animal->vptr[0]);
    simpleFunction greet = (simpleFunction)(animal->vptr[1]);
    printf("%s pozdravlja: %s\n", name((void*)animal), greet());
}

void animalPrintMenu(struct Animal* animal) {
    nameFun name = (nameFun)(animal->vptr[0]);
    simpleFunction menu = (simpleFunction)(animal->vptr[2]);
    printf("%s voli: %s\n", name((void*)animal), menu());
}