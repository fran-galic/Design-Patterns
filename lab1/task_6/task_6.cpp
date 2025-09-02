    #include <stdio.h>
    #include <stdlib.h>

    class Base{
    public:
    Base() {
        metoda();
    }

    virtual void virtualnaMetoda() {
        printf("ja sam bazna implementacija!\n");
    }

    void metoda() {
        printf("Metoda kaze: ");
        virtualnaMetoda();
    }
    };

    class Derived: public Base{
    public:
    Derived(): Base() {
        metoda();
    }
    virtual void virtualnaMetoda() {
        printf("ja sam izvedena implementacija!\n");
    }
    };

    int main(){
    Derived* pd=new Derived();
    pd->metoda();
    free(pd);
    }

// Napomena:
// Sve komentare i zaključke sam sam pisao.

// Komentar:

/* 
Kad se pozove konstruktor Derived klase, prvo se rezervira memorija za objekt, a zatim se poziva konstruktor bazne klase Base(). 
U Base() konstruktoru inicijalizira se dio objekta koji pripada klasi Base i postavlja se pokazivač na virtualnu tablicu (vtable) na onu koja odgovara baznoj klasi. 
Unutar tog konstruktora se poziva metoda() koja, budući da se koristi vtable bazne klase, izvršava virtualnu metodu iz Base implementacije i ispisuje "ja sam bazna implementacija!".

Nakon toga, u tijelu Derived konstruktora, virtualna tablica se ažurira tako da pokazuje na implementacije izvedene klase Derived. 
Kad se unutar Derived konstruktora ponovno pozove metoda(), sada se koristi virtualna metoda definirana u Derived klasi, te se ispisuje "ja sam izvedena implementacija!".

Na kraju, kada se jednom objekt potpuno stvori, svaki daljnji poziv metoda() nad objektom koristi odgovarajuću implementaciju virtualne metode, 
odnosno onu iz Derived klase, pa se ispisuje "ja sam izvedena implementacija!" kao treća poruka.
*/


/*
Ovaj komentar objašnjava dijelove strojno generiranog koda i kako se postavlja te mijenja pokazivač na virtualnu tablicu (vtable)
tijekom konstrukcije objekta, što utječe na ponašanje polimorfnih poziva.

1. Konstruktor bazne klase (Base::Base):
_ZN4BaseC2Ev:
  push    rbp                     // Spremi stari frame pointer
  mov     rbp, rsp                // Postavi novi frame pointer
  sub     rsp, 16                 // Rezerviraj prostor na stogu
  mov     QWORD PTR -8[rbp], rdi  // Spremi 'this' pointer (adresu objekta) u lokalnu varijablu
  lea     rdx, _ZTV4Base[rip+16]  // Učitaj adresu Base vtable-a (ovdje se dobiva pokazivač na tablicu virtualnih funkcija za Base)
  mov     rax, QWORD PTR -8[rbp]  // Učitaj 'this' pointer u registar rax
  mov     QWORD PTR [rax], rdx    // Postavi vtable pointer u objektu na Base vtable
  mov     rdi, rax                // Pripremi 'this' pointer za poziv funkcije
  call    _ZN4Base6metodaEv      // Pozovi Base::metoda(), koja koristi vtable iz Base (dakle, Base::virtualnaMetoda)

2. Funkcija Base::metoda():
_ZN4Base6metodaEv:
  mov     QWORD PTR -8[rbp], rdi  // Spremi 'this' pointer
  lea     rax, .LC1[rip]          // Učitaj adresu stringa "Metoda kaze: "
  mov     rdi, rax               
  mov     eax, 0
  call    printf@PLT            // Ispiši "Metoda kaze: "
  mov     rax, QWORD PTR -8[rbp]  // Učitaj 'this'
  mov     rax, QWORD PTR [rax]    // Dohvati vtable pointer iz objekta (koji je još uvijek Base vtable)
  mov     rdx, QWORD PTR [rax]    // Iz vtable-a učitaj adresu prve virtualne metode (Base::virtualnaMetoda)
  mov     rdi, QWORD PTR -8[rbp]  // Proslijedi 'this' pointer
  call    rdx                   // Pozovi virtualnu metodu – sada se poziva Base implementacija

3. Konstruktor izvedene klase (Derived::Derived):
_ZN7DerivedC2Ev:
  push    rbp                     // Spremi stari frame pointer
  mov     rbp, rsp                // Postavi novi frame pointer
  sub     rsp, 16                 // Rezerviraj prostor na stogu
  mov     QWORD PTR -8[rbp], rdi  // Spremi 'this' pointer (adresu objekta Derived)
  mov     rdi, rax                // Priprema 'this' za poziv baznog konstruktora
  call    _ZN4BaseC2Ev          // Pozovi Base::Base() – inicijalizira Base dio objekta
  lea     rdx, _ZTV7Derived[rip+16] // Učitaj adresu Derived vtable-a
  mov     rax, QWORD PTR -8[rbp]  // Učitaj 'this' pointer
  mov     QWORD PTR [rax], rdx    // Ažuriraj vtable pointer objekta na Derived vtable
  mov     rdi, rax                // Pripremi 'this' pointer
  call    _ZN4Base6metodaEv      // Pozovi Base::metoda(), ali sada se preko vtable-a poziva Derived::virtualnaMetoda

4. Virtualne tablice (vtable):
Base vtable (_ZTV4Base):
  .quad  0                             // Rezervirano (često za RTTI ili offset)
  .quad  _ZTI4Base                    // Informacije o tipu Base
  .quad  _ZN4Base15virtualnaMetodaEv  // Adresa Base::virtualnaMetoda

Derived vtable (_ZTV7Derived):
  .quad  0                             // Rezervirano (često za RTTI ili offset)
  .quad  _ZTI7Derived                  // Informacije o tipu Derived
  .quad  _ZN7Derived15virtualnaMetodaEv// Adresa Derived::virtualnaMetoda

Zaključak:
Tijekom konstrukcije objekta Derived:
- Prvo se poziva Base konstruktor koji postavlja vtable pointer na Base vtable, pa se pozivi virtualnih funkcija (npr. u metoda()) odnose na Base implementaciju.
- Nakon toga, u Derived konstruktoru se vtable pointer ažurira na Derived vtable, pa svi daljnji virtualni pozivi koriste Derived implementaciju.
Ovim se objašnjava kako se polimorfizam mijenja tijekom konstrukcije objekta i kako vtable pointer upravlja tim ponašanjem.
*/
