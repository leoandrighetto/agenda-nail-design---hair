"""
Testes automatizados da Etapa 2:
- Unificação da entidade Pessoa com checkboxes/flags (eh_cliente e eh_aluno)
- Cadastro direto como Aluno (eh_aluno=True, eh_cliente=False)
- Cadastro direto como Cliente (eh_cliente=True, eh_aluno=False)
- Promoção automática de Cliente para Aluno (e vice-versa) mantendo o mesmo ID e CPF sem erro de duplicidade
- Alternância de flags via PUT e validação de unicidade de CPF, E-mail e Matrícula
"""
import pytest
from app import create_app
from app.core.config import TestingConfig
from app.extensions import db
from app.models import Pessoa


@pytest.fixture
def app():
    application = create_app(TestingConfig)
    yield application
    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_cenario_aluna_que_nunca_foi_cliente(client):
    """
    Cenário do usuário: Fulana nunca foi cliente da mãe, mas será Aluna.
    Ao cadastrar em /api/alunos, cria Pessoa com eh_aluno=True e eh_cliente=False.
    """
    resp = client.post("/api/alunos", json={
        "nome": "Fulana de Tal",
        "telefone": "11977776666",
        "cpf": "11122233344",
        "email": "fulana@curso.com",
        "matricula": "ALU-2026-001",
    })
    assert resp.status_code == 201
    aluno_id = resp.get_json()["id"]

    # Deve aparecer na listagem de alunos
    lista_alunos = client.get("/api/alunos").get_json()
    assert len(lista_alunos) == 1
    assert lista_alunos[0]["id"] == aluno_id
    assert lista_alunos[0]["eh_aluno"] is True
    assert lista_alunos[0]["eh_cliente"] is False
    assert lista_alunos[0]["matricula"] == "ALU-2026-001"

    # Não deve aparecer na listagem de clientes enquanto eh_cliente for False
    lista_clientes = client.get("/api/clientes").get_json()
    assert len(lista_clientes) == 0


def test_cliente_vira_aluna_sem_duplicar_pessoa(client, app):
    """
    Cenário: Cliente já cadastrada no salão decide fazer um curso.
    Ao cadastrar em /api/alunos com o mesmo CPF, o sistema reutiliza a mesma Pessoa
    e ativa eh_aluno=True sem erro de CPF duplicado.
    """
    resp_cli = client.post("/api/clientes", json={
        "nome": "Carla Cliente",
        "telefone": "11955554444",
        "cpf": "55566677788",
        "email": "carla@salao.com",
    })
    assert resp_cli.status_code == 201
    id_original = resp_cli.get_json()["id"]

    # Agora Carla se inscreve como aluna usando o mesmo CPF
    resp_alu = client.post("/api/alunos", json={
        "nome": "Carla Cliente",
        "telefone": "11955554444",
        "cpf": "55566677788",
        "email": "carla@salao.com",
        "matricula": "ALU-2026-002",
    })
    assert resp_alu.status_code == 201
    assert resp_alu.get_json()["id"] == id_original

    # Verifica no banco que existe apenas 1 registro em pessoas com ambas as checkboxes ativas
    with app.app_context():
        assert Pessoa.query.count() == 1
        pessoa = db.session.get(Pessoa, id_original)
        assert pessoa.eh_cliente is True
        assert pessoa.eh_aluno is True
        assert pessoa.matricula == "ALU-2026-002"

    # Deve aparecer tanto em /api/clientes quanto em /api/alunos
    assert len(client.get("/api/clientes").get_json()) == 1
    assert len(client.get("/api/alunos").get_json()) == 1


def test_aluna_vira_cliente_por_checkbox_ou_post(client):
    """
    Cenário inverso: Aluna que nunca foi cliente resolve agendar um procedimento
    ou tem a checkbox eh_cliente ativada via PUT.
    """
    resp_alu = client.post("/api/alunos", json={
        "nome": "Beatriz Aluna",
        "telefone": "11944443333",
        "cpf": "99988877766",
        "matricula": "ALU-2026-003",
    })
    id_beatriz = resp_alu.get_json()["id"]

    # Ativando checkbox eh_cliente via PUT /api/alunos/<id>
    resp_put = client.put(f"/api/alunos/{id_beatriz}", json={
        "eh_cliente": True,
    })
    assert resp_put.status_code == 200

    # Agora Beatriz aparece em /api/clientes
    detalhe_cli = client.get(f"/api/clientes/{id_beatriz}")
    assert detalhe_cli.status_code == 200
    assert detalhe_cli.get_json()["eh_cliente"] is True
    assert detalhe_cli.get_json()["eh_aluno"] is True


def test_bloqueia_matricula_duplicada(client):
    """ Garante que duas alunas distintas não podem usar o mesmo código de matrícula. """
    client.post("/api/alunos", json={
        "nome": "Aluna 1",
        "telefone": "11911112222",
        "matricula": "MAT-UNICA",
    })
    resp_dup = client.post("/api/alunos", json={
        "nome": "Aluna 2",
        "telefone": "11933334444",
        "matricula": "MAT-UNICA",
    })
    assert resp_dup.status_code == 400
    assert "matrícula" in resp_dup.get_json()["erro"].lower()
