#D1 Deszczowa Goraco Wysoka Slaby Tak
#D2 Pochmurna Lagodnie Wysoka Slaby Tak
#D3 Sloneczna Chlodno Wysoka Mocny Tak
#D4 Sloneczna Goraco Wysoka Mocny Tak
#D5 Pochmurna Goraco Normalna Mocny Tak
#D6 Sloneczna Chlodno Wysoka Slaby Tak
#D7 Deszczowa Goraco Wysoka Mocny Tak
#D8 Deszczowa Chlodno Wysoka Mocny Tak
#D9 Deszczowa Lagodnie Normalna Mocny Tak
#D10 Deszczowa Lagodnie Wysoka Mocny Nie
#D11 Sloneczna Chlodno Normalna Mocny Nie
#D12 Deszczowa Lagodnie Normalna Slaby Nie
#D13 Pochmurna Goraco Wysoka Slaby Nie
#D14 Sloneczna Goraco Normalna Mocny Nie

#1 1 1 1 3 1 1
#1 1 1 1 3 2 1
#1 1 1 3 2 1 0
#1 1 1 3 3 2 1
#1 1 2 1 2 1 0
#1 1 2 1 2 2 1
#1 1 2 2 3 1 0
#1 1 2 2 4 1 1

#values.txt

with open("dane/values.txt", "r") as f:
    data = [list(map(int, line.split())) for line in f]

kolumny = ["a1", "a2", "a3", "a4", "a5", "a6", "d"]
wiersze = [f"o{i + 1}" for i in range(len(data))]

atrybuty = len(kolumny) - 1
obiekty = len(wiersze)

print("Liczba atrybutów:", atrybuty)
print("Liczba obiektów:", obiekty)

for i in range(obiekty):
    print("\nObiekt:", wiersze[i], data[i])

    for j in range(atrybuty):
        print(f"[{wiersze[i]}, {kolumny[j]}] = {data[i][j]} -> decyzja {data[i][-1]}")

        if data[i][-1] == 0 and data[i][j] == data[i][0]:
            print(f"Break na [{wiersze[i]}, {kolumny[j]}] = {data[i][j]}")
            break

#SystemDecyzyjny.txt

with open("dane/SystemDecyzyjny.txt", "r", encoding="utf-8") as f:
    data = [line.strip().split() for line in f]

kolumny = ["Pogoda", "Temperatura", "Wilgotnosc", "Wiatr", "Decyzja"]
wiersze = [f"D{i + 1}" for i in range(len(data))]

atrybuty = len(kolumny) - 1
obiekty = len(wiersze)

print("Liczba atrybutów:", atrybuty)
print("Liczba obiektów:", obiekty)

for i in range(obiekty):
    print("\nObiekt:", wiersze[i], data[i])

    for j in range(atrybuty):
        print(f"[{wiersze[i]}, {kolumny[j]}] = {data[i][j]} -> decyzja {data[i][-1]}")

        if data[i][-1] == "Nie" and data[i][j] == data[i][0]:
            print(f"Break na [{wiersze[i]}, {kolumny[j]}] = {data[i][j]}")
            break
