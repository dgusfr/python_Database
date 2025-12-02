import sqlite3

# Conecta ao banco de dados (cria o arquivo se não existir)
com = sqlite3.connect("escola.db")
cursor = com.cursor()

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

# Create - Insere dados na tabela
# Inserimos o estudante primeiro para gerar o ID
cursor.execute("INSERT INTO estudantes (nome, idade) VALUES ('Carlos', 22)")

# Pegamos o ID do estudante recém-criado para usar na disciplina
id_estudante = cursor.lastrowid

# Inserimos a disciplina vinculando ao ID do estudante
cursor.execute(
    "INSERT INTO disciplinas (nome_disciplina, estudante_id) VALUES ('Python Avançado', ?)",
    (id_estudante,),
)


# Confirma as alterações no banco de dados
com.commit()

# Recupera dados da tabela
cursor.execute(
    """
    SELECT * FROM estudantes
"""
)
resultado = cursor.fetchall()
print(resultado)

# Fecha a conexão com o banco de dados
com.close()
