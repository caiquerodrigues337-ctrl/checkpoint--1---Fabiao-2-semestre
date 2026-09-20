import mysql.connector


# Conexão com o MySQL
conexao = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="1234",
    database="cp1_db",
    autocommit=True
)

cursor = conexao.cursor()


# Cria a tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS contas (
    id INT PRIMARY KEY,
    titular VARCHAR(100),
    saldo DECIMAL(10,2)
)
""")


# Reinicia os dados
cursor.execute("DELETE FROM contas")

cursor.execute(
    "INSERT INTO contas (id, titular, saldo) VALUES (%s, %s, %s)",
    (1, "Alice", 1000)
)

cursor.execute(
    "INSERT INTO contas (id, titular, saldo) VALUES (%s, %s, %s)",
    (2, "Bob", 500)
)


# Função de transferência
def transferir(origem, destino, valor):

    try:
        # Inicia uma transação manual
        conexao.start_transaction()

        # Retira dinheiro da origem
        cursor.execute(
            "UPDATE contas SET saldo = saldo - %s WHERE id = %s",
            (valor, origem)
        )

        if cursor.rowcount != 1:
            raise Exception("Conta de origem inexistente")

        # Coloca dinheiro no destino
        cursor.execute(
            "UPDATE contas SET saldo = saldo + %s WHERE id = %s",
            (valor, destino)
        )

        if cursor.rowcount != 1:
            raise Exception("Conta destino inexistente")

        # Tudo funcionou
        conexao.commit()

        return True

    except Exception as erro:

        # Alguma operação falhou
        conexao.rollback()

        print("Erro:", erro)

        return False


# =====================================================
# TESTE 1
# Alice manda 200 para Bob
# =====================================================

sucesso = transferir(1, 2, 200)

cursor.execute("SELECT saldo FROM contas WHERE id = 1")
saldo_alice = cursor.fetchone()[0]

cursor.execute("SELECT saldo FROM contas WHERE id = 2")
saldo_bob = cursor.fetchone()[0]

if sucesso:
    print(
        f"Transferência 1 OK. Alice={saldo_alice:.0f}, Bob={saldo_bob:.0f}"
    )


# =====================================================
# TESTE 2
# Alice tenta mandar 100 para uma conta inexistente
# =====================================================

sucesso = transferir(1, 99, 100)

cursor.execute("SELECT saldo FROM contas WHERE id = 1")
saldo_alice = cursor.fetchone()[0]

if not sucesso:
    print(
        f"Transferência 2 FALHOU "
        f"(conta destino inexistente). "
        f"Rollback. Alice={saldo_alice:.0f}"
    )


cursor.close()
conexao.close()
