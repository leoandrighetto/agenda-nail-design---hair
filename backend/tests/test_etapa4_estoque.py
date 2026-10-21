"""
Testes automatizados da Etapa 4:
- Unidades de medida (ml, g, un, par, cx, etc.), estoque_minimo e custo_unitario em Material
- Alerta automático de estoque_baixo e filtro GET /api/materiais?estoque_baixo=true
- Movimentação de estoque (ENTRADA, SAIDA, AJUSTE), bloqueio de saldo negativo e histórico
- Impacto automático da baixa de estoque na disponibilidade de Serviços e Modalidades
"""
import pytest
from app import create_app
from app.core.config import TestingConfig
from app.extensions import db


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


def test_cadastro_materiais_unidades_medida_e_alerta_estoque_baixo(client):
    """ Testa cadastro com unidades de medida (ml, cx), estoque mínimo e filtro de reposição. """
    # Gel Construtor em gramas (saldo 30g, mínimo 10g -> estoque_baixo=False)
    r1 = client.post("/api/materiais", json={
        "nome": "Gel Construtor Nude",
        "quantidade": 30.0,
        "unidade_medida": "g",
        "estoque_minimo": 10.0,
        "custo_unitario": 45.90,
    })
    assert r1.status_code == 201
    id_gel = r1.get_json()["id"]

    # Prep Bactericida em ml (saldo 50ml, mínimo 100ml -> estoque_baixo=True)
    r2 = client.post("/api/materiais", json={
        "nome": "Prep Spray Antisséptico",
        "quantidade": 50.0,
        "unidade_medida": "ml",
        "estoque_minimo": 100.0,
        "custo_unitario": 22.50,
    })
    assert r2.status_code == 201
    id_prep = r2.get_json()["id"]

    # Unidade de medida inválida deve retornar 400
    r_inv = client.post("/api/materiais", json={
        "nome": "Material Inválido",
        "unidade_medida": "tonelada",
    })
    assert r_inv.status_code == 400

    # Filtra apenas materiais com estoque baixo
    baixos = client.get("/api/materiais?estoque_baixo=true").get_json()
    assert len(baixos) == 1
    assert baixos[0]["id"] == id_prep
    assert baixos[0]["estoque_baixo"] is True

    gel_detalhe = client.get(f"/api/materiais/{id_gel}").get_json()
    assert gel_detalhe["estoque_baixo"] is False
    assert gel_detalhe["unidade_medida"] == "g"
    assert gel_detalhe["custo_unitario"] == 45.9


def test_movimentacao_estoque_entrada_saida_e_impacto_em_servico(client):
    """
    Testa entradas e saídas de estoque, bloqueio de saldo negativo, histórico de
    movimentações e atualização de recursos_disponiveis no Serviço vinculado.
    """
    mat_id = client.post("/api/materiais", json={
        "nome": "Lixa Banana 100/180",
        "quantidade": 5,
        "unidade_medida": "un",
        "estoque_minimo": 3,
    }).get_json()["id"]

    serv_id = client.post("/api/servicos", json={
        "nome": "Manutenção Fibra",
        "duracao_minutos": 90,
        "preco": 130.00,
        "materiais_ids": [mat_id],
    }).get_json()["id"]

    # Inicialmente o serviço tem recursos disponíveis
    assert client.get(f"/api/servicos/{serv_id}").get_json()["recursos_disponiveis"] is True

    # Realiza SAIDA de 3 unidades -> saldo cai para 2 (atinge estoque_minimo=3 -> estoque_baixo=True)
    mov_saida = client.post(f"/api/materiais/{mat_id}/movimentar", json={
        "tipo_movimentacao": "SAIDA",
        "quantidade": 3,
        "motivo": "Consumo nos atendimentos da semana",
    })
    assert mov_saida.status_code == 201
    dados_saida = mov_saida.get_json()
    assert dados_saida["saldo_atual"] == 2.0
    assert dados_saida["estoque_baixo"] is True

    # Tenta dar saída de 5 unidades tendo apenas 2 -> deve bloquear com 400
    mov_excesso = client.post(f"/api/materiais/{mat_id}/movimentar", json={
        "tipo_movimentacao": "SAIDA",
        "quantidade": 5,
        "motivo": "Tentativa inválida",
    })
    assert mov_excesso.status_code == 400

    # Zera o estoque dando saída das 2 unidades restantes -> disponivel vira False
    client.post(f"/api/materiais/{mat_id}/movimentar", json={
        "tipo_movimentacao": "SAIDA",
        "quantidade": 2,
        "motivo": "Fim do pacote",
    })
    assert client.get(f"/api/servicos/{serv_id}").get_json()["recursos_disponiveis"] is False

    # Registra ENTRADA de reposição de 10 unidades -> volta a ficar disponível
    mov_entrada = client.post(f"/api/materiais/{mat_id}/movimentar", json={
        "tipo_movimentacao": "ENTRADA",
        "quantidade": 10,
        "motivo": "Compra de reposição",
    })
    assert mov_entrada.status_code == 201
    assert mov_entrada.get_json()["saldo_atual"] == 10.0
    assert mov_entrada.get_json()["estoque_baixo"] is False
    assert client.get(f"/api/servicos/{serv_id}").get_json()["recursos_disponiveis"] is True

    # Verifica histórico de movimentações (3 movimentações válidas registradas)
    historico = client.get(f"/api/materiais/{mat_id}/movimentacoes").get_json()
    assert len(historico) == 3
