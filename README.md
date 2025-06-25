
# PlanIt 📅✅📝

## 📌 Sobre o Projeto

PlanIt é uma aplicação web desenvolvida com Flask que permite o gerenciamento de tarefas, notas e eventos, com integração a um calendário visual e suporte a internacionalização (i18n) com três idiomas: Português, Inglês e Espanhol.

O objetivo principal é ajudar usuários a organizar suas atividades diárias de forma simples e rápida.

---

## 🚀 Como Instalar

1. **Clone o repositório:**

```bash
git clone https://github.com/seuusuario/planit.git
cd planit
```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**

```bash
python -m venv .venv
.\.venv\Scriptsctivate
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados (SQLite):**

```bash
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

5. **Compile os arquivos de tradução (se quiser testar os idiomas):**

```bash
pybabel compile -d translations
```

6. **Execute a aplicação:**

```bash
python app.py
```

---

## 🌟 Funcionalidades Implementadas ✅

- ✅ Dashboard com Resumo (tarefas pendentes, notas e calendário)
- ✅ CRUD de Tarefas (Criar, Listar, Concluir, Excluir, Exportar PDF)
- ✅ CRUD de Notas (Criar, Listar, Excluir)
- ✅ Eventos no Calendário (Criar, Visualizar, Excluir)
- ✅ Calendário Mensal com destaque no Dia Atual
- ✅ Suporte a Internacionalização (i18n):
  - 🇧🇷 Português
  - 🇺🇸 English
  - 🇪🇸 Español
- ✅ Exportação de Tarefas em PDF
- ✅ Filtro de Tarefas por Status
- ✅ Uso de Flask-Babel / Flask-Babelex + Bootstrap 5

---

## 📝 Funcionalidades Desejadas (ToDo) ❌

- ❌ Login/Logout (Autenticação de Usuário)
- ❌ Cadastro de múltiplos usuários
- ❌ Edição de tarefas e eventos
- ❌ Notificações por e-mail
- ❌ Upload de anexos nas tarefas
- ❌ Visualização semanal no calendário
- ❌ Tema escuro / claro (Dark Mode / Light Mode)
- ❌ Deploy na nuvem (Heroku, Render, etc.)

---

## 📂 Estrutura de Pastas

```
PlanIt/
├── app.py
├── models.py
├── requirements.txt
├── translations/
├── templates/
├── static/
├── docs/              
└── README.md
```

---

## 👩‍💻 Tecnologias Utilizadas

- Python 3.11: Linguagem principal.
- Flask 2.3.2: Framework web.
- Flask-SQLAlchemy 3.1.1: ORM para gerenciamento do banco SQLite.
- Flask-Babel 3.1.0: Suporte à internacionalização.
- xhtml2pdf 0.2.17: Geração de PDFs (com from xhtml2pdf import pisa).
- SQLite: Banco de dados leve (instance/planit.db).
- Jinja2: Renderização de templates.
- Babel CLI: Ferramenta para compilar traduções (via translations.py).


