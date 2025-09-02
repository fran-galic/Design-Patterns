#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <math.h>

typedef struct Unary_Function Unary_Function;
typedef struct vTable vTable;

typedef double (*virtual_function)(Unary_Function*, double);

struct vTable {
    virtual_function value_at;
    virtual_function negative_value_at;
};

struct Unary_Function {
    //pokazivac na vritualnu klasu
    vTable* vt;
    // podatkovni clanovi objekta
    int lower_bound;
    int upper_bound;
};

//osnovne funkcije bazne klase:
void tabulate(Unary_Function* self) {
    for(int x = self->lower_bound; x <= self->upper_bound; x++) {
        printf("f(%d)=%lf\n", x, self->vt->value_at(self, x));
    }
}

int same_functions_for_ints(Unary_Function* f1, Unary_Function* f2, double tolerance) {
    if(f1->lower_bound != f2->lower_bound) return 0;
    if(f1->upper_bound != f2->upper_bound) return 0;
    
    for(int x = f1->lower_bound; x <= f1->upper_bound; x++) {
        double delta = f1->vt->value_at(f1, x) - f2->vt->value_at(f2, x);
        if(fabs(delta) > tolerance) return 0;
    }
    return 1;
}


double base_negative_value_at(Unary_Function* self, double x){
    if (self->vt->value_at == NULL) {
        printf("value_at nije implementiran!\n");
        exit(1);
    }
    return - (self->vt->value_at(self, x));
};

// konkretne implementacije:
vTable base_vtable = {
    .value_at = NULL,
    .negative_value_at = base_negative_value_at
};

// ovo se moze i opcenito koristiti za postavaljanje vrijednosti za Unary_Function
void construct_Unary_Function(struct Unary_Function* self, int lower_bound, int upper_bound) {
    self->vt = &base_vtable;
    self->lower_bound = lower_bound;
    self->upper_bound = upper_bound;
} 

// konstruktor za Unary_Function
struct Unary_Function* create_Unary_Function(int lower_bound, int upper_bound) {
    struct Unary_Function* uf  = malloc(sizeof(struct Unary_Function));;
    construct_Unary_Function(uf, lower_bound, upper_bound);
    return uf;
};

// definiranje stvari za Square

struct Square {
    Unary_Function base_class;
};

double square_value_at(Unary_Function* self, double x){
    return x * x;
};

vTable square_vtable = {
    .value_at = square_value_at,
    .negative_value_at = base_negative_value_at
};

// konstruktor za Square
void construct_Square(struct Square* self, int lower_bound, int upper_bound) {
    construct_Unary_Function((struct Unary_Function*)self, lower_bound, upper_bound);
    self->base_class.vt = &square_vtable;
};

struct Square* create_Square(int lower_bound, int upper_bound) {
    struct Square* sq  = malloc(sizeof(struct Square));
    construct_Square(sq, lower_bound, upper_bound);
    return sq;
};


// stvari za Linear:

struct Linear{
    Unary_Function base_class;
    double a;
    double b;
};

double linear_value_at(struct Unary_Function* self, double x){
    struct Linear* lin = (struct Linear*)self;
    return lin->a * x + lin->b;
};

vTable linear_vtable = {
    .value_at = linear_value_at,
    .negative_value_at = base_negative_value_at
};

// konstruktor za Linear
void construct_Linear(struct Linear* self, int lower_bound, int upper_bound, double a_coef, double b_coef) {
    construct_Unary_Function((struct Unary_Function*)self, lower_bound, upper_bound);
    self->base_class.vt = &linear_vtable;
    self->a = a_coef;
    self->b = b_coef;
};

struct Linear* create_Linear(int lower_bound, int upper_bound, double a_coef, double b_coef) {
    struct Linear* sq  = malloc(sizeof(struct Linear));
    construct_Linear(sq, lower_bound, upper_bound, a_coef, b_coef);
    return sq;
};


// main:

int main() {
    struct Square* f1 = create_Square(-2, 2);
    tabulate((Unary_Function*)f1);
  
    struct Linear* f2 = create_Linear(-2, 2, 5, -2);
    tabulate((Unary_Function*)f2);
  
    printf("f1==f2: %s\n", same_functions_for_ints((Unary_Function*)f1,(Unary_Function*) f2, 1E-6) ? "DA" : "NE");
    printf("neg_val f2(1) = %lf\n", f2->base_class.vt->negative_value_at((Unary_Function*)f2, 1.0));

    printf("size of square: %ld\n", sizeof(*f1));
    printf("size of linear: %ld\n", sizeof(*f2));
    free(f1);
    free(f2);
    return 0;
}

// Napomena: Mislim da zadatak radi kako bi trebao jedini razlog zasto a linear daje 32 a ne 16 zato sot u mom slucjau nema optimizacije