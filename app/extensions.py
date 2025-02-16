#criado para evitar import loops, gerencia instancia do SQLALchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()