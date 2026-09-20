print("O PROGRAMA COMEÇOU")
from pymongo import MongoClient
from datetime import datetime
from sklearn.tree import DecisionTreeClassifier
import re


# ============================================================
# 1. CONECTAR AO MONGODB
# ============================================================

client = MongoClient("mongodb://localhost:27017/")

db = client["siem_db"]
colecao = db["logs"]

# Apaga dados antigos para não duplicar caso execute novamente
colecao.delete_many({})


# ============================================================
# 2. LER O auth.log E NORMALIZAR AS LINHAS
# ============================================================

documentos = []

padrao = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) "
    r"(?P<tipo>\w+) "
    r"usuario=(?P<usuario>\S+) "
    r"ip=(?P<ip>\S+)"
)

with open("auth.log", "r", encoding="utf-8") as arquivo:

    for linha in arquivo:

        linha = linha.strip()

        # Ignora linhas vazias
        if not linha:
            continue

        resultado = padrao.match(linha)

        if resultado:

            documento = {
                "timestamp": datetime.strptime(
                    resultado.group("timestamp"),
                    "%Y-%m-%d %H:%M:%S"
                ),
                "tipo": resultado.group("tipo"),
                "usuario": resultado.group("usuario"),
                "ip": resultado.group("ip")
            }

            documentos.append(documento)


# ============================================================
# 3. INSERIR OS DOCUMENTOS NO MONGODB
# ============================================================

if documentos:
    colecao.insert_many(documentos)

print("Eventos inseridos no MongoDB:", len(documentos))


# ============================================================
# 4. CONTAR FAILS POR IP USANDO AGREGAÇÃO
# ============================================================

pipeline = [

    # Pega somente eventos FAIL
    {
        "$match": {
            "tipo": "FAIL"
        }
    },

    # Agrupa pelo IP
    {
        "$group": {
            "_id": "$ip",
            "qtd_fails": {
                "$sum": 1
            }
        }
    },

    # Ordena do maior número de falhas para o menor
    {
        "$sort": {
            "qtd_fails": -1
        }
    }
]

resultado_agregacao = list(colecao.aggregate(pipeline))


# ============================================================
# 5. CRIAR DATASET PARA MACHINE LEARNING
# ============================================================

X = []
y = []

print("\nContagem de FAILs por IP:")

for item in resultado_agregacao:

    ip = item["_id"]
    qtd_fails = item["qtd_fails"]

    # Regra do exercício:
    # >= 5 falhas = suspeito
    if qtd_fails >= 5:
        suspeito = 1
    else:
        suspeito = 0

    print(
        ip,
        "->",
        qtd_fails,
        "FAILs",
        "(suspeito=" + str(suspeito) + ")"
    )

    # X contém a característica usada pelo ML
    X.append([qtd_fails])

    # y contém a resposta correta
    y.append(suspeito)


print("\nDataset de treino:")
print("X =", X)
print("y =", y)


# ============================================================
# 6. TREINAR O CLASSIFICADOR
# ============================================================

modelo = DecisionTreeClassifier(
    max_depth=2,
    random_state=42
)

modelo.fit(X, y)


# ============================================================
# 7. PREVER UM NOVO IP COM 8 FALHAS
# ============================================================

novo_ip = [[8]]

previsao = modelo.predict(novo_ip)

print("\nPrevisão para IP com 8 falhas:")

if previsao[0] == 1:
    print("Suspeito (1)")
else:
    print("Não suspeito (0)")