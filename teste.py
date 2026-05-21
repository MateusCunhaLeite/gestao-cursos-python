import mysql.connector

print("Passo 1: Tentando achar o MySQL (XAMPP)...")

try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="", # Senha padrão do XAMPP é vazia
        database="plataforma_cursos"
    )
    print("Passo 2: CONEXÃO BEM SUCEDIDA! O banco existe.")
    conexao.close()
except Exception as e:
    print(f"============= ERRO NO BANCO =============")
    print(e)
    print(f"=========================================")