""" Configurações principais da aplicação. """
import os
import sys
from pathlib import Path


def obter_uri_banco_padrao() -> str:
    """
    Define o caminho do banco SQLite de acordo com o ambiente de execução.
    Quando empacotado como executável (.exe via PyInstaller/sys.frozen),
    armazena o banco em %APPDATA%/AgendaSalao para evitar perda de dados.
    """
    if getattr(sys, "frozen", False):
        appdata = os.environ.get("APPDATA") or str(Path.home())
        pasta_dados = Path(appdata) / "AgendaSalao"
        pasta_dados.mkdir(parents=True, exist_ok=True)
        caminho_db = pasta_dados / "agenda.db"
        return f"sqlite:///{caminho_db.as_posix()}"

    return "sqlite:///agenda.db"


class Config:
    """ Classe base de configuração. """
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-secreta-desenvolvimento")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or obter_uri_banco_padrao()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """ Configuração dedicada para execução de testes automatizados em memória. """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
