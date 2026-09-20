import numpy as np
from sklearn.ensemble import IsolationForest

# [requisicoes_min, conexoes_simultaneas]
trafego = np.array([
    [100, 5],
    [120, 6],
    [110, 5],
    [105, 4],
    [50000, 500],
    [109, 5],
    [111, 6],
    [45000, 450]
])

# Criando o modelo
modelo = IsolationForest(
    contamination=0.25,
    random_state=42
)

# Treinando e classificando
resultado = modelo.fit_predict(trafego)

# Mostrando os resultados
for i, classificacao in enumerate(resultado):

    if classificacao == -1:
        print(f"Amostra {i}: {trafego[i].tolist()} -> ANOMALIA")
    else:
        print(f"Amostra {i}: {trafego[i].tolist()} -> Normal")