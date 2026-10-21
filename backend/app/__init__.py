""" Factory de inicialização do app flask. """
from flask import Flask
from .core.config import Config
from .extensions import db, cors

def create_app(config_class=Config):
    """ Cria e configura a aplicação flask. """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # inicializa as extensões
    db.init_app(app)
    cors.init_app(app)

    # registra os blueprints modularizados
    from .api.endpoints.status import status_bp
    from .api.endpoints.clientes import clientes_bp
    from .api.endpoints.alunos import alunos_bp
    from .api.endpoints.materiais import materiais_bp
    from .api.endpoints.equipamentos import equipamentos_bp
    from .api.endpoints.servicos import servicos_bp
    from .api.endpoints.modalidades import modalidades_bp
    from .api.endpoints.cursos import cursos_bp
    from .api.endpoints.pagamentos import pagamentos_bp
    from .api.endpoints.agendamentos import agendamentos_bp

    app.register_blueprint(status_bp, url_prefix="/api/status")
    app.register_blueprint(clientes_bp, url_prefix="/api/clientes")
    app.register_blueprint(alunos_bp, url_prefix="/api/alunos")
    app.register_blueprint(materiais_bp, url_prefix="/api/materiais")
    app.register_blueprint(equipamentos_bp, url_prefix="/api/equipamentos")
    app.register_blueprint(servicos_bp, url_prefix="/api/servicos")
    app.register_blueprint(modalidades_bp, url_prefix="/api/modalidades")
    app.register_blueprint(cursos_bp, url_prefix="/api/cursos")
    app.register_blueprint(pagamentos_bp, url_prefix="/api/pagamentos")
    app.register_blueprint(agendamentos_bp, url_prefix="/api/agendamentos")

    # cria as tabelas do banco de dados (apenas para desenvolvimento inicial)
    with app.app_context():
        db.create_all()

    return app
