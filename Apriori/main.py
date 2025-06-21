from itertools import combinations

def apriori(transakcje, prog_czestosci):

    # znajduje unikalne elementy
    wszystkie_elementy = set()
    for t in transakcje:
        wszystkie_elementy.update(t)

    # znajduje jednoelementowe zbiory czeste
    F1 = {}
    for element in wszystkie_elementy:
        czestosc = sum(1 for t in transakcje if element in t)
        if czestosc >= prog_czestosci:
            F1[frozenset([element])] = czestosc

    # wszystkie zbiory czeste
    wynik = {1: F1}
    k = 1

    # petla while do momentu kiedy zawiera zbiory czyste
    while len(wynik[k]) > 0:
        k += 1
        Ck = {}

        # generowanie z poprzedniego
        for a in wynik[k - 1]:
            for b in wynik[k - 1]:
                if a != b:
                    # polacz i sprawdz czy maja odpowiewdnia dlugosc
                    nowy_zbior = a.union(b)
                    if len(nowy_zbior) == k:
                        # wszystkie podzbiory musza byc czeste
                        wszystkie_podzbiory_czeste = True
                        for podzbior in combinations(nowy_zbior, k - 1):
                            if frozenset(podzbior) not in wynik[k - 1]:
                                wszystkie_podzbiory_czeste = False
                                break

                        if wszystkie_podzbiory_czeste:
                            Ck[nowy_zbior] = 0

        # sprawdza czestosc
        for t in transakcje:
            t_set = set(t)
            for kandydat in Ck:
                if kandydat.issubset(t_set):
                    Ck[kandydat] += 1

        # filtrowanie
        wynik[k] = {zbior: czest for zbior, czest in Ck.items() if czest >= prog_czestosci}

        # gdy nie ma lub jest jeden
        if len(wynik[k]) <= 1:
            break

    return wynik


def generuj_reguly(zbiory_czeste, transakcje, min_jakosc):

    reguly = []
    liczba_trans = len(transakcje)

    # wszytkie zbiory w jedeno
    wszystkie_zbiory = {}
    for k, zbiory in zbiory_czeste.items():
        wszystkie_zbiory.update(zbiory)

    # dla zbiorow czestych o dlugosci co najmniej 2
    for k in zbiory_czeste:
        if k < 2:
            continue

        for zbior, czest in zbiory_czeste[k].items():
            # wsparcie
            wsparcie = czest / liczba_trans

            # generowanie poprzednich podzbiorow
            for i in range(1, k):
                for poprzednik in combinations(zbior, i):
                    poprzednik_set = frozenset(poprzednik)
                    nastepnik = zbior - poprzednik_set

                    # reguly z 1 elementowym nastepnikiem
                    if len(nastepnik) == 1:
                        # ufnosc
                        poprzednik_czest = wszystkie_zbiory[poprzednik_set]
                        ufnosc = czest / poprzednik_czest

                        # jakosc
                        jakosc = wsparcie * ufnosc

                        # sprawdzanie czy spelnia prog jakosci
                        if jakosc >= min_jakosc:
                            reguly.append((poprzednik_set, nastepnik, wsparcie, ufnosc, jakosc))

    return reguly


def drukuj_wyniki(zbiory_czeste, reguly):

    # wyswietla zbiory czeste
    print("ZBIORY CZĘSTE:")
    for k in sorted(zbiory_czeste.keys()):
        print(f"\n{k}-elementowe zbiory częste:")
        for zbior, czest in zbiory_czeste[k].items():
            print(f"  {set(zbior)}: {czest}")

    # wyswietla reguly
    print("\nREGUŁY ASOCJACYJNE:")
    for poprz, nast, wsp, ufn, jakosc in reguly:
        print(f"  {set(poprz)} => {set(nast)} | wsparcie: {wsp:.2f}, ufność: {ufn:.2f}, jakość: {jakosc:.2f}")


def main():
    # transakcje z pdf
    transakcje = [
        {"kapusta", "ogórki", "pomidory", "kabaczki"},
        {"ogórki", "pomidory", "kabaczki"},
        {"cytryny", "pomidory", "woda"},
        {"cytryny", "woda", "jajka"},
        {"ogórki", "grzybki", "żołądkowa"},
        {"żołądkowa", "ogórki", "pomidory"},
    ]

    # prog czestosci
    prog_czestosci = 2

    # uruchom algorytm
    zbiory_czeste = apriori(transakcje, prog_czestosci)

    print(f"Algorytm Apriori dla progu częstości {prog_czestosci}")

    # generowanie regul dla roznych progow jakosci
    for prog_jakosci in [1 / 10, 2 / 10, 3 / 10, 4 / 10]:
        print(f"\n\nWYNIKI {prog_jakosci}")
        reguly = generuj_reguly(zbiory_czeste, transakcje, prog_jakosci)
        drukuj_wyniki(zbiory_czeste, reguly)

if __name__ == "__main__":
    main()