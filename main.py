# main.py
import customtkinter as ctk
import tkinter.messagebox as messagebox

# Importação do arquivo de lógica (Modularização conforme solicitado)
from gerenciador import GerenciadorPlataforma 

# Configurações globais de estilo do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")  # Tema verde adequado para plataformas de ensino

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da Janela Principal
        self.title("E-Learning: Gestão de Plataforma")
        self.geometry("750x550")
        
        # Instanciação do Objeto da classe modularizada
        # Altere o 'user' ou 'password' se a configuração do seu XAMPP for diferente
        self.plataforma = GerenciadorPlataforma(user="root", password="")

        # Configuração do Grid Principal da Janela
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # FRAME 1: Menu Lateral (Forms Main Menu)
        # ==========================================
        self.frame_menu = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.frame_menu.grid(row=0, column=0, sticky="nsew")
        self.frame_menu.grid_rowconfigure(5, weight=1)

        self.label_menu = ctk.CTkLabel(self.frame_menu, text="Menu Principal", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_menu.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_listar = ctk.CTkButton(self.frame_menu, text="Listar Cursos", command=self.mostrar_lista)
        self.btn_listar.grid(row=1, column=0, padx=20, pady=10)

        self.btn_cadastrar = ctk.CTkButton(self.frame_menu, text="Novo Curso", command=self.mostrar_cadastro)
        self.btn_cadastrar.grid(row=2, column=0, padx=20, pady=10)

        # ==========================================
        # FRAME 2: Área de Conteúdo (Demais formulários)
        # ==========================================
        self.frame_conteudo = ctk.CTkFrame(self)
        self.frame_conteudo.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.frame_conteudo.grid_columnconfigure(0, weight=1)

        # Inicializa o sistema exibindo a listagem de cursos
        self.mostrar_lista()

    # --- FUNÇÕES DE NAVEGAÇÃO ENTRE FORMULÁRIOS ---

    def limpar_conteudo(self):
        """Remove os componentes antigos do frame antes de desenhar um novo formulário."""
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

    def mostrar_lista(self):
        """Formulário 1: Exibe a lista de cursos vindos do Banco de Dados."""
        self.limpar_conteudo()
        
        lbl_titulo = ctk.CTkLabel(self.frame_conteudo, text="Cursos Disponíveis", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_titulo.grid(row=0, column=0, pady=(20, 10))

        # Recupera as Estruturas Lineares (Lista de Tuplas) do banco de dados
        cursos = self.plataforma.listar_cursos()

        texto_cursos = "ID | Nome do Curso | Categoria | Carga Horária\n"
        texto_cursos += "-"*50 + "\n"
        
        # Iteração sobre a Lista de Tuplas para formatar a exibição em texto
        for curso in cursos:
            texto_cursos += f"[{curso[0]}] {curso[1]} | {curso[2]} | {curso[3]}h\n"

        # Componente de texto para apresentar os dados na tela de forma limpa
        textbox = ctk.CTkTextbox(self.frame_conteudo, width=450, height=300)
        textbox.grid(row=1, column=0, padx=20, pady=10)
        textbox.insert("0.0", texto_cursos)
        textbox.configure(state="disabled")  # Bloqueia a edição manual por parte do usuário

        # Pequeno formulário acoplado para exclusão de registos (DELETE do CRUD)
        frame_delete = ctk.CTkFrame(self.frame_conteudo)
        frame_delete.grid(row=2, column=0, pady=10)
        
        self.entry_id_del = ctk.CTkEntry(frame_delete, placeholder_text="ID do Curso p/ Deletar")
        self.entry_id_del.pack(side="left", padx=5)
        
        btn_del = ctk.CTkButton(frame_delete, text="Deletar", fg_color="#c0392b", hover_color="#e74c3c", command=self.deletar_curso)
        btn_del.pack(side="left", padx=5)

    def mostrar_cadastro(self):
        """Formulário 2: Cadastro de Novos Cursos (CREATE do CRUD)."""
        self.limpar_conteudo()

        lbl_titulo = ctk.CTkLabel(self.frame_conteudo, text="Cadastrar Novo Curso", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_titulo.grid(row=0, column=0, pady=(20, 20))

        self.entry_nome = ctk.CTkEntry(self.frame_conteudo, placeholder_text="Nome do Curso (ex: Python para Iniciantes)", width=300)
        self.entry_nome.grid(row=1, column=0, pady=10)
        
        self.entry_categoria = ctk.CTkEntry(self.frame_conteudo, placeholder_text="Categoria (ex: Programação)", width=300)
        self.entry_categoria.grid(row=2, column=0, pady=10)

        self.entry_horas = ctk.CTkEntry(self.frame_conteudo, placeholder_text="Carga Horária (apenas números)", width=300)
        self.entry_horas.grid(row=3, column=0, pady=10)

        btn_salvar = ctk.CTkButton(self.frame_conteudo, text="Salvar Curso", command=self.salvar_curso)
        btn_salvar.grid(row=4, column=0, pady=20)

    # --- PROCESSAMENTO DOS COMANDOS DO BANCO DE DADOS ---

    def salvar_curso(self):
        nome = self.entry_nome.get()
        categoria = self.entry_categoria.get()
        horas_str = self.entry_horas.get()

        try:
            horas = int(horas_str)  # Validação para garantir que horas é um número inteiro
            if nome == "" or categoria == "":
                raise ValueError("Campos em branco.")
                
            self.plataforma.cadastrar_curso(nome, categoria, horas)
            messagebox.showinfo("Sucesso", "Curso cadastrado com sucesso!")
            self.mostrar_lista()  # Redireciona de volta para a listagem atualizada
            
        except ValueError:
            messagebox.showerror("Aviso", "Por favor, verifique se a carga horária é numérica e preencha todos os campos.")
        except Exception as e:
            messagebox.showerror("Erro de BD", f"Erro ao acessar o banco de dados: {e}")

    def deletar_curso(self):
        id_str = self.entry_id_del.get()
        try:
            id_curso = int(id_str)
            self.plataforma.deletar_curso(id_curso)
            messagebox.showinfo("Sucesso", "Curso removido com sucesso!")
            self.mostrar_lista()  # Atualiza a listagem após a remoção
        except ValueError:
            messagebox.showerror("Aviso", "Insira um número de ID válido para efetuar a exclusão.")
        except Exception as e:
            messagebox.showerror("Erro de BD", f"Erro ao aceder ao banco de dados: {e}")

# Ponto de entrada padrão do sistema Python para execução do loop da GUI
if __name__ == "__main__":
    app = App()
    app.mainloop()