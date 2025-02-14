from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Definição da aplicação Flask
app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para sessões e flash messages

# Configuração do banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:353620@localhost/planit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o banco de dados com a aplicação
db = SQLAlchemy(app)

# Modelo para Usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Senha criptografada
    
    notes = db.relationship('Note', back_populates='user')
    checklists = db.relationship('Checklist', back_populates='user')
    calendar_events = db.relationship('CalendarEvent', back_populates='user')  # Referência à string "CalendarEvent"

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password  # Já deve ser criptografada

# Modelo para Notas
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='notes')  # Nome diferente para a propriedade reversa
    
    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

# Modelo para Checklists
class Checklist(db.Model):
    __tablename__ = 'checklists'
    
    id = db.Column(db.Integer, primary_key=True)  # ID único da checklist
    name = db.Column(db.String(100), nullable=False)  # Nome da checklist
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Relacionamento com o usuário
    
    user = db.relationship('User', backref=db.backref('user_checklists', lazy=True))  # Alterado para 'user_checklists'

    def __repr__(self):
        return f'<Checklist {self.name}>'
class ChecklistItem(db.Model):
    __tablename__ = 'checklist_items'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)  # O item da checklist
    checked = db.Column(db.Boolean, default=False)  # Define se está marcado ou não
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Relacionamento com usuário

    user = db.relationship('User', backref=db.backref('checklist_items', lazy=True))

    def __repr__(self):
        return f'<ChecklistItem {self.content}>'
    
# Modelo para CalendarEvent
class CalendarEvent(db.Model):
    __tablename__ = 'calendar_events'
    
    id = db.Column(db.Integer, primary_key=True)  # ID do evento
    title = db.Column(db.String(100), nullable=False)  # Título do evento
    description = db.Column(db.String(255))  # Descrição do evento
    date = db.Column(db.DateTime, nullable=False)  # Data e hora do evento
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Relacionamento com o usuário

    user = db.relationship('User', backref=db.backref('user_calendar_events', lazy=True))  # Alterado para 'user_calendar_events'

    def __repr__(self):
        return f'<Calendar Event {self.title}>'


# Cria o banco de dados e as tabelas
with app.app_context():
    db.create_all()

# Rota para cadastro
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Verifica se o e-mail já está cadastrado
    if User.query.filter_by(email=email).first():
        flash('E-mail já cadastrado.', 'danger')
        return redirect(url_for('login'))  # Redireciona para a página de login se e-mail já existe

    
    hashed_password = generate_password_hash(password)

    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    flash('Cadastro realizado com sucesso! Faça login.', 'success')
    return redirect(url_for('login'))  # Redireciona para a página de login após o cadastro

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():  
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash(f'Bem-vindo, {user.name}!', 'success')
            return redirect(url_for('calendar'))  # Redireciona para a página calendar após login bem-sucedido

        flash('Credenciais inválidas. Tente novamente.', 'danger')

    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

@app.route('/save_note', methods=['POST'])
def save_note():
    # Lógica para salvar a nota
    title = request.form['title']
    content = request.form['content']
    user_id = session.get('user_id')

    # Criação de uma nova nota
    new_note = Note(title=title, content=content, user_id=user_id)
    db.session.add(new_note)
    db.session.commit()

    flash('Nota salva com sucesso!', 'success')
    return redirect(url_for('notes'))  # Redireciona para a página de notas

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get(note_id)
    
    if note and note.user_id != session['user_id']:  # Verifica se a nota pertence ao usuário logado
        flash('Você não tem permissão para editar esta nota.', 'danger')
        return redirect(url_for('notes'))  # Redireciona para a página de notas

    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        flash('Nota editada com sucesso!', 'success')
        return redirect(url_for('notes'))
    
    return render_template('edit_note.html', note=note)

@app.route('/delete_note/<int:note_id>', methods=['GET', 'POST'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    
    if note and note.user_id != session['user_id']:  # Verifica se a nota pertence ao usuário logado
        flash('Você não tem permissão para excluir esta nota.', 'danger')
        return redirect(url_for('notes'))  # Redireciona para a página de notas
    
    if note:
        db.session.delete(note)
        db.session.commit()
        flash('Nota excluída com sucesso!', 'success')
    else:
        flash('Nota não encontrada!', 'danger')
    
    return redirect(url_for('notes'))

# Rota para exibir o calendário
@app.route('/calendar')
def calendar():
    if 'user_id' not in session:
        flash('Faça login para acessar esta página.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    # Recuperar eventos do usuário no banco de dados
    events = CalendarEvent.query.filter_by(user_id=user_id).all()
    
    calendar_events = []
    for event in events:
        calendar_events.append({
            'title': event.title,
            'start': event.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': event.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'description': event.description,
        })

    return render_template('calendar.html', events=calendar_events)

@app.route('/notes')
def notes():
    if 'user_id' not in session:
        flash('Faça login para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    notes = Note.query.filter_by(user_id=user_id).all()  # Somente as notas do usuário logado
    return render_template('notes.html', user_name=session['user_name'], notes=notes)

@app.route('/checklist')
def checklist():
    if 'user_id' not in session:
        flash('Faça login para acessar esta página.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('checklist.html', user_name=session['user_name'])

if __name__ == '__main__':
    app.run(debug=True)
