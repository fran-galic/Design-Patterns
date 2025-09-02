// ideja je Testirati memorijsku cijenu dinamičkog polimorfizma:

#include <stdio.h>

class CoolClass{
public:
  virtual void set(int x){x_=x;};
  virtual int get(){return x_;};
private:
  int x_;
};

class PlainOldClass{
public:
  void set(int x){x_=x;};
  int get(){return x_;};
private:
  int x_;
};

int main() {
    int a = 12;
    printf("size of CoolCLass: %ld\n", sizeof(CoolClass));
    printf("size of PlainOldClass; %ld\n", sizeof(PlainOldClass));
    printf("%lu", sizeof(&a));
    return 0;
}

// Objašnjenje:

// PlainOldClass u svojoj memoriji sadrzi samo taj jedan int x_ koji je 4 byte-a,
// funkcije set i get su definirane negdje u memoriji i različiti instance klase se uvijek pozivaju na te iste funkcije, nema dupliciranja funkcija i ne spremaju se u 
// memoriju za svaki objekt

// CoolClass je Cool pa koristi virtualne metode zbog cega se interno stvara dodatna struktura podataka - virtualna tablica, koja čuva pokazivace na 
// konkretnu implementaciju funkcija u zadanom baznom objektu (koji mogu biti iz neke klase koja je nasljedila baznu klasu)
// Kompajler u klasi koja koristi virtualne metode dodaje pokazaic na vritualnu tablicu, i to zauzima ekstra 8 bytova
// 4 + 8 = 12;     sizeof(PlainOldClass) nam daje 16, a preostalih 4 objašnjavamo sa Paddingom koji compiler ubaci od 4 byta kako bi sve varijable bile
// pravopisno poravnate u memoriji



