import sqlite3

# Conecta ao banco de dados (cria o arquivo se não existir)
com = sqlite3.connect("escola.db")
cursor = com.cursor()

# CRUD - Create, Read, Update, Delete
# Executa comandos SQL para criar uma tabela (se não existir)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS disciplinas (
        id INTEGER PRIMARY KEY,
        nome_disciplina TEXT,
        estudante_id INTEGER
        FOREIGN KEY (estudante_id) REFERENCES estudantes(id)
    )
"""
)

# Create - Insere dados na tabela
cursor.execute(
    """
    INSERT INTO estudantes (nome, idade) VALUES ('João', 20)
"""
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
