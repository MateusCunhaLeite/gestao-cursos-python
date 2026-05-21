# 📚 Sistema de Gestão de Plataforma (E-Learning)

Um sistema desktop intuitivo desenvolvido em **Python** para gerenciar o catálogo de cursos de uma plataforma de E-Learning. Este projeto foi construído como parte da avaliação acadêmica da disciplina de Estruturas Lineares, unindo conceitos teóricos de listas, tuplas e dicionários com aplicações práticas reais.

## ✨ Funcionalidades
* **Interface Gráfica Moderna:** Desenvolvida utilizando a biblioteca `CustomTkinter`.
* **Persistência de Dados (CRUD):** Conexão direta com banco de dados MySQL para Criar, Ler e Deletar cursos de forma segura.
* **Estruturas Lineares:** Uso prático de Listas e Tuplas para manipulação dos dados em memória e exibição limpa em tela.
* **Modularização:** Separação estrutural entre a lógica de banco de dados (`gerenciador.py`) e a interface do usuário (`main.py`).

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **GUI (Interface):** CustomTkinter
* **Banco de Dados:** MySQL (via XAMPP)
* **Conector:** PyMySQL

---

## 🚀 Tutorial de Instalação e Execução

Siga o passo a passo abaixo para preparar o ambiente e rodar o projeto no seu computador:

### 1. Instalação do Python e IDE
1. Baixe e instale a versão mais recente do Python para Windows em [python.org/downloads](https://www.python.org/downloads/).
   * **ATENÇÃO:** Na primeira tela do instalador, certifique-se de marcar a caixa **"Add python.exe to PATH"**.
2. Baixe e instale o editor de código Visual Studio Code em [code.visualstudio.com](https://code.visualstudio.com/).

### 2. Instalação e Configuração do MySQL (XAMPP)
1. Baixe e instale o XAMPP através de [apachefriends.org](https://www.apachefriends.org/).
2. Abra o **XAMPP Control Panel** e clique em **"Start"** nas opções **Apache** e **MySQL**. Ambos devem ficar com o fundo verde.
3. Abra o seu navegador de internet e acesse: `http://localhost/phpmyadmin/`.
4. Clique na aba **"SQL"** no menu superior, cole o script abaixo e clique em **Executar**:
   ```sql
   CREATE DATABASE plataforma_cursos;
   USE plataforma_cursos;

   CREATE TABLE cursos (
       id INT AUTO_INCREMENT PRIMARY KEY,
       nome VARCHAR(100) NOT NULL,
       categoria VARCHAR(50) NOT NULL,
       carga_horaria INT NOT NULL
   );
