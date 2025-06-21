import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# siec neuronowa
class SiecNeuronowa:
    def __init__(self, n_ukrytych=5, learning_rate=0.01):
        self.n_ukrytych = n_ukrytych
        self.learning_rate = learning_rate

    # funkcja ReLu
    def relu(self, x):
        return np.maximum(0, x)

    def relu_pochodna(self, x):
        return (x > 0).astype(float)

    # funkcja sigmoid
    def sigmoid(self, x):
        # żeby nie było overflow
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def sigmoid_pochodna(self, x):
        s = self.sigmoid(x)
        return s * (1 - s)

    # wagi losowe [0,1]
    def inicjalizuj_wagi(self, n_wejsc):
        np.random.seed(42)

        # wagi wejście -> ukryte
        self.W1 = np.random.rand(n_wejsc, self.n_ukrytych)
        self.b1 = np.random.rand(1, self.n_ukrytych)

        # wagi ukryte -> wyjście
        self.W2 = np.random.rand(self.n_ukrytych, 1)
        self.b2 = np.random.rand(1, 1)

    # propagacja w przod
    def propagacja_w_przod(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = self.relu(self.z1)

        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2

    # koszt
    def oblicz_koszt(self, y, y_hat):
        m = y.shape[0]
        # mala wartosc epsilon zeby uniknac log(0)
        epsilon = 1e-15
        y_hat = np.clip(y_hat, epsilon, 1 - epsilon)
        return -np.sum(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat)) / m

    # propagacja wsteczna
    def propagacja_wstecz(self, X, y):
        m = X.shape[0]

        # Warstwa wyjściowa
        dz2 = self.a2 - y  # To jest poprawny gradient dla BCE + sigmoid
        dW2 = self.a1.T @ dz2 / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m

        # Warstwa ukryta
        da1 = dz2 @ self.W2.T
        dz1 = da1 * self.relu_pochodna(self.z1)
        dW1 = X.T @ dz1 / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m

        return dW1, db1, dW2, db2

    # wagi
    def aktualizuj_wagi(self, dW1, db1, dW2, db2):
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2

    # glowna petla
    def trenuj(self, X, y, epoki=100):
        self.inicjalizuj_wagi(X.shape[1])
        y = y.reshape(-1, 1) if y.ndim == 1 else y

        for epoka in range(epoki):
            y_hat = self.propagacja_w_przod(X)

            koszt = self.oblicz_koszt(y, y_hat)

            dW1, db1, dW2, db2 = self.propagacja_wstecz(X, y)

            self.aktualizuj_wagi(dW1, db1, dW2, db2)

            if (epoka + 1) % 10 == 0:
                print(f"Epoka {epoka + 1}: koszt = {koszt:.4f}, dokładność = {self.oblicz_dokladnosc(X, y):.4f}")

    # przewidywanie
    def przewiduj(self, X):
        return (self.propagacja_w_przod(X) > 0.5).astype(int)

    # dokladnosc modelu
    def oblicz_dokladnosc(self, X, y):
        y = y.reshape(-1, 1) if y.ndim == 1 else y
        return np.mean(self.przewiduj(X) == y)

def main():

    dane = load_breast_cancer()
    X, y = dane.data, dane.target

    print(f"Rozmiar danych: {X.shape}")
    print(f"Liczba klas: {len(np.unique(y))}")
    print(f"Klasy: {np.unique(y)} (0=malignant, 1=benign)")

    # podzial na train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # normalizacja danych
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # tworzenie sieci
    siec = SiecNeuronowa(n_ukrytych=5, learning_rate=0.01)

    # uczenie przez 100 epok
    siec.trenuj(X_train_scaled, y_train, epoki=100)

    print("\nWyniki końcowe:")
    dokladnosc_train = siec.oblicz_dokladnosc(X_train_scaled, y_train) * 100
    dokladnosc_test = siec.oblicz_dokladnosc(X_test_scaled, y_test) * 100

    print(f"Dokładność zbiór treningowy: {dokladnosc_train:.2f}%")
    print(f"Dokładność zbiór testowy:    {dokladnosc_test:.2f}%")

    # przewidywania przykladowe
    print("\nPrzykładowe przewidywania:")
    y_pred = siec.przewiduj(X_test_scaled[:10])
    print("Prawdziwe wartości: ", y_test[:10])
    print("Przewidywania:      ", y_pred.flatten())

    print(f"\nWarstwa wejściowa: {X.shape[1]} neuronów")
    print(f"Warstwa ukryta: {siec.n_ukrytych} neuronów ReLU")
    print(f"Warstwa wyjściowa: 1 neuron Sigmoid")
    print(f"Liczba parametrów: {siec.W1.size + siec.b1.size + siec.W2.size + siec.b2.size}")

    return siec, X_test_scaled, y_test


if __name__ == "__main__":
    siec, X_test, y_test = main()