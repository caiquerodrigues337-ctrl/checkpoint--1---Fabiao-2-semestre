import mysql.connector


# Conexão com o MySQL local
conexao = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="1234",
    database="cp1_db"
)

cursor = conexao.cursor()


# Cria a tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100)
)
""")


# Limpa execuções anteriores
cursor.execute("DELETE FROM usuarios")


# Usuários do exercício
usuarios = [
    ("admin", "admin@x.com"),
    ("ana", "ana@x.com"),
    ("bruno", "bruno@x.com")
]

cursor.executemany(
    "INSERT INTO usuarios (nome, email) VALUES (%s, %s)",
    usuarios
)

conexao.commit()


# ============================================
# FUNÇÃO INSEGURA
# ============================================

def busca_insegura(nome):

    # ERRADO: entrada do usuário é colocada diretamente no SQL
    sql = "SELECT nome, email FROM usuarios WHERE nome = '" + nome + "'"

    cursor.execute(sql)

    return cursor.fetchall()


# ============================================
# FUNÇÃO SEGURA
# ============================================

def busca_segura(nome):

    # CERTO: o valor é enviado separadamente da consulta SQL
    sql = "SELECT nome, email FROM usuarios WHERE nome = %s"

    cursor.execute(sql, (nome,))

    return cursor.fetchall()


# Entrada usada no exercício
entrada = "' OR '1'='1"


# Teste inseguro
resultado_inseguro = busca_insegura(entrada)

print(
    f"[INSEGURO] entrada={entrada!r} -> "
    f"{len(resultado_inseguro)} usuários (VAZAMENTO)"
)


# Teste seguro
resultado_seguro = busca_segura(entrada)

print(
    f"[SEGURO] entrada={entrada!r} -> "
    f"{len(resultado_seguro)} usuários (defesa OK)"
)


cursor.close()
conexao.close()