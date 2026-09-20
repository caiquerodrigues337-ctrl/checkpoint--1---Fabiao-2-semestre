import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# Features: [bytes, porta, duracao]
X = np.array([
    [500, 80, 0.1],
    [1200, 80, 0.5],
    [64, 22, 0.02],
    [64000, 4444, 10.0],
    [45000, 8080, 15.0],
    [60000, 31337, 20.0],
    [800, 443, 0.3],
    [300, 53, 0.05],
    [55000, 9999, 18.0],
    [200, 25, 0.2]
])

# 0 = normal
# 1 = malicioso
y = np.array([0, 0, 0, 1, 1, 1, 0, 0, 1, 0])


# Divide os dados em treino e teste
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)


# Cria o modelo
modelo = RandomForestClassifier(random_state=42)


# Treina
modelo.fit(X_treino, y_treino)


# Faz previsões com os dados de teste
previsoes = modelo.predict(X_teste)


# Calcula acurácia
acuracia = accuracy_score(y_teste, previsoes)

print(f"Acurácia no teste: {acuracia:.2f}")


# Novo tráfego
caso_novo = [[58000, 4444, 16.0]]

resultado = modelo.predict(caso_novo)


if resultado[0] == 1:
    print(f"Caso novo {caso_novo[0]} -> Malicioso (1)")
else:
    print(f"Caso novo {caso_novo[0]} -> Normal (0)")