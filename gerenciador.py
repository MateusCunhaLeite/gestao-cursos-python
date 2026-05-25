# gerenciador.py
# Camada de lógica e persistência de dados do sistema E-Learning.
# Realiza a conexão com o banco de dados MySQL via XAMPP usando PyMySQL.

import pymysql

class GerenciadorPlataforma:
    def __init__(self, host="localhost", user="root", password="", database="plataforma_cursos"):
        # Dicionário com as configurações de conexão ao banco de dados
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }

    def conectar(self):
        """Estabelece e retorna uma conexão com o banco MySQL."""
        return pymysql.connect(**self.config)

    # ==========================
    # C R U D - Entidade CURSOS
    # ==========================

    def cadastrar_curso(self, nome, categoria, carga_horaria):
        """(CREATE) Insere um novo curso no banco de dados."""
        conexao = self.conectar()
        cursor = conexao.cursor()
        # Tupla com os valores a serem inseridos (evita SQL Injection)
        cursor.execute(
            "INSERT INTO cursos (nome, categoria, carga_horaria) VALUES (%s, %s, %s)",
            (nome, categoria, carga_horaria)
        )
        conexao.commit()
        cursor.close()
        conexao.close()

    def listar_cursos(self):
        """(READ) Retorna uma Lista de Tuplas com todos os cursos."""
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM cursos")
        resultados = cursor.fetchall()  # Lista de Tuplas retornada pelo banco
        cursor.close()
        conexao.close()
        return resultados

    def deletar_curso(self, id_curso):
        """(DELETE) Remove um curso pelo seu ID."""
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM cursos WHERE id = %s", (id_curso,))
        conexao.commit()
        cursor.close()
        conexao.close()

    # ==========================
    # C R U D - Entidade ALUNOS
    # ==========================

    def cadastrar_aluno(self, nome, email, curso_id):
        """(CREATE) Insere um novo aluno no banco de dados."""
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO alunos (nome, email, curso_id) VALUES (%s, %s, %s)",
            (nome, email, curso_id)
        )
        conexao.commit()
        cursor.close()
        conexao.close()

    def listar_alunos(self):
        """(READ) Retorna uma Lista de Tuplas com todos os alunos."""
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM alunos")
        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()
        return resultados

    def deletar_aluno(self, id_aluno):
        """(DELETE) Remove um aluno pelo seu ID."""
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM alunos WHERE id = %s", (id_aluno,))
        conexao.commit()
        cursor.close()
        conexao.close()

    # ==============================
    # C R U D - Entidade PROFESSORES
    # ==============================

    def cadastrar_professor(self, nome, especialidade, email):
        """(CREATE) Insere um novo professor no banco de dados."""
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO professores (nome, especialidade, email) VALUES (%s, %s, %s)",
            (nome, especialidade, email)
        )
        conexao.commit()
        cursor.close()
        conexao.close()

    def listar_professores(self):
        """(READ) Retorna uma Lista de Tuplas com todos os professores."""
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM professores")
        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()
        return resultados

    def deletar_professor(self, id_professor):
        """(DELETE) Remove um professor pelo seu ID."""
        conexao = self.conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM professores WHERE id = %s", (id_professor,))
        conexao.commit()
        cursor.close()
        conexao.close()
