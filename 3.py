from pymongo import MongoClient


# Conecta ao MongoDB
client = MongoClient("mongodb://localhost:27017/")

db = client["cp1_db"]
colecao = db["eventos_ex3"]


# Limpa execuções anteriores
colecao.delete_many({})


# Eventos fornecidos pelo exercício
eventos = [
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "OK",   "ip": "192.168.1.10"},
    {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "45.33.32.156"},
    {"tipo": "FAIL", "ip": "185.220.101.1"}
]


# Insere os eventos no MongoDB
colecao.insert_many(eventos)


# Pipeline de agregação
pipeline = [

    # 1 - Pega somente eventos FAIL
    {
        "$match": {
            "tipo": "FAIL"
        }
    },

    # 2 - Agrupa pelo IP e conta quantos existem
    {
        "$group": {
            "_id": "$ip",
            "total": {
                "$sum": 1
            }
        }
    },

    # 3 - Ordena do maior para o menor
    {
        "$sort": {
            "total": -1
        }
    },

    # 4 - Retorna somente os 3 primeiros
    {
        "$limit": 3
    }
]


# Executa a agregação
resultado = colecao.aggregate(pipeline)


print("Top 3 IPs com mais FAILs:")

for item in resultado:
    print(f"{item['_id']} -> {item['total']}")


client.close()