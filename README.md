<h1 align="center">Sistema de Gerenciamento Web & Banco de Dados Relacional</h1>

<p align="center">
  <img
    src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=20&pause=1000&color=2E9EF7&center=true&vCenter=true&width=550&lines=Barbershop+Management+System+%F0%9F%92%88;Python+%7C+Flask+%7C+SQLite3;Full+CRUD+%2B+WCAG+2.1+Accessibility;Project+under+continuous+development+%F0%9F%9A%80"
    alt="Typing SVG"
  />
</p>

---

### 📌 Sobre o Projeto

O **Barbearia Estilo & Corte** é um sistema web desenvolvido para gerenciar as operações de cadastro e controle de uma barbearia real. A aplicação permite realizar o **CRUD completo** (Cadastrar, Listar, Editar e Excluir) para profissionais (**Barbeiros**) e **Serviços**, resolvendo a relação **N:M (Muitos-para-Muitos)** entre eles por meio de uma tabela associativa no banco de dados.

Este projeto foi desenvolvido focando nos princípios de **desenvolvimento web com Flask**, **modelagem de banco de dados relacional (3FN)** e **acessibilidade digital (WCAG 2.1 - Nível AA)**.

> 🚀 **Evolução do Projeto:** Esta aplicação passará por **implementações contínuas ao longo do ano**, integrando novos recursos de negócios, otimizações no backend e aprimoramentos de interface.

---

### 🧠 Lógica e Arquitetura do Sistema

#### 1. Solução do Relacionamento $N:M$
No modelo de negócio da barbearia, **um barbeiro pode realizar vários serviços** e **um serviço pode ser prestado por vários barbeiros**.
- A associação é gerenciada através de uma tabela pivô (`barbeiro_servico`) no arquivo `barbershop.db`.
- O banco utiliza restrições de chave estrangeira com `ON DELETE CASCADE`. Ou seja, ao excluir um barbeiro ou serviço, os seus vínculos são removidos automaticamente.
- Para garantir a integridade no SQLite3, ativa-se o comando `PRAGMA foreign_keys = ON;` nas conexões.

#### 2. Consulta SQL Otimizada (`GROUP_CONCAT`)
Para exibir a lista de profissionais e seus respectivos serviços sem multiplicar linhas nem sobrecarregar o banco com consultas desnecessárias:
- Utiliza-se a instrução `LEFT JOIN` junto à função de agregação `GROUP_CONCAT(s.nome_servico, ', ')`.
- Isso retorna todos os serviços de cada barbeiro agrupados em uma única string pronta para exibição no template Jinja2.

#### 3. Organização do Código
- **`app.py`**: Atua como o controlador principal da aplicação Flask, definindo as rotas HTTP, tratamento de requisições POST/GET e renderização dos templates.
- **`model.py`**: Concentra as funções de manipulação e persistência de dados junto ao SQLite3.
- **`templates/`**: Contém as páginas HTML renderizadas pelo Jinja2.

---

### ♿ Acessibilidade (WCAG 2.1 - Nível AA)

A interface foi projetada e validada segundo diretrizes internacionais de acessibilidade:

- **0 Violações no axe DevTools (`forms-label`):** Rótulos (`<label>`) vinculados explicitamente aos seus respectivos campos de entrada (`<input>`).
- **Score 100 no Google Lighthouse (`color-contrast`):** Taxa de contraste entre texto e fundo superior a **7:1**, garantindo excelente leitura.
- **Tamanho do Alvo (`target-size`):** Elementos interativos (como *checkboxes* de serviços) possuem dimensões adequadas para toque e clique.
- **Uso Não Exclusivo da Cor (`use-of-color`):** Feedbacks de erro e sucesso utilizam suporte textual e ícones, sem depender exclusivamente de cores.
- **Responsividade (`reflow`):** Layout adaptável a telas menores através de media queries no `style.css`, sem necessidade de rolagem horizontal.

---

### 🛠️ Tecnologias Utilizadas

<p align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=py,flask,sqlite,html,css,git,github" alt="Tecnologias Utilizadas" />
  </a>
</p>

- **Linguagem Backend:** Python 3
- **Framework Web:** Flask (Jinja2)
- **Banco de Dados:** SQLite3 (`barbershop.db`)
- **Estilização e Layout:** HTML5 Semântico e CSS3 (`style.css`)
- **Auditoria de Acessibilidade:** Google Lighthouse & axe DevTools

---

### 📂 Estrutura do Repositório

```text
CRUD---Barber-shop/
├── static/
│   ├── css/
│   │   └── style.css            # Estilos visuais e regras de acessibilidade
│   └── img/
│       └── barbearia.jfif       # Imagens do sistema
├── templates/
│   ├── index.html               # Página inicial do sistema
│   ├── barbeiro.html            # Listagem e cadastro de barbeiros
│   ├── editar_barbeiro.html     # Formulário de edição de barbeiro
│   ├── servico.html             # Listagem e cadastro de serviços
│   └── editar_servico.html      # Formulário de edição de serviço
├── .gitignore                   # Arquivos ignorados pelo Git
├── app.py                       # Servidor Flask e gerenciamento de rotas
├── barbershop.db                # Banco de dados relacional SQLite3
├── model.py                     # Funções de banco de dados e regras de negócio
└── README.md                    # Documentação do projeto
