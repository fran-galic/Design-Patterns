// animal.h
#ifndef ANIMAL_H
#define ANIMAL_H

#ifdef __cplusplus
extern "C" {
#endif

typedef const char* (*simpleFunction)();
typedef const char* (*nameFun)(void*);

typedef struct Animal Animal;

void animalPrintGreeting(struct Animal* animal);
void animalPrintMenu(struct Animal* animal);

#ifdef __cplusplus
}
#endif

#endif