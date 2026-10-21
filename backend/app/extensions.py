""" Instanciação das extensões do flask e configuração de pragmas do SQLite. """
import sqlite3
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
cors = CORS()
migrate = Migrate()


@event.listens_for(Engine, "connect")
def configurar_sqlite_pragma(dbapi_connection, _connection_record):
    """
    Ativa chaves estrangeiras (FOREIGN KEY) e modo WAL para conexões SQLite,
    garantindo integridade referencial e melhor concorrência em desktop.
    """
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        # ativa WAL apenas quando não for banco em memória
        try:
            db_list = cursor.execute("PRAGMA database_list;").fetchall()
            arquivo_db = db_list[0][2] if db_list else ""
            if arquivo_db:
                cursor.execute("PRAGMA journal_mode=WAL;")
                cursor.execute("PRAGMA synchronous=NORMAL;")
        except sqlite3.Error:
            pass
        finally:
            cursor.close()
