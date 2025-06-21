def wczytaj_dane(sciezka):
    # dane z txt
    dane = []
    with open(sciezka, 'r') as plik:
        for lin in plik:
            wier = lin.strip().split()
            dane.append(wier[1:])
    return dane


def znajdz_konc(dane):
    # koncepty find
    konc = {}
    for i, wier in enumerate(dane):
        dec = wier[-1]
        if dec not in konc:
            konc[dec] = []
        konc[dec].append(i)
    return konc

def oblicz_desk(dane):
     # deskryptory

    desk = {}
    l_atr = len(dane[0]) - 1

    for atr in range(l_atr):
        for obj, wier in enumerate(dane):
            war = wier[atr]
            klucz = (atr, war)

            if klucz not in desk:
                desk[klucz] = []
            desk[klucz].append(obj)

    return desk


def lem2(dane, atr_nazwy):
    # tu lem
    konc = znajdz_konc(dane)
    desk = oblicz_desk(dane)
    wszystkie_reg = []

    for dec, koncept in konc.items():
        niepokr = koncept.copy()
        print(f"\nPrzetwarzanie konceptu {dec}")

        while niepokr:
            print(f"Niepokryte obiekty: {[i + 1 for i in niepokr]}")

            obj_do_pokr = niepokr[0]
            print(f"Wybrano obiekt D{obj_do_pokr + 1} do pokrycia")

            pas_desk = []
            for (atr, war), objs in desk.items():
                if obj_do_pokr in objs:
                    pas_desk.append((atr, war))

            reg = []
            pokr_obj = set(range(len(dane)))

            while pokr_obj - set(koncept) and pas_desk:
                naj_desk = None
                naj_jak = -1
                naj_pokr = set()

                for desk_i in pas_desk:
                    nowe_pokr = pokr_obj & set(desk[desk_i])

                    z_konc = len(nowe_pokr & set(koncept))
                    spoza_konc = len(nowe_pokr - set(koncept))

                    if z_konc > 0:
                        jak = z_konc / (z_konc + spoza_konc) if spoza_konc > 0 else float('inf')

                        if jak > naj_jak:
                            naj_jak = jak
                            naj_desk = desk_i
                            naj_pokr = nowe_pokr

                if naj_desk:
                    reg.append(naj_desk)
                    pas_desk.remove(naj_desk)
                    pokr_obj = naj_pokr
                    print(
                        f"Dodano: ({atr_nazwy[naj_desk[0]]} = {naj_desk[1]})")
                else:
                    break

                if not (pokr_obj - set(koncept)):
                    break

            if reg and not (pokr_obj - set(koncept)):
                pokr_w_konc = pokr_obj & set(niepokr)

                for obj in pokr_w_konc:
                    if obj in niepokr:
                        niepokr.remove(obj)

                reg_txt = " ∧ ".join([f"({atr_nazwy[atr]} = {war})" for atr, war in reg])
                reg_txt += f" ==> (d = {dec})"

                l_pokr = len(pokr_w_konc)
                if l_pokr > 1:
                    reg_txt += f"[{l_pokr}]"

                wszystkie_reg.append(reg_txt)
                print(f"Utworzono regułę: {reg_txt}")
            else:
                print(f"!Nie udało się znaleźć reguły dla obiektu D{obj_do_pokr + 1}.")
                niepokr.remove(obj_do_pokr)

    return wszystkie_reg

def main():
        dane = wczytaj_dane("dane/SystemDecyzyjny.txt")

        atr_nazwy = ["Pogoda", "Temperatura", "Wilgotnosc", "Wiatr"]

        print("Wczytane dane:")
        for i, wier in enumerate(dane):
            print(f"D{i + 1}: {wier}")

        konc = znajdz_konc(dane)
        print("\nZnalezione koncepty:")
        for dec, objs in konc.items():
            objs_str = [f"D{i + 1}" for i in objs]
            print(f"Koncept {dec}: {', '.join(objs_str)}")

        print("\nWyliczanie reguł LEM2")
        reg = lem2(dane, atr_nazwy)

        print("\n Wszystkie reguły")
        for i, reg_i in enumerate(reg, 1):
            print(f"Reguła{i} {reg_i}")

if __name__ == "__main__":
    main()