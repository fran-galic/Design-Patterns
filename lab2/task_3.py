def mymax(iterable, key):
    max_x=max_key=None

    max_x = iterable[0]
    max_key = key(max_x)
    for x in iterable:
        if key(x) > max_key:
            max_x = x
            max_key = key(x)
    return max_x

# za sada najbolje rjesenje
def mymax2(iterable, key= lambda x: x):
    iterator = iter(iterable)
    max_x = next(iterator)
    max_key = key(max_x)

    for x in iterator:
        new_key = key(x)
        if new_key > max_key:
            max_x = x
            max_key = new_key
    return max_x

# doduse mozda je ovdje ideja da ne koristimo funkciju sorted
def mymax_better(iterable, key=None):
    temp = None
    if key is None:
        try:
            temp = sorted(iterable)
        except TypeError as e:
            print(f"Ne mogu sortirati: {e}")
    else:
        temp = [rez for (_, rez) in sorted((key(x), x) for x in iterable)]
    return temp[-1]


def main():
    strings = [
    "Gle", "malu", "vocku", "poslije", "kise",
    "Puna", "je", "kapi", "pa", "ih", "njise", "jako_duga_rececnia_tj_string_predobro", "zadnja abecedno"]

    print()
    print("sa mymax:")
    max_lentgh_str_0 = mymax_better(strings, key= lambda x: len(x))
    print(max_lentgh_str_0)
    max_last_str_0 = mymax_better(strings, key= lambda x: x)
    print(max_last_str_0)

    print()
    print("Sa mymax_better:")
    max_lentgh_str = mymax_better(strings, key= lambda x: len(x))
    print(max_lentgh_str)
    max_last_str = mymax_better(strings)
    print(max_last_str)

    # dalje:
    maxint = mymax2([1, 3, 5, 7, 4, 6, 9, 2, 0])
    maxchar = mymax2("Suncana strana ulice")
    maxstring = mymax2([
        "Gle", "malu", "vocku", "poslije", "kise",
        "Puna", "je", "kapi", "pa", "ih", "njise"])
    print()
    print("Nakon nadogradnje my_max funkcije:")
    print(maxint)
    print(maxchar)
    print(maxstring)

    # 4. dio:
    D={'burek':8, 'buhtla':5}
    max_entry = mymax2(D, key= lambda k: D.get(k))
    # metodu mozemo koristiti kao slobodnu funkciju zato sto su metode, pa cak i od objekata ravnopravni first order objekti u pyhtonu
    # te ih mi mozemo izdvojiti van i najnormlanije koristiti. !!! samo moramo paziti i znati da je ta metoda i dalje vezana za KONKRENTO
    # nas objekt koji smo stvorili i kada je pozivmao zapravo provjeravamo i operiramo nad njenim objektom 
    print(f"najskuplje pecivo: {max_entry}")

    # zadnji dio:
    osobe = [
        ("Fran", "Galic"),
        ("mama", "Galic"),
        ("tata", "Galic"),
        ("Mlad_Brat", "Galic"),
        ("djevojka", "Uskoro_Galic"),
        ("pas", "Galic"),
        ("zadnja", "Galic")
    ]

    last_leksi = mymax2(osobe)
    print(f"Zadnja osoba leksikografski je: {last_leksi[0]} {last_leksi[1]}")

if __name__ == "__main__":
    main()