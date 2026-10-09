""" Configurações principais da aplicação. """
import os

class Config:
    """ Classe base de configuração. """
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-secreta-desenvolvimento")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///agenda.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
