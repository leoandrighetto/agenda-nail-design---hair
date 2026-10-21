"""
Testes automatizados da Etapa 1:
- Infraestrutura Flask-Migrate
- Pragmas SQLite (foreign_keys=ON e journal_mode=WAL)
- Resolução de caminho do banco para executável (sys.frozen / %APPDATA%)
- Tratamento global de IntegrityError e rollback seguro via API HTTP
"""
import sqlite3
from sqlalchemy import text
import pytest
from app import create_app
from app.core.config import TestingConfig, obter_uri_banco_padrao
from app.extensions import db


@pytest.fixture
def app():
    """ Instancia a aplicação em modo de teste em memória. """
    application = create_app(TestingConfig)
    yield application
    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """ Cliente HTTP de teste do Flask. """
    return app.test_client()


def test_status_endpoint(client):
    """ Verifica se a API responde com status 200 OK. """
    resp = client.get("/api/status")
    assert resp.status_code == 200
    dados = resp.get_json()
    assert dados["status"] == "ok"


def test_sqlite_pragma_foreign_keys_ativo(app):
    """ Garante que PRAGMA foreign_keys=ON está ativo em todas as conexões SQLite. """
    with app.app_context():
        resultado = db.session.execute(text("PRAGMA foreign_keys;")).scalar()
        assert resultado == 1


def test_sqlite_pragma_wal_em_arquivo(tmp_path):
    """ Garante que PRAGMA journal_mode=WAL é ativado quando o SQLite usa arquivo em disco. """
    db_file = tmp_path / "teste_wal.db"

    class FileConfig(TestingConfig):
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_file.as_posix()}"

    app_file = create_app(FileConfig)
    with app_file.app_context():
        modo_journal = db.session.execute(text("PRAGMA journal_mode;")).scalar()
        assert str(modo_journal).lower() == "wal"
        fk_ativo = db.session.execute(text("PRAGMA foreign_keys;")).scalar()
        assert fk_ativo == 1
        db.session.remove()
        db.engine.dispose()


def test_caminho_banco_executavel_frozen(monkeypatch, tmp_path):
    """ Verifica se em modo executável (sys.frozen=True) o banco é alocado em %APPDATA%/AgendaSalao. """
    monkeypatch.setattr("sys.frozen", True, raising=False)
    monkeypatch.setenv("APPDATA", str(tmp_path))

    uri = obter_uri_banco_padrao()
    assert "AgendaSalao/agenda.db" in uri
    assert (tmp_path / "AgendaSalao").exists()


def test_tratamento_integrity_error_cpf_e_email_duplicados(client):
    """
    Testa chamadas HTTP reais tentando duplicar CPF e E-mail:
    - Deve retornar HTTP 400 (e não 500)
    - Deve realizar rollback na sessão permitindo novas operações subsequentes
    """
    resp1 = client.post("/api/clientes", json={
        "nome": "Maria Silva",
        "telefone": "11999990001",
        "cpf": "12345678901",
        "email": "maria@exemplo.com",
    })
    assert resp1.status_code == 201

    # Tenta criar outro cliente com o mesmo CPF
    resp_cpf_dup = client.post("/api/clientes", json={
        "nome": "Joana Souza",
        "telefone": "11999990002",
        "cpf": "12345678901",
        "email": "joana@exemplo.com",
    })
    assert resp_cpf_dup.status_code == 400
    assert "CPF" in resp_cpf_dup.get_json()["erro"]

    # Tenta criar outro cliente com o mesmo E-mail
    resp_email_dup = client.post("/api/clientes", json={
        "nome": "Joana Souza",
        "telefone": "11999990002",
        "cpf": "10987654321",
        "email": "maria@exemplo.com",
    })
    assert resp_email_dup.status_code == 400
    assert "e-mail" in resp_email_dup.get_json()["erro"].lower()

    # Garante que a sessão se recuperou após o rollback automático e permite criar registro válido
    resp_valido = client.post("/api/clientes", json={
        "nome": "Joana Souza",
        "telefone": "11999990002",
        "cpf": "10987654321",
        "email": "joana@exemplo.com",
    })
    assert resp_valido.status_code == 201


def test_integridade_chave_estrangeira_ao_deletar_cliente_com_agendamento(client):
    """
    Verifica que o PRAGMA foreign_keys=ON e o handler de IntegrityError impedem
    excluir um cliente que possui agendamento vinculado (retornando 400 amigável).
    """
    c_resp = client.post("/api/clientes", json={"nome": "Cliente Com Agenda", "telefone": "11988887777"})
    cliente_id = c_resp.get_json()["id"]

    s_resp = client.post("/api/servicos", json={"nome": "Manicure Gel", "duracao_minutos": 60, "preco": 80.0})
    servico_id = s_resp.get_json()["id"]

    a_resp = client.post("/api/agendamentos", json={
        "cliente_id": cliente_id,
        "servico_id": servico_id,
        "data_hora_inicio": "2026-10-25T14:00:00",
    })
    assert a_resp.status_code == 201

    del_resp = client.delete(f"/api/clientes/{cliente_id}")
    assert del_resp.status_code == 400
    assert "vinculado" in del_resp.get_json()["erro"].lower() or "integridade" in del_resp.get_json()["erro"].lower()
