// ideja je probati uspješno pozvati funkcije iz virtualnih tablica bez navodneja njihovih imena
// pod predpostavkom da se pokazivac na tablicu nalazi na pocetku objekta

#include <cstdint>
#include <stdio.h>
class B{
public:
  virtual int prva()=0;
  virtual int druga(int)=0;
};

class D: public B{
public:
  virtual int prva(){return 42;}
  virtual int druga(int x){return prva()+x;}
};

void call_virtual_functions(class B* pb) {
  // uzima pointer na klasu i pretvara ga u pointer na unisenged integere velcine pointera (8 bytova)
  // efektivno pointer na polje takvih uintptr od kojih bi prvi trebao pokazivati na vtable od tog objekta
  uintptr_t* o_ptr = reinterpret_cast<uintptr_t*>(pb);
  uintptr_t* v_table = reinterpret_cast<uintptr_t*>(o_ptr[0]);
  // cini se da je kod mene vtbale implementiran da su funckije na prvom mjestu, iako sam
  // ocekivao da budu tek na tipa [2] i [3] ili nesot takoT
  int (* get_42)(B*) = reinterpret_cast<int (*)(B*)>(v_table[0]);
  int (* get_42_plus_x)(B*, int) = reinterpret_cast<int (*)(B*, int)>(v_table[1]);

  printf("Pozivamo 1. metodu obejkta:\n");
  printf("Očekivani ispis : 42\n");
  printf("ispis: %d\n\n", get_42(pb));

  printf("Pozivamo 2. metodu obejkta:\n");
  printf("Unesite int x: ");
  int y;
  scanf("%d", &y);
  printf("Očekivani ispis : 42 + %d = %d\n", y, 42 + y);
  printf("ispis: %d\n", get_42_plus_x(pb, y));
}


int main() {

    D probnaKlasa;
    call_virtual_functions(&probnaKlasa);
    return 0;
}