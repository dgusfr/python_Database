from pymongo import MongoClient

# Conecta ao MongoDB (certifique-se de que o MongoDB esteja rodando localmente)
client = MongoClient("mongodb://localhost:27017/")

# Acessa o banco de dados "escola"
db = client["escola"]

# Acessa a coleção "estudantes"
estudantes = db["estudantes"]

# Insere alguns estudantes (pode comentar ou remover após a primeira execução)
estudantes.insert_one({"nome": "João", "idade": 20})
estudantes.insert_one({"nome": "Pedro", "idade": 21})
estudantes.insert_one({"nome": "Maria", "idade": 22})

# Imprime todos os estudantes no banco de dados
print("Estudantes no banco de dados:")
for estudante in estudantes.find():
    print(estudante)

# Fechar a conexão (boa prática, mas geralmente não é necessário em scripts simples)
client.close()
