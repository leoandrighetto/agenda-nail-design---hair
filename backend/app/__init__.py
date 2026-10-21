""" Factory de inicialização do app flask. """
from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from .core.config import Config
from .extensions import db, cors, migrate


def _traduzir_erro_integridade(err: IntegrityError) -> str:
    """ Extrai uma mensagem amigável para violações de integridade do banco. """
    msg_original = str(getattr(err, "orig", err)).lower()
    if "unique constraint failed" in msg_original:
        if "cpf" in msg_original:
            return "Já existe um cadastro com este CPF."
        if "email" in msg_original:
            return "Já existe um cadastro com este e-mail."
        if "matricula" in msg_original:
            return "Já existe um aluno com esta matrícula."
        return "Registro duplicado: um dos campos únicos informados já está cadastrado."
    if "foreign key constraint failed" in msg_original or (
        "not null constraint failed" in msg_original and request.method == "DELETE"
    ):
        return "Operação não permitida pois este registro está vinculado a outros dados do sistema."
    if "not null constraint failed" in msg_original:
        return "Um campo obrigatório não foi preenchido corretamente."
    return "Violação de integridade no banco de dados."


def create_app(config_class=Config):
    """ Cria e configura a aplicação flask. """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # inicializa as extensões
    db.init_app(app)
    cors.init_app(app)

    # importa os modelos para que o SQLAlchemy e o Flask-Migrate reconheçam o metadado
    from . import models  # noqa: F401
    migrate.init_app(app, db, render_as_batch=True)

    # registra handlers globais para evitar erros 500 por falhas de banco de dados
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(err):
        db.session.rollback()
        return jsonify({"erro": _traduzir_erro_integridade(err)}), 400

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(_err):
        db.session.rollback()
        return jsonify({"erro": "Erro interno ao processar operação no banco de dados."}), 500

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

    # cria as tabelas automaticamente apenas em ambiente de teste em memória
    if app.config.get("TESTING"):
        with app.app_context():
            db.create_all()

    return app
