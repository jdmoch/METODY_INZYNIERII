# Wczytywanie pliku
def wczytaj_dane(dane_plik):

    plik = open(dane_plik, 'r', encoding='utf-8')
    linie = plik.readlines()
    plik.close()

# Listy na dane
    obiekty = []
    wartosci = []

# Przetwarzanie każdej linii
    for linia in linie:
        elementy = linia.strip().split()
        obiekty.append(elementy[0])
        wartosci.append(elementy[1:])

# Nazwy atrybutów
    nazwy_atrybutow = []
    for i in range(len(wartosci[0]) - 1):
        nazwy_atrybutow.append(f"a{i + 1}")

# Struktura danych
    system = {
        "obiekty": obiekty,
        "atrybuty": nazwy_atrybutow,
        "dane": {}
    }

# Dane
    for i in range(len(obiekty)):
        id_obiektu = obiekty[i]
        system["dane"][id_obiektu] = {}

        for j in range(len(nazwy_atrybutow)):
            nazwa_atrybutu = nazwy_atrybutow[j]
            system["dane"][id_obiektu][nazwa_atrybutu] = wartosci[i][j]

        system["dane"][id_obiektu]["d"] = wartosci[i][-1]

    return system

# Funkcja generująca wszystkie kombinacje
def kombinacje(lista, k):

    if k == 0:
        return [[]]

    if not lista:
        return []

    wynik = []

# Dla każdego elementu z listy
    for i in range(len(lista)):
        element = lista[i]

        reszta = lista[i + 1:]

        for kombinacja in kombinacje(reszta, k - 1):
            wynik.append([element] + kombinacja)

    return wynik


# Funkcja sprawdzająca czy reguła jest niesprzeczna
def czy_regula_niesprzeczna(regula, system):

    decyzje = set()
    pokryte_obiekty = []

# Sprawdzenie każdego obiektu
    for id_obiektu in system["obiekty"]:
        dane_obiektu = system["dane"][id_obiektu]

# Sprawdzenie czy obiekt spełnia wszystkie warunki
        czy_pasuje = True

        for atrybut, wartosc in regula:
            if dane_obiektu[atrybut] != wartosc:
                czy_pasuje = False
                break

 # Obiekt spełnia warunki
        if czy_pasuje:
            decyzje.add(dane_obiektu["d"])
            pokryte_obiekty.append(id_obiektu)

# Jeżeli wszystkei obiekty mają ta samą decyzje to jest niesprzeczna
    czy_niesprzeczna = len(decyzje) == 1

# Jeśli reguła jest niesprzeczna zwracamy decyzję
    if czy_niesprzeczna:
        decyzja = list(decyzje)[0]
    else:
        decyzja = None

# Liczba obiektów pokrytych przez regułę
    liczba_pokrytych = len(pokryte_obiekty)

    return czy_niesprzeczna, decyzja, liczba_pokrytych, pokryte_obiekty


# Funkcja znajdująca niesprzeczną regułe o konkretnym rzedzie
def znajdz_regule(id_obiektu, system, rzad):

    atrybuty = system["atrybuty"]
    dane_obiektu = system["dane"][id_obiektu]
    kombinacje_atrybutow = kombinacje(atrybuty, rzad)

# Dla każdej kombinacji atrybutów
    for kombinacja in kombinacje_atrybutow:
        regula = []
        for atrybut in kombinacja:
            regula.append((atrybut, dane_obiektu[atrybut]))

# Sprawdzenie
        czy_niesprzeczna, decyzja, liczba_pokrytych, pokryte_obiekty = czy_regula_niesprzeczna(regula, system)

# Jeśli reguła jest niesprzeczna, zwracamy ją
        if czy_niesprzeczna:
            return regula, decyzja, liczba_pokrytych, pokryte_obiekty

    return None, None, 0, []


# Funkcja formatująca regułe
def formatuj_regule(regula, decyzja, liczba_pokrytych):

    warunki = []
    for atrybut, wartosc in regula:
        warunki.append(f"({atrybut} = {wartosc})")

    tekst_reguly = " ∧ ".join(warunki)

    return f"{tekst_reguly} ==> (d = {decyzja})[{liczba_pokrytych}]"


# Główna funkcja algorytmu pokrywającego obiekty
def algorytm_pokrywajacy(system):

    reguly = []
    obiekty_do_rozpatrzenia = system["obiekty"].copy()
    maksymalny_rzad = len(system["atrybuty"])

# Dla każdego rzędu od 1 do maksymalnego
    for rzad in range(1, maksymalny_rzad + 1):
        print(f"Rząd {rzad}:")

# Obiekty przetworzone w rzędzie
        przetworzone_obiekty = []

# Dla każdego obiektu do rozpatrzenia
        for id_obiektu in obiekty_do_rozpatrzenia[:]:

# Jeśli został przetworzony, to pomijamy
            if id_obiektu in przetworzone_obiekty:
                continue

# Szukamy niesprzecznej reguły dla obiektu
            regula, decyzja, liczba_pokrytych, pokryte_obiekty = znajdz_regule(id_obiektu, system, rzad)

# Jeśli znaleziono regułę
            if regula:
                reguly.append((regula, decyzja, liczba_pokrytych))

                print(f"Z obiektu {id_obiektu}:", formatuj_regule(regula, decyzja, liczba_pokrytych))
                print(f"Wyrzucamy z rozważań obiekty: {pokryte_obiekty}")

                for obj in pokryte_obiekty:
                    if obj not in przetworzone_obiekty:
                        przetworzone_obiekty.append(obj)
            else:
                print(f"Z obiektu {id_obiektu}: brak spójnej reguły rzędu {rzad}")

# Usuwamy przetworzone
        nowe_obiekty_do_rozpatrzenia = []
        for obj in obiekty_do_rozpatrzenia:
            if obj not in przetworzone_obiekty:
                nowe_obiekty_do_rozpatrzenia.append(obj)

        obiekty_do_rozpatrzenia = nowe_obiekty_do_rozpatrzenia

        print(f"Pozostałe obiekty do rozważania po rzędzie {rzad}: {obiekty_do_rozpatrzenia}")
        print("-" * 50)

        if not obiekty_do_rozpatrzenia:
            break

    print("Końcowy zestaw reguł:")
    for regula, decyzja, liczba_pokrytych in reguly:
        print(formatuj_regule(regula, decyzja, liczba_pokrytych))

    return reguly

# Funkcja wyświetlająca system decyzyjny
def wyswietl_system(system):
    print("Obiekt".ljust(8), end="")

    for atrybut in system["atrybuty"]:
        print(f"{atrybut}".ljust(12), end="")

    print("d".ljust(12))

    for id_obiektu in system["obiekty"]:
        print(f"{id_obiektu}".ljust(8), end="")

        for atrybut in system["atrybuty"]:
            wartosc = system["dane"][id_obiektu][atrybut]
            print(f"{wartosc}".ljust(12), end="")

        print(f"{system['dane'][id_obiektu]['d']}".ljust(12))

try:

    dane_plik = "dane/SystemDecyzyjny.txt"
    system = wczytaj_dane(dane_plik)

    print("Wczytany plik")
    wyswietl_system(system)
    print("-" * 50)

    reguly = algorytm_pokrywajacy(system)

except:
    print(f"Wystąpił błąd")
    
