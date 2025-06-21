import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from collections import Counter

# dane
data = load_iris()
X = data.data
y = data.target

# podział danych (treningowy i testowy)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# odległość euklidesowa
def eukalidusowa(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))

# odległość Manhattan
def manhattan(x1, x2):
    return np.sum(np.abs(x1 - x2))

# odległość cosinusowa
def cosinus(x1, x2):
    dot_prod = np.dot(x1, x2)
    norm_x1 = np.linalg.norm(x1)
    norm_x2 = np.linalg.norm(x2)
    if norm_x1 == 0 or norm_x2 == 0:
        return 1.0
    return 1 - (dot_prod / (norm_x1 * norm_x2))

# zwraca przewidywane klasy
def knn(X_train, y_train, X_test, k=3, metric='eukalides'):
    # wybor odpowiedniej metryki
    if metric == 'eukalides':
        distance_function = eukalidusowa
    elif metric == 'manhattan':
        distance_function = manhattan
    elif metric == 'cosinus':
        distance_function = cosinus
    else:
        raise ValueError("Nieznana metryka")

    # lista
    przewidywanie = []

    # dla każdego punktu testowego
    for test_sample in X_test:

        dystans = []

        # obliczanie odległości do każdego punktu treningowego
        for i, train_sample in enumerate(X_train):
            dist = distance_function(test_sample, train_sample)
            dystans.append((dist, y_train[i]))

        # sortowanie według odległości
        dystans.sort(key=lambda x: x[0])

        # wybieranie k najbliższych sąsiadów
        sasiedzi = [label for _, label in dystans[:k]]

        # wybieranie najczęstszej klasy wśród sąsiadów
        najczestszy = Counter(sasiedzi).most_common(1)[0][0]
        przewidywanie.append(najczestszy)

    return przewidywanie

# obliczanie dokładności klasyfikacji
def oblicz_dokladnosc(y_true, y_pred):
    poprawne = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
    return (poprawne / len(y_true)) * 100

# Testowanie dla wszystkich trzech metryk
print("Wyniki KNN dla zbioru Iris: ")
print(f"Rozmiar zbioru treningowego: {len(X_train)}")
print(f"Rozmiar zbioru testowego: {len(X_test)}")
print("\nDokładność dla różnych metryk (k=3):")

for nazwa_metryki in ['eukalides', 'manhattan', 'cosinus']:

    przewidywanie = knn(X_train, y_train, X_test, k=3, metric=nazwa_metryki)
    dokladnosc = oblicz_dokladnosc(y_test, przewidywanie)

    print(f"Metryka {nazwa_metryki}: {dokladnosc:.2f}%")