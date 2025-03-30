import pandas as pd


def wczytaj_plik(nazwa_pliku):
    """Wczytuje plik i zwraca DataFrame"""
    dane = []
    with open(nazwa_pliku, 'r', encoding='utf-8') as f:
        for linia in f:
            wiersz = linia.strip().split()
            dane.append(wiersz)

    kolumny = ['ID', 'Pogoda', 'Temperatura', 'Wilgotnosc', 'Wiatr', 'Decyzja']
    df = pd.DataFrame(dane, columns=kolumny)
    df = df.drop('ID', axis=1)
    return df


def macierz(df):
    """Tworzy macierz nieodróżnialności z różnymi decyzjami"""
    n = len(df)
    macierz_nieodrozn = {}

    for i in range(n):
        for j in range(i + 1, n):
            if df.loc[i, 'Decyzja'] == df.loc[j, 'Decyzja']:
                continue
            wspolne = [kol for kol in df.columns[:-1] if df.loc[i, kol] == df.loc[j, kol]]
            macierz_nieodrozn[(i, j)] = wspolne

    return macierz_nieodrozn


def generuj_reguly(df, macierz_nieodrozn):
    """Generuje reguły decyzyjne na podstawie macierzy nieodróżnialności"""
    reguly = {1: [], 2: [], 3: []}
    uzyte_warunki = set()
    for (i, j), wspolne_atrybuty in macierz_nieodrozn.items():
        for atrybut in wspolne_atrybuty:
            warunek = f'({atrybut} = {df.loc[i, atrybut]})'
            if warunek not in uzyte_warunki:
                pasujace_wiersze = df[df[atrybut] == df.loc[i, atrybut]]
                wsparcie = len(pasujace_wiersze[pasujace_wiersze['Decyzja'] == df.loc[i, 'Decyzja']])
                regula = {
                    'warunek': warunek,
                    'decyzja': df.loc[i, 'Decyzja'],
                    'wsparcie': wsparcie
                }
                reguly[1].append(regula)
                uzyte_warunki.add(warunek)

    def polacz_reguly(poprzednie_reguly):
        """Łączy reguły niższego rzędu w celu utworzenia bardziej złożonych reguł"""
        nowe_reguly = []
        widziane_warunki = set()

        for i in range(len(poprzednie_reguly)):
            for j in range(i + 1, len(poprzednie_reguly)):
                regula1, regula2 = poprzednie_reguly[i], poprzednie_reguly[j]

                warunki_reguly1 = regula1['warunek'].split(' ∧ ')
                warunki_reguly2 = regula2['warunek'].split(' ∧ ')

                if len(set(warunki_reguly1) & set(warunki_reguly2)) > 0:
                    continue

                warunki = set(warunki_reguly1) | set(warunki_reguly2)
                polaczony_warunek = ' ∧ '.join(sorted(warunki))

                if polaczony_warunek in widziane_warunki:
                    continue

                pasujace_wiersze = df.copy()
                for war in warunki:
                    atrybut, wartosc = war.strip('()').split(' = ')
                    pasujace_wiersze = pasujace_wiersze[pasujace_wiersze[atrybut] == wartosc]

                if not pasujace_wiersze.empty and (
                        pasujace_wiersze['Decyzja'] == pasujace_wiersze['Decyzja'].iloc[0]).all():
                    regula = {
                        'warunek': polaczony_warunek,
                        'decyzja': pasujace_wiersze['Decyzja'].iloc[0],
                        'wsparcie': len(pasujace_wiersze)
                    }
                    nowe_reguly.append(regula)
                    widziane_warunki.add(polaczony_warunek)

        return nowe_reguly

    reguly[2] = polacz_reguly(reguly[1])
    reguly[3] = polacz_reguly(reguly[2])

    return reguly


def wypisz_reguly(reguly):
    """Wyświetla reguły decyzyjne"""
    for rzad, lista_regul in reguly.items():
        print(f"\nReguły rzędu {rzad}:")
        for regula in lista_regul:
            tekst_wsparcia = f"[{regula['wsparcie']}]" if regula['wsparcie'] > 1 else ""
            print(f"{regula['warunek']} ==> (Decyzja = {regula['decyzja']}) {tekst_wsparcia}")


def main():
    df = wczytaj_plik('dane/SystemDecyzyjny.txt')
    macierz_nieodrozn = macierz(df)
    print("\nMacierz nieodróżnialności:")
    for (i, j), atrybuty in macierz_nieodrozn.items():
        print(f"({i}, {j}): {', '.join(atrybuty) if atrybuty else '{}'}")

    reguly = generuj_reguly(df, macierz_nieodrozn)
    wypisz_reguly(reguly)


if __name__ == '__main__':
    main()