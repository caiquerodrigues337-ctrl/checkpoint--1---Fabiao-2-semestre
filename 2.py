from pymongo import MongoClient


# Conecta ao MongoDB
client = MongoClient("mongodb://localhost:27017/")

db = client["cp1_db"]
colecao = db["vulnerabilidades"]


# Limpa execuções anteriores
colecao.delete_many({})


# ==========================================================
# CREATE - INSERÇÃO
# ==========================================================

vulns = [
    {
        "cve_id": "CVE-2024-001",
        "tipo": "SQL Injection",
        "severidade": "Alta",
        "corrigida": False
    },
    {
        "cve_id": "CVE-2024-002",
        "tipo": "XSS",
        "severidade": "Media",
        "corrigida": True
    },
    {
        "cve_id": "CVE-2024-003",
        "tipo": "Path Traversal",
        "severidade": "Critica",
        "corrigida": False
    }
]

resultado_insert = colecao.insert_many(vulns)

print(f"{len(resultado_insert.inserted_ids)} vulnerabilidades inseridas.")


# ==========================================================
# READ - BUSCAR POR SEVERIDADE
# ==========================================================

resultado_busca = colecao.find({"severidade": "Alta"})

for vuln in resultado_busca:
    print(
        f"Buscar severidade='Alta' -> "
        f"{vuln['cve_id']}: {vuln['tipo']}"
    )


# ==========================================================
# UPDATE - MARCAR CVE-2024-001 COMO CORRIGIDA
# ==========================================================

resultado_update = colecao.update_one(
    {"cve_id": "CVE-2024-001"},
    {"$set": {"corrigida": True}}
)

print(
    f"Update corrigida=True em 001 -> "
    f"{resultado_update.modified_count} documento modificado"
)


# Conta quantas continuam abertas
abertas = colecao.count_documents({"corrigida": False})

print(
    f"count corrigida=False -> {abertas} "
    f"(só a CVE-2024-003 restou aberta)"
)


# ==========================================================
# DELETE - EXCLUIR POR CVE_ID
# ==========================================================

resultado_delete = colecao.delete_one(
    {"cve_id": "CVE-2024-002"}
)

print(
    f"Delete CVE-2024-002 -> "
    f"{resultado_delete.deleted_count} documento removido"
)


client.close()