from pymongo import MongoClient


# Conecta ao MongoDB
client = MongoClient("mongodb://localhost:27017/")

db = client["cp1_db"]
colecao = db["eventos"]


# Limpa execuções anteriores para não duplicar os dados
colecao.delete_many({})


# IPs usados nos eventos
ips = [
    "185.220.101.1",
    "91.240.118.172",
    "45.33.32.156",
    "192.168.1.10"
]


# Gera 1000 eventos
eventos = []

for i in range(1000):
    evento = {
        "id_evento": i + 1,
        "ip": ips[i % 4],
        "tipo": "ACESSO"
    }

    eventos.append(evento)


# Insere todos de uma vez
colecao.insert_many(eventos)

print("1000 eventos inseridos.")


# Cria índice no campo ip
colecao.create_index("ip")

print("Índice criado em 'ip'.")


# Consulta um IP específico
ip_procurado = "185.220.101.1"

resultado = list(
    colecao.find({"ip": ip_procurado})
)

print(
    f"Eventos do IP {ip_procurado}:",
    len(resultado)
)
