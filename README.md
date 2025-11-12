# PlanIt 

O **PlanIt** é uma aplicação web desenvolvida em **Python (Flask)** para ajudar na **organização pessoal**.  
O sistema permite gerenciar **tarefas, anotações e eventos**, tudo integrado em uma interface simples e funcional.

---

## Funcionalidades

- **Autenticação de usuários**
  - Cadastro e login com senhas criptografadas
  - Sessões seguras com `Flask-Session`

- **Calendário**
  - Exibe eventos salvos pelo usuário
  - Armazena as informações no banco de dados
  - Redireciona usuários não autenticados para login

- **Notas**
  - Criação, edição e exclusão de notas pessoais
  - Cada nota é vinculada ao usuário autenticado

- **Checklist**
  - Criação e marcação de itens (tarefas concluídas ou pendentes)
  - Exclusão de itens diretamente na interface
  - Comunicação com o backend via JSON (AJAX)

---

## Tecnologias Utilizadas

- **Python 3.11+**
- **Flask**
- **Flask SQLAlchemy**
- **Werkzeug Security**
- **HTML5, CSS3 e JavaScript**
- **Bootstrap (opcional, para layout)**

---

## Como Executar o Projeto

### Clonar o repositório
```bash
git clone https://github.com/LuizaaQueiroz/planit
cd planit
```

### Criar e ativar o ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
```

### Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Executar o servidor Flask
```bash
flask run
```
