# tab = [
#     [1, 1, 1, 1, 3, 1, 1],
#     [1, 1, 1, 1, 3, 2, 1],
#     [1, 1, 1, 3, 2, 1, 0],
#     [1, 1, 1, 3, 3, 2, 1],
#     [1, 1, 2, 1, 2, 1, 0],
#     [1, 1, 2, 1, 2, 2, 1],
#     [1, 1, 2, 2, 3, 1, 0],
#     [1, 1, 2, 2, 4, 1, 1]
# ]
# print(tab)

f = open("dane/values.txt", "r")
# print(f.read())

data = []
for line in f:
    data.append([int(d) for d in line.split()])
print(data)

cols_d = ["a1", "a2", "a3", "a4", "a5", "a6", "d"]
rows_d = ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8"]

x = len(cols_d)-1
y = len(rows_d)-1

print(f"{x} {y}")

o_num = 1
a_num = 1
num_d = 0
for j in range(x):
    for i in range(y):
        # if data[i][j] == data[len(cols_d)-1][j]
        print(f"[{i},{j}]={data[i][j]} == [{data[i][x]}]") #[col,row]
        # if data[i][j] == 0:
        num_d = data[i][j]
        if data[i][x] == 0 and num_d == data[i][0]: # do poprawy 2nd arg
            # o_num = j+1
            # a_num = i+1
            # num_d = data[i+1][j+1]
            print(f"break:[{i+1},{j+1}]={data[i][j]}") #[col,row]
            # print(f"{rows_d[i]}, {cols_d[j]}")
            break

=-------------------------------------------------------

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
