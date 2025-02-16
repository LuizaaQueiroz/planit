#arquivo para criar e configurar o flask dinamicamente
from flask import Flask
from config import Config
from .extensions import db  

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # inicializa o banco de dados
    db.init_app(app)

    # registra Blueprints
    from .routes.auth import auth_bp
    from .routes.notes import notes_bp
    from .routes.checklist import checklist_bp
    from .routes.calendar import calendar_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(calendar_bp, url_prefix='/calendar')
    app.register_blueprint(notes_bp, url_prefix='/notes')
    app.register_blueprint(checklist_bp, url_prefix='/checklist')
    
    return app