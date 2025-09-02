from datetime import datetime
import time

class TipkovnickiIzvor:
    def procitaj(self):
        x = input()
        if x.strip() == "-1":
            return -1
        try:
            return int(x)
        except ValueError:
             raise TypeError("Program cita samo cijele brojeve (int)")

class DatotecniIzvor:
    def __init__(self, putanja):
        self.f = open(putanja, "r")

    def procitaj(self):
        linija = self.f.readline()
        if not linija:
            self.f.close()
            return -1
        try:
            return int(linija.strip())
        except ValueError:
             raise TypeError("Program cita samo cijele brojeve (int)")

    def zatvori_izvor(self):
        if not self.f.closed:
            self.f.close()

def spremi_u_datoteku(kolekcija, naziv_datoteke="rezultat.txt"):
    with open(naziv_datoteke, "a") as f:
        vrijeme = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n")
        f.write(f"Zapis: {vrijeme}\n")
        f.write(f"Podaci: {kolekcija}\n")

def zbroji(brojevi):
    rezultat = sum(brojevi)
    print(f"[Zbroj] Zbroj svih brojeva je: {rezultat}")

def najveci(brojevi):
    najveci_broj = max(brojevi)
    print(f"[Najveci] Najveći broj u nizu je: {najveci_broj}")

def najmanji(brojevi):
    najmanji_broj = min(brojevi)
    print(f"[Najmanji] Najmanji broj u nizu je: {najmanji_broj}")

def prosjek(brojevi):
    if not brojevi:
        print("[Prosjek] Nema brojeva za izračun prosjeka.")
        return
    rezultat = sum(brojevi) / len(brojevi)
    print(f"[Prosjek] Prosjek svih brojeva je: {rezultat:.2f}")

def medijan(brojevi):
    if not brojevi:
        print("[Medijan] Nema brojeva za izračun medijana.")
        return
    sortirani = sorted(brojevi)
    n = len(sortirani)
    sredina = n // 2
    if n % 2 == 1:
        print(f"[Medijan] Medijan je: {sortirani[sredina]}")
    else:
        med = (sortirani[sredina - 1] + sortirani[sredina]) / 2
        print(f"[Medijan] Medijan je: {med}")
    
class SlijedBrojeva:
    def __init__(self, get_info_from_izvor):
        self.array = []
        self.akcije = dict()
        self.get_info_from_izvor = get_info_from_izvor

    def set_izvor(self, get_info_from_izvor):
        if hasattr(self.get_info_from_izvor, 'zatvori_izvor'):
            self.get_info_from_izvor.zatvori_izvor()
        self.get_info_from_izvor = get_info_from_izvor
    
    def kreni(self):
        if self.get_info_from_izvor is None:
            raise AttributeError("izvor jos nije inicijaliziran")
        while True:
            start = time.time()
            data = self.get_info_from_izvor.procitaj()
            if data == -1:
                break
            self.array.append(data)
            # tu treba iterirait po rjencniku akciji i obaviit akcije
            for _, akcija in self.akcije.items():
                akcija(self.array)
            kraj = time.time()

            trajanje = kraj - start
            sleep_time = max(0, 1 - trajanje)
            time.sleep(sleep_time)
        if hasattr(self.get_info_from_izvor, 'zatvori_izvor'):
            self.get_info_from_izvor.zatvori_izvor()
        

    def dodaj_akciju(self, ime, akcija):
        self.akcije[ime] = akcija
    
    def dodaj_akcije(self, rjecnik_akcija):
        self.akcije.update(rjecnik_akcija)

    def makni_akciju(self, ime):
        del self.akcije[ime]
    
    def popis_akcija(self):
        print("popis akcija")
        print([(ime, akcija) for ime, akcija in self.akcije.items()])

def main():
    sb = SlijedBrojeva(get_info_from_izvor= TipkovnickiIzvor())
    sb.dodaj_akciju("zbroji", zbroji)
    sb.dodaj_akciju("najveci", najveci)
    sb.popis_akcija()
    sb.kreni()

    sb.set_izvor(get_info_from_izvor= DatotecniIzvor("input.txt"))
    sb.dodaj_akciju("medijan", medijan)
    sb.popis_akcija()
    sb.makni_akciju("najveci")
    sb.dodaj_akciju("spremi_u_datoteku", spremi_u_datoteku)
    sb.popis_akcija()
    sb.kreni()

if __name__ == "__main__":
    main()
    
