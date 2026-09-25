""" Factory de inicialização do app flask. """
from flask import Flask
from .core.config import Config
from .extensions import db, cors

def create_app(config_class=Config):
    """ Cria e configura a aplicação flask. """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa as extensões
    db.init_app(app)
    cors.init_app(app)

    # Registra os blueprints
    from .api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    # Cria as tabelas do banco de dados (Apenas para desenvolvimento inicial)
    with app.app_context():
        db.create_all()

    return app
