# main.py
# Interface gráfica do sistema de gestão da plataforma E-Learning.
# Utiliza a biblioteca CustomTkinter para construção dos componentes visuais.

import customtkinter as ctk
import tkinter.messagebox as messagebox

# Importação da camada de lógica/dados (Modularização)
from gerenciador import GerenciadorPlataforma

# Configurações globais de aparência da interface
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")


# ============================================================
# CLASSE BASE: JanelaEntidade
# Padrão reutilizável (herança) para as 3 entidades do sistema.
# Cada entidade (Cursos, Alunos, Professores) herda desta classe,
# aproveitando o mesmo layout de menu lateral + área de conteúdo.
# ============================================================
class JanelaEntidade(ctk.CTkToplevel):
    def __init__(self, master, titulo):
        super().__init__(master)
        self.title(titulo)
        self.geometry("750x550")
        self.grab_set()  # Torna a janela modal: bloqueia a tela inicial enquanto estiver aberta

        # Configuração do grid: coluna 1 (conteúdo) se expande, coluna 0 (menu) é fixa
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Menu Lateral ---
        self.frame_menu = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nsew")
        self.frame_menu.grid_rowconfigure(5, weight=1)  # Empurra os botões para o topo

        # Título do menu lateral com o nome da entidade
        ctk.CTkLabel(self.frame_menu, text=titulo, font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, padx=20, pady=(20, 10)
        )

        # Botão de navegação para o formulário de listagem
        ctk.CTkButton(self.frame_menu, text="Listar", command=self.mostrar_lista).grid(
            row=1, column=0, padx=20, pady=10
        )

        # Botão de navegação para o formulário de cadastro
        ctk.CTkButton(self.frame_menu, text="Novo", command=self.mostrar_cadastro).grid(
            row=2, column=0, padx=20, pady=10
        )

        # --- Área de Conteúdo ---
        # Frame dinâmico onde os formulários são renderizados
        self.frame_conteudo = ctk.CTkFrame(self)
        self.frame_conteudo.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.frame_conteudo.grid_columnconfigure(0, weight=1)

        # Exibe a listagem ao abrir a janela
        self.mostrar_lista()

    def limpar_conteudo(self):
        """Remove todos os widgets do frame de conteúdo antes de renderizar um novo formulário."""
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

    # Métodos abstratos: cada subclasse implementa sua própria versão
    def mostrar_lista(self): pass
    def mostrar_cadastro(self): pass

    def _criar_textbox(self, cabecalho, linhas):
        """
        Cria o componente de texto somente-leitura para exibir os registros.
        Recebe o cabeçalho da tabela e uma lista de strings (uma por registro).
        Utiliza uma Lista para iterar e montar o conteúdo exibido.
        """
        # Título do formulário gerado a partir do cabeçalho
        ctk.CTkLabel(
            self.frame_conteudo,
            text=cabecalho.split("|")[0].strip() + "s Cadastrados",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, pady=(20, 10))

        # Caixa de texto para exibir os dados em formato tabular
        textbox = ctk.CTkTextbox(self.frame_conteudo, width=450, height=300)
        textbox.grid(row=1, column=0, padx=20, pady=10)

        # Monta o conteúdo: cabeçalho + separador + linhas da lista
        textbox.insert("0.0", cabecalho + "\n" + "-" * 50 + "\n" + "\n".join(linhas))
        textbox.configure(state="disabled")  # Impede edição manual pelo usuário

    def _criar_frame_delete(self, placeholder, comando):
        """
        Cria o mini-formulário de exclusão por ID (operação DELETE do CRUD).
        Recebe o texto de placeholder do campo e a função a ser chamada ao deletar.
        """
        frame = ctk.CTkFrame(self.frame_conteudo)
        frame.grid(row=2, column=0, pady=10)

        # Campo de entrada para o ID do registro a ser removido
        self.entry_id_del = ctk.CTkEntry(frame, placeholder_text=placeholder)
        self.entry_id_del.pack(side="left", padx=5)

        # Botão de exclusão com cor vermelha para indicar ação destrutiva
        ctk.CTkButton(
            frame, text="Deletar",
            fg_color="#c0392b", hover_color="#e74c3c",
            command=comando
        ).pack(side="left", padx=5)


# ============================================================
# JANELA DE CURSOS
# Herda de JanelaEntidade e implementa o CRUD da entidade Curso.
# Campos: Nome, Categoria, Carga Horária
# ============================================================
class JanelaCursos(JanelaEntidade):
    def __init__(self, master, plataforma):
        self.plataforma = plataforma  # Referência ao gerenciador de dados
        super().__init__(master, "Cursos")

    def mostrar_lista(self):
        """(READ) Busca os cursos e exibe em tela usando uma Lista de Tuplas."""
        self.limpar_conteudo()
        cursos = self.plataforma.listar_cursos()  # Retorna Lista de Tuplas

        # Itera sobre a Lista de Tuplas para formatar cada linha de exibição
        linhas = [f"[{c[0]}] {c[1]} | {c[2]} | {c[3]}h" for c in cursos]

        self._criar_textbox("ID | Nome | Categoria | Carga Horária", linhas)
        self._criar_frame_delete("ID do Curso p/ Deletar", self._deletar)

    def mostrar_cadastro(self):
        """Renderiza o formulário de cadastro de novo curso."""
        self.limpar_conteudo()
        ctk.CTkLabel(self.frame_conteudo, text="Cadastrar Novo Curso",
                     font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=(20, 20))

        self.entry_nome = ctk.CTkEntry(self.frame_conteudo, placeholder_text="Nome do Curso", width=300)
        self.entry_nome.grid(row=1, column=0, pady=10)

        self.entry_categoria = ctk.CTkEntry(self.frame_conteudo, placeholder_text="Categoria", width=300)
        self.entry_categoria.grid(row=2, column=0, pady=10)

        self.entry_horas = ctk.CTkEntry(self.frame_conteudo, placeholder_text="Carga Horária (horas)", width=300)
        self.entry_horas.grid(row=3, column=0, pady=10)

        ctk.CTkButton(self.frame_conteudo, text="Salvar Curso", command=self._salvar).grid(row=4, column=0, pady=20)

    def _salvar(self):
        """(CREATE) Valida os campos e persiste o novo curso."""
        try:
            nome = self.entry_nome.get()
            categoria = self.entry_categoria.get()
            horas = int(self.entry_horas.get())  # Valida que carga horária é numérica
            if not nome or not categoria:
                raise ValueError
            self.plataforma.cadastrar_curso(nome, categoria, horas)
            messagebox.showinfo("Sucesso", "Curso cadastrado com sucesso!")
            self.mostrar_lista()  # Redireciona para a listagem atualizada
        except ValueError:
            messagebox.showerror("Aviso", "Preencha todos os campos corretamente.")
        except Exception as e:
            messagebox.showerror("Erro de BD", str(e))

    def _deletar(self):
        """(DELETE) Remove o curso pelo ID informado."""
        try:
            self.plataforma.deletar_curso(int(self.entry_id_del.get()))
            messagebox.showinfo("Sucesso", "Curso removido com sucesso!")
            self.mostrar_lista()
        except ValueError:
            messagebox.showerror("Aviso", "Insira um ID válido.")
        except Exception as e:
            messagebox.showerror("Erro de BD", str(e))


# ============================================================
# JANELA DE ALUNOS
# Herda de JanelaEntidade e implementa o CRUD da entidade Aluno.
# Campos: Nome, Email, ID do Curso (matrícula)
# ============================================================
class JanelaAlunos(JanelaEntidade):
    def __init__(self, master, plataforma):
        self.plataforma = plataforma
        super().__init__(master, "Alunos")

    def mostrar_lista(self):
        """(READ) Busca os alunos e exibe em tela usando uma Lista de Tuplas."""
        self.limpar_conteudo()
        alunos = self.plataforma.listar_alunos()  # Retorna Lista de Tuplas

        # Itera sobre a Lista de Tuplas para formatar cada linha de exibição
        linhas = [f"[{a[0]}] {a[1]} | {a[2]} | Curso ID: {a[3]}" for a in alunos]

        self._criar_textbox("ID | Nome | Email | Curso", linhas)
        self._criar_frame_delete("ID do Aluno p/ Deletar", self._deletar)

    def mostrar_cadastro(self):
        """Renderiza o formulário de cadastro de novo aluno."""
        self.limpar_conteudo()
        ctk.CTkLabel(self.frame_conteudo, text="Cadastrar Novo Aluno",
                     font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=(20, 20))

        self.entry_nome = ctk.CTkEntry(self.frame_conteudo, placeholder_text="Nome do Aluno", width=300)
        self.entry_nome.grid(row=1, column=0, pady=10)

        self.entry_email = ctk.CTkEntry(self.frame_conteudo, placeholder_text="Email", width=300)
        self.entry_email.grid(row=2, column=0, pady=10)

        # O curso_id vincula o aluno a um curso já cadastrado
        self.entry_curso_id = ctk.CTkEntry(self.frame_conteudo, placeholder_text="ID do Curso (número)", width=300)
        self.entry_curso_id.grid(row=3, column=0, pady=10)

        ctk.CTkButton(self.frame_conteudo, text="Salvar Aluno", command=self._salvar).grid(row=4, column=0, pady=20)

    def _salvar(self):
        """(CREATE) Valida os campos e persiste o novo aluno."""
        try:
            nome = self.entry_nome.get()
            email = self.entry_email.get()
            curso_id = int(self.entry_curso_id.get())  # Valida que o ID do curso é numérico
            if not nome or not email:
                raise ValueError
            self.plataforma.cadastrar_aluno(nome, email, curso_id)
            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
            self.mostrar_lista()
        except ValueError:
            messagebox.showerror("Aviso", "Preencha todos os campos corretamente.")
        except Exception as e:
            messagebox.showerror("Erro de BD", str(e))

    def _deletar(self):
        """(DELETE) Remove o aluno pelo ID informado."""
        try:
            self.plataforma.deletar_aluno(int(self.entry_id_del.get()))
            messagebox.showinfo("Sucesso", "Aluno removido com sucesso!")
            self.mostrar_lista()
        except ValueError:
            messagebox.showerror("Aviso", "Insira um ID válido.")
        except Exception as e:
            messagebox.showerror("Erro de BD", str(e))


# ============================================================
# JANELA DE PROFESSORES
# Herda de JanelaEntidade e implementa o CRUD da entidade Professor.
# Campos: Nome, Especialidade, Email
# ============================================================
class JanelaProfessores(JanelaEntidade):
    def __init__(self, master, plataforma):
        self.plataforma = plataforma
        super().__init__(master, "Professores")

    def mostrar_lista(self):
        """(READ) Busca os professores e exibe em tela usando uma Lista de Tuplas."""
        self.limpar_conteudo()
        professores = self.plataforma.listar_professores()  # Retorna Lista de Tuplas

        # Itera sobre a Lista de Tuplas para formatar cada linha de exibição
        linhas = [f"[{p[0]}] {p[1]} | {p[2]} | {p[3]}" for p in professores]

        self._criar_textbox("ID | Nome | Especialidade | Email", linhas)
        self._criar_frame_delete("ID do Professor p/ Deletar", self._deletar)

    def mostrar_cadastro(self):
        """Renderiza o formulário de cadastro de novo professor."""
        self.limpar_conteudo()
        ctk.CTkLabel(self.frame_conteudo, text="Cadastrar Novo Professor",
                     font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=(20, 20))

        self.entry_nome = ctk.CTkEntry(self.frame_conteudo, placeholder_text="Nome do Professor", width=300)
        self.entry_nome.grid(row=1, column=0, pady=10)

        self.entry_especialidade = ctk.CTkEntry(self.frame_conteudo, placeholder_text="Especialidade", width=300)
        self.entry_especialidade.grid(row=2, column=0, pady=10)

        self.entry_email = ctk.CTkEntry(self.frame_conteudo, placeholder_text="Email", width=300)
        self.entry_email.grid(row=3, column=0, pady=10)

        ctk.CTkButton(self.frame_conteudo, text="Salvar Professor", command=self._salvar).grid(row=4, column=0, pady=20)

    def _salvar(self):
        """(CREATE) Valida os campos e persiste o novo professor."""
        try:
            nome = self.entry_nome.get()
            especialidade = self.entry_especialidade.get()
            email = self.entry_email.get()
            if not nome or not especialidade or not email:
                raise ValueError
            self.plataforma.cadastrar_professor(nome, especialidade, email)
            messagebox.showinfo("Sucesso", "Professor cadastrado com sucesso!")
            self.mostrar_lista()
        except ValueError:
            messagebox.showerror("Aviso", "Preencha todos os campos corretamente.")
        except Exception as e:
            messagebox.showerror("Erro de BD", str(e))

    def _deletar(self):
        """(DELETE) Remove o professor pelo ID informado."""
        try:
            self.plataforma.deletar_professor(int(self.entry_id_del.get()))
            messagebox.showinfo("Sucesso", "Professor removido com sucesso!")
            self.mostrar_lista()
        except ValueError:
            messagebox.showerror("Aviso", "Insira um ID válido.")
        except Exception as e:
            messagebox.showerror("Erro de BD", str(e))


# ============================================================
# TELA INICIAL (App)
# Ponto de entrada visual do sistema. Exibe os 3 botões de
# navegação para as entidades: Cursos, Alunos e Professores.
# ============================================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("E-Learning: Gestão de Plataforma")
        self.geometry("400x300")
        self.resizable(False, False)

        # Instancia o gerenciador de dados (camada de lógica)
        self.plataforma = GerenciadorPlataforma(user="root", password="")

        # Centraliza os elementos na tela
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Título e subtítulo da tela inicial
        ctk.CTkLabel(self, text="E-Learning", font=ctk.CTkFont(size=28, weight="bold")).grid(
            row=0, column=0, pady=(30, 5)
        )
        ctk.CTkLabel(self, text="Gestão de Plataforma", font=ctk.CTkFont(size=14)).grid(
            row=1, column=0, pady=(0, 20)
        )

        # Frame transparente para agrupar os 3 botões lado a lado
        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.grid(row=2, column=0, pady=10)

        # Cada botão abre a janela correspondente à entidade, passando o gerenciador compartilhado
        ctk.CTkButton(frame_botoes, text="📚  Cursos", width=100,
                      command=lambda: JanelaCursos(self, self.plataforma)).pack(side="left", padx=10)

        ctk.CTkButton(frame_botoes, text="🎓  Alunos", width=100,
                      command=lambda: JanelaAlunos(self, self.plataforma)).pack(side="left", padx=10)

        ctk.CTkButton(frame_botoes, text="👨🏫  Professores", width=100,
                      command=lambda: JanelaProfessores(self, self.plataforma)).pack(side="left", padx=10)


# Ponto de entrada do programa: inicia o loop principal da interface gráfica
if __name__ == "__main__":
    app = App()
    app.mainloop()
