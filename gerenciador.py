# gerenciador.py
import pymysql

class GerenciadorPlataforma:
    def __init__(self, host="localhost", user="root", password="", database="plataforma_cursos"):
        # Dicionário (Estrutura Linear) para guardar as configurações de conexão
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        
        # Dicionário simulando Módulos/Avaliações para complementar o requisito
        self.modulos_padrao = {
            "Modulo 1": "Introdução",
            "Modulo 2": "Desenvolvimento",
            "Modulo 3": "Avaliação Final"
        }
    
    def conectar(self):
        """Estabelece e retorna a conexão com o banco MySQL."""
        return pymysql.connect(**self.config)

    # ==========================
    # C R U D - Entidade CURSOS
    # ==========================

    def cadastrar_curso(self, nome, categoria, carga_horaria):
        """(CREATE) Insere um novo curso no banco de dados."""
        conexao = self.conectar()
        cursor = conexao.cursor()
        sql = "INSERT INTO cursos (nome, categoria, carga_horaria) VALUES (%s, %s, %s)"
        
        # Tupla (Estrutura Linear) para passar os valores da query
        valores = (nome, categoria, carga_horaria)
        
        cursor.execute(sql, valores)
        conexao.commit()
        
        cursor.close()
        conexao.close()

    def listar_cursos(self):
        """(READ) Retorna uma lista de tuplas com os cursos."""
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM cursos")
        
        # Retorna uma Lista de Tuplas (Estruturas Lineares)
        resultados = cursor.fetchall() 
        
        cursor.close()
        conexao.close()
        return resultados

    def deletar_curso(self, id_curso):
        """(DELETE) Remove um curso pelo seu ID."""
        conexao = self.conectar()
        cursor = conexao.cursor()
        sql = "DELETE FROM cursos WHERE id = %s"
        
        # Tupla com um único elemento
        valores = (id_curso,)
        
        cursor.execute(sql, valores)
        conexao.commit()
        
        cursor.close()
        conexao.close()
        
    def obter_modulos_texto(self):
        """Retorna os módulos formatados a partir do Dicionário."""
        texto = ""
        for modulo, descricao in self.modulos_padrao.items():
            texto += f"{modulo}: {descricao}\n"
        return texto