import sqlite3

# Conecta ao banco de dados (cria o arquivo se não existir)
conn = sqlite3.connect("escola.db")
cursor = conn.cursor()

# CRUD - Create, Read, Update, Delete
# Executa comandos SQL para criar uma tabela (se não existir)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS estudantes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY,
        nome_disciplina TEXT,
        estudante_id INTEGER,
        FOREIGN KEY (estudante_id) REFERENCES estudantes(id)
    )
"""
)

# ------------------------------------------------------------

# CREATE - Insere dados na tabela
# Inserimos o estudante primeiro para gerar o ID
cursor.execute(
    """
    INSERT INTO estudantes (nome, idade) 
    VALUES (?, ?)
    """,
    ("Ana Silva", 22),
)

# Pegamos o ID do estudante recém-criado para usar na disciplina
id_estudante = cursor.lastrowid

# Inserimos a disciplina vinculando ao ID do estudante
cursor.execute(
    "INSERT INTO disciplinas (nome_disciplina, estudante_id) VALUES ('Python Avançado', ?)",
    (id_estudante,),
)


# Confirma as alterações no banco de dados
conn.commit()

# ------------------------------------------------------------

# READ - Lê os dados da tabela
cursor.execute("SELECT id, nome, idade FROM estudantes")

# O método fetchall() recupera todas as linhas do resultado da consulta
estudantes = cursor.fetchall()

print("--- Estudantes ---")
for estudante in estudantes:
    print(f"ID: {estudante[0]}, Nome: {estudante[1]}, Idade: {estudante[2]}")


conn.close()

# ------------------------------------------------------------

# Update - Atualiza dados na tabela
conn = sqlite3.connect("escola.db")
cursor = conn.cursor()


cursor.execute(
    """
    UPDATE estudantes 
    SET idade = ? 
    WHERE nome = ?
    """,
    (25, "Ana Silva"),
)

conn.commit()
print(f"\nUpdate realizado. Linhas afetadas: {cursor.rowcount}")
conn.close()

# ------------------------------------------------------------

# Delete - Remove dados da tabela
conn = sqlite3.connect("escola.db")
cursor = conn.cursor()

# Habilitar Foreign Keys é crucial, especialmente para DELETE
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute(
    """
    DELETE FROM estudantes 
    WHERE id = ?
""",
    (1),
)

conn.commit()

print(f"A operação DELETE removeu {cursor.rowcount} registro(s).")

conn.close()
