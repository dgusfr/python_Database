produtos = [
  {"id": 1, "nome": "Teclado", "preco": 150.00},
  {"id": 2, "nome": "Mouse", "preco": 89.90}
]

print("ID\tProduto\t\tPreço")
for produto in produtos:
  print(f'{produto["id"]}\t{produto["nome"]}\t\t${produto["preco"]:.2f}')