#include <stdio.h>
#include <stdlib.h>

// metode:
char const* dogGreet(void){
  return "vau!";
}
char const* dogMenu(void){
  return "kuhanu govedinu";
}
char const* catGreet(void){
  return "mijau!";
}
char const* catMenu(void){
  return "konzerviranu tunjevinu";
}

typedef char const* (*behaviour_actions)();
typedef behaviour_actions behaviour_actions_list[];

//virtualne tablice
behaviour_actions_list dogActions= {dogGreet, dogMenu};
behaviour_actions_list catActions = {catGreet, catMenu};

struct Animal {
    // Podatkovni članovi objekta:
    char const* name;
    //virtulane metode:
    behaviour_actions_list* actions;
};

// metode u OOP:
void animalPrintGreeting(struct Animal* animal) {
    printf("%s pozdravlja: %s\n", animal->name, (*(animal->actions))[0]());
}
void animalPrintMenu(struct Animal* animal) {
    printf("%s voli %s\n", animal->name, (*(animal->actions))[1]());
}

// konstruktori u OOP_u:
void constructDog(struct Animal* memory_space, const char* name) {
    memory_space->actions = &dogActions;
    memory_space->name = name;
} 
void constructCat(struct Animal* memory_space, const char* name) {
    memory_space->actions = &catActions;
    memory_space->name = name;
} 
struct Animal* createDog(const char* name) {
    struct Animal* dogo = malloc(sizeof(struct Animal));;
    constructDog(dogo, name);
    return dogo;
}
struct Animal* createCat(const char* name) {
    struct Animal* garf = malloc(sizeof(struct Animal));
    constructCat(garf, name);
    return garf;
}

void testAnimalsHeap(void){
  printf("test animals created on heap: \n");
  struct Animal* p1=createDog("Hamlet");
  struct Animal* p2=createCat("Ofelija");
  struct Animal* p3=createDog("Polonije");

  animalPrintGreeting(p1);
  animalPrintGreeting(p2);
  animalPrintGreeting(p3);

  animalPrintMenu(p1);
  animalPrintMenu(p2);
  animalPrintMenu(p3);

  free(p1); free(p2); free(p3);
}

void testAnimalsStack(void){
  printf("test animals created on stack: \n");
  // 1. nacin - dirketno
  struct Animal p1;
  struct Animal p2;
  struct Animal p3;
  constructDog(&p1, "Marko");
  constructDog(&p2, "Pero");
  constructDog(&p3, "Ivan");

  animalPrintGreeting(&p1);
  animalPrintGreeting(&p2);
  animalPrintGreeting(&p3);

  animalPrintMenu(&p1);
  animalPrintMenu(&p2);
  animalPrintMenu(&p3);
}

struct Animal* stvaranje_n_pasa(int n) {
    struct Animal* dogs = malloc(n * sizeof(struct Animal));
    for (int i = 0; i < n; i++) { 
        constructDog(&dogs[i], "Marko");  
    }
    return dogs;
}

void main() {
    testAnimalsHeap();
    printf("\n");
    testAnimalsStack();

    int n = 20;
    struct Animal* dogs = stvaranje_n_pasa(n);
    printf("\n");
    printf("Pregled stvorenih %d peseka:\n", n);
    for (int i = 0; i < 20; i++) {
        printf("Pas %d. : %s\n", i + 1, dogs[i].name);
    }

    free(dogs);
}




