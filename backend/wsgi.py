""" Ponto de entrada do servidor web. """
from pathlib import Path
from flask_migrate import upgrade
from app import create_app
from app.extensions import db

app = create_app()


def inicializar_banco_dados():
    """ Aplica migrações pendentes automaticamente ao iniciar o servidor/executável. """
    pasta_migrations = Path(__file__).resolve().parent / "migrations"
    with app.app_context():
        if pasta_migrations.exists():
            upgrade(directory=str(pasta_migrations))
        else:
            db.create_all()


if __name__ == "__main__":
    inicializar_banco_dados()
    app.run(debug=True, port=5000)
