

class PlainOldClass{
public:
  void set(int x){x_=x;};
  int get(){return x_;};
private:
  int x_;
};

class Base{
public:
  //if in doubt, google "pure virtual"
  virtual void set(int x)=0;
  virtual int get()=0;
};
class CoolClass: public Base{
public:
  virtual void set(int x){x_=x;};
  virtual int get(){return x_;};
private:
  int x_;
};
int main(){
  PlainOldClass poc;
  Base* pb=new CoolClass;
  poc.set(42);
  pb->set(42);
} 
// Napomena:
// Sve komentare i zaključke sam sam pisao.

// Odgovori na pitanja:

// 1. Pronađite dijelove assemblerskog kôda u kojima se odvija alociranje memorije za objekte poc i *pb.
// 2. Objasnite razliku u načinu alociranja tih objekata.

	// sub	rsp, 40             ; Alociraj 40 bajtova na stogu
	// .cfi_offset 3, -24
	// mov	rax, QWORD PTR fs:40 ; Dohvati stack canary
	// mov	QWORD PTR -24[rbp], rax ; Spremi canary na stog
	// xor	eax, eax            ; Postavi RAX na 0

	// ; Alokacija za *pb (CoolClass)
	// mov	edi, 16             ; Velicina alokacije (16 bajtova)
	// call	_Znwm@PLT        ; Poziv operator new
	// mov	rbx, rax            ; Adresa alocirane memorije u RBX
	// mov	rdi, rbx            ; Postavi this pointer za konstruktor
	// call	_ZN9CoolClassC1Ev ; Poziv konstruktora CoolClass
	// mov	QWORD PTR -32[rbp], rbx ; Spremi pb na stog (lokalna varijabla)

    // Razlika je Što se poc direktno sprema na stog, što ga cini brzo dostupnim i nemora ga eksplictino brisati,
    // dok za *pb alociramo memoriju negdje na heapu i onda dobivamo adresu od te zauzete memorije i onda tu adresu
    // cuvamo na sustavskom stogu, takoder moramo se brinuti oko oslobadanja memorije

// 3. Pronađite dio assemblerskog kôda koji je zadužen za poziv konstruktora objekta poc, ako takav poziv postoji.

    // PlainOldClass nema korisnički definirani konstruktor, tako da bi se generirao samo neki defolutni konstruktor
    // kojeg onda kompajler izbacuje van zbog optimizacije

// 4. Pronađite dio assemblerskog kôda koji je zadužen za poziv konstruktora objekta *pb. Razmotrite kako se točno izvršava taj kôd. Što se u njemu događa?

	// mov	edi, 16 // 
	// call	_Znwm@PLT
	// mov	rbx, rax
	// mov	rdi, rbx
	// call	_ZN9CoolClassC1Ev

    // Jednom kada se alocira odgovarajuća memorija, konstruktor se ekplicitino pozove sa all	_ZN9CoolClassC1Ev, i on u sebi poziva i konstruktor bazne klase,
    // i takoder inicijalizira virtualnu tablicu:

        // call   _ZN4BaseC2Ev    ; Poziv konstruktora Base

        // lea    rdx, _ZTV9CoolClass[rip+16] ; Učitaj adresu vtable
        // mov     QWORD PTR [rax], rdx         ; Postavi vptr u objektu

// 5. Promotrite kako je prevoditelj izveo pozive pb->set i poc.set. Objasnite razliku između izvedbi tih dvaju poziva. 
    // Koji od ta dva poziva zahtijeva manje instrukcija? Za koju od te dvije izvedbe bi optimirajući prevoditelj mogao generirati 
    // kôd bez instrukcije CALL odnosno izravno umetnuti implementaciju funkcije (eng. inlining)?

    // - poc.set(42) (direktni poziv):
    //     lea    rax, -36[rbp]    ; Dohvati adresu `poc`
    //     mov    esi, 42          ; Argument x=42
    //     mov    rdi, rax         ; Postavi this pointer
    //     call   _ZN13PlainOldClass3setEi ; Direktan poziv
    // - Broj instrukcija: 4 instrukcije prije call.
    // - Dalo bi se generirati poziv bez call funkcije vec se direktno moze umetnuti u memoriju

    // - pb->set(42) (virtualni poziv):
    //     mov    rax, QWORD PTR -32[rbp] ; Dohvati pb
    //     mov    rax, QWORD PTR [rax]    ; Dohvati vptr iz objekta
    //     mov    rdx, QWORD PTR [rax]    ; Dohvati adresu set() iz vtable
    //     mov    rax, QWORD PTR -32[rbp] ; Ponovno dohvati pb (this)
    //     mov    esi, 42                 ; Argument x=42
    //     mov    rdi, rax                ; Postavi this pointer
    //     call   rdx                     ; Indirektni poziv
    // - Broj instrukcija: 6 instrukcija prije call. + treba imati na umu da se potrosi puno vise instrukcija samo dok se stvori objekt koji koristi dinamicki polimorfizam   

// 6. Pronađite asemblerski kôd za definiciju i inicijalizaciju tablice virtualnih funkcija razreda CoolClass.
    // - unutar konstruktora se desava: 
        // sub    rsp, 16            // Alociraj 16 bajtova za lokalne varijable/poravnanje

        // // 1. Inicijalizacija bazne klase
        // mov    QWORD PTR -8[rbp], rdi  // Spremi "this" pointer na stog (-8[rbp])
        // mov    rax, QWORD PTR -8[rbp]  // Dohvati "this" pointer iz stoga
        // mov    rdi, rax                // Postavi "this" u RDI (prvi argument za bazni konstruktor)
        // call   _ZN4BaseC2Ev            // Pozovi konstruktor bazne klase Base

        // // 2. Postavljanje virtualne tablice (vtable)
        // lea    rdx, _ZTV9CoolClass[rip+16]  // Učitaj adresu vtable (preskoči prva dva člana)
        // mov    rax, QWORD PTR -8[rbp]       // Dohvati "this" pointer
        // mov    QWORD PTR [rax], rdx         // Postavi vptr na početak objekta

        // prva dva clana bi bila:
        //     _ZTV9CoolClass:
        // .quad   0                 ; Offset 0: "offset to top" (za višestruko nasljeđivanje)
        // .quad   _ZTI9CoolClass    ; Offset 8: RTTI informacije
        // .quad   _ZN9CoolClass3setEi ; Offset 16: Adresa set()
        // .quad   _ZN9CoolClass3getEv ; Offset 24: Adresa get()