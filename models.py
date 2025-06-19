from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """
    Modelo que representa um Usuário no sistema.

    Campos:
        id (int): Identificador único do usuário.
        username (str): Nome de usuário único.
        email (str): Email único.
        password_hash (str): Senha criptografada.
        created_at (datetime): Data de criação do usuário.
        tasks (List[Task]): Lista de tarefas relacionadas.
        notes (List[Note]): Lista de notas relacionadas.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship('Task', backref='user', lazy=True)
    notes = db.relationship('Note', backref='user', lazy=True)

    def set_password(self, password):
        """
        Define e criptografa a senha do usuário.

        Args:
            password (str): A senha em texto plano.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifica se a senha fornecida corresponde ao hash salvo.

        Args:
            password (str): A senha a ser verificada.

        Returns:
            bool: True se a senha estiver correta, False caso contrário.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        Representação textual do usuário.

        Returns:
            str: Representação em formato "<User username>".
        """
        return f'<User {self.username}>'


class Task(db.Model):
    """
    Modelo que representa uma Tarefa criada por um usuário.

    Campos:
        id (int): ID da tarefa.
        title (str): Título da tarefa.
        description (str): Descrição detalhada.
        status (str): Status atual (ex: 'Pendente', 'Concluída').
        due_date (datetime): Data limite da tarefa.
        created_at (datetime): Data de criação da tarefa.
        user_id (int): ID do usuário dono da tarefa.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pendente')
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """
        Representação textual da tarefa.

        Returns:
            str: Representação em formato "<Task title>".
        """
        return f'<Task {self.title}>'


class Note(db.Model):
    """
    Modelo que representa uma Nota criada por um usuário.

    Campos:
        id (int): ID da nota.
        content (str): Conteúdo da nota.
        created_at (datetime): Data de criação da nota.
        user_id (int): ID do usuário dono da nota.
    """

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """
        Representação textual da nota.

        Returns:
            str: Representação em formato "<Note id>".
        """
        return f'<Note {self.id}>'


class Event(db.Model):
    """
    Modelo que representa um Evento agendado pelo usuário.

    Campos:
        id (int): ID do evento.
        title (str): Título do evento.
        date (date): Data do evento.
        time (time): Hora do evento (opcional).
        user_id (int): ID do usuário dono do evento.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
