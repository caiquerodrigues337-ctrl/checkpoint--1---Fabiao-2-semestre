import mysql.connector
from mysql.connector import Error


# Conexão com o MySQL
conexao = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="1234",
    database="cp1_db"
)

cursor = conexao.cursor()


# ==========================================================
# 1. CRIAR A TABELA
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS ativos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ip VARCHAR(45) UNIQUE NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    criticidade ENUM('baixa', 'media', 'alta') NOT NULL,
    status VARCHAR(20) NOT NULL
)
""")


# Limpa dados anteriores para poder testar várias vezes
cursor.execute("DELETE FROM ativos")
conexao.commit()


# ==========================================================
# 2. INSERT
# ==========================================================

ativos = [
    ("SRV-WEB01", "192.168.1.10", "servidor", "alta", "ativo"),
    ("PC-RH03", "192.168.1.45", "estacao", "baixa", "ativo"),
    ("SW-CORE01", "192.168.1.1", "switch", "media", "inativo")
]

cursor.executemany("""
INSERT INTO ativos (nome, ip, tipo, criticidade, status)
VALUES (%s, %s, %s, %s, %s)
""", ativos)

conexao.commit()

print("3 ativos inseridos.")


# ==========================================================
# 3. SELECT FILTRANDO POR TIPO
# ==========================================================

cursor.execute("""
SELECT nome, ip, criticidade, status
FROM ativos
WHERE tipo = %s
""", ("servidor",))

resultado = cursor.fetchone()

print(
    f"Listar tipo='servidor' -> "
    f"{resultado[0]} | {resultado[1]} | "
    f"{resultado[2]} | {resultado[3]}"
)


# ==========================================================
# 4. UPDATE
# ==========================================================

cursor.execute("""
UPDATE ativos
SET status = %s
WHERE nome = %s
""", ("ativo", "SW-CORE01"))

conexao.commit()

print(
    f"Após UPDATE status de SW-CORE01 para 'ativo' -> "
    f"{cursor.rowcount} registro atualizado"
)


# ==========================================================
# 5. TESTE DO UNIQUE NO IP
# ==========================================================

try:

    cursor.execute("""
    INSERT INTO ativos (nome, ip, tipo, criticidade, status)
    VALUES (%s, %s, %s, %s, %s)
    """, (
        "SRV-TESTE",
        "192.168.1.10",
        "servidor",
        "media",
        "ativo"
    ))

    conexao.commit()

except Error:

    conexao.rollback()

    print(
        "Inserir IP duplicado (192.168.1.10) "
        "-> erro de UNIQUE tratado"
    )


# ==========================================================
# 6. DELETE
# ==========================================================

cursor.execute("""
DELETE FROM ativos
WHERE nome = %s
""", ("PC-RH03",))

conexao.commit()

print(
    f"Remover PC-RH03 -> "
    f"{cursor.rowcount} registro removido"
)


cursor.close()
conexao.close()