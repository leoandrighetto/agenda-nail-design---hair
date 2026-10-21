"""
Testes automatizados da Etapa 3:
- Catálogo de Curso reutilizável para múltiplas alunas via Matricula
- Controle individual de horas_realizadas, progresso_percentual, valor_acordado (desconto) e conclusão automática
- Pagamentos vinculados à Matrícula e novas formas de pagamento (DINHEIRO, CARTAO_CREDITO, etc.)
- Precisão decimal em Servico.preco (Numeric 10,2)
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


def test_reutilizacao_curso_com_multiplas_matriculas_independentes(client):
    """
    Cenário validado com o usuário:
    - Curso 'Alongamento em Fibra de Vidro (Iniciante)' (16h, R$ 1200)
    - Aluna Juliana: concluiu 16h -> status CONCLUIDO automático (100%)
    - Aluna Carla: cumpriu 4h -> status EM_ANDAMENTO (25%)
    - Aluna Beatriz: desconto negociado R$ 1000 -> valor_acordado individual preservado
    """
    resp_curso = client.post("/api/cursos", json={
        "nome": "Alongamento em Fibra de Vidro (Iniciante)",
        "numero_aulas": 4,
        "duracao_no_dia": "4 horas",
        "carga_horaria_total": 16,
        "valor_total": 1200.00,
    })
    assert resp_curso.status_code == 201
    curso_id = resp_curso.get_json()["id"]

    j_id = client.post("/api/alunos", json={"nome": "Juliana", "telefone": "11900001111", "matricula": "M-JUL"}).get_json()["id"]
    c_id = client.post("/api/alunos", json={"nome": "Carla", "telefone": "11900002222", "matricula": "M-CAR"}).get_json()["id"]
    b_id = client.post("/api/alunos", json={"nome": "Beatriz", "telefone": "11900003333", "matricula": "M-BEA"}).get_json()["id"]

    # Matrícula da Juliana (já com 16h concluídas)
    mat_j = client.post("/api/matriculas", json={
        "aluno_id": j_id,
        "curso_id": curso_id,
        "horas_realizadas": 16,
    })
    assert mat_j.status_code == 201
    mat_j_id = mat_j.get_json()["id"]

    # Matrícula da Carla (4h realizadas até agora)
    mat_c = client.post("/api/matriculas", json={
        "aluno_id": c_id,
        "curso_id": curso_id,
        "horas_realizadas": 4,
    })
    assert mat_c.status_code == 201
    mat_c_id = mat_c.get_json()["id"]

    # Matrícula da Beatriz (com desconto para R$ 1000,00)
    mat_b = client.post("/api/matriculas", json={
        "aluno_id": b_id,
        "curso_id": curso_id,
        "valor_acordado": 1000.00,
    })
    assert mat_b.status_code == 201
    mat_b_id = mat_b.get_json()["id"]

    # Verifica estado individual de cada matrícula
    dados_j = client.get(f"/api/matriculas/{mat_j_id}").get_json()
    assert dados_j["status"] == "CONCLUIDO"
    assert dados_j["progresso_percentual"] == 100.0
    assert dados_j["valor_acordado"] == 1200.0
    assert dados_j["data_conclusao"] is not None

    dados_c = client.get(f"/api/matriculas/{mat_c_id}").get_json()
    assert dados_c["status"] == "EM_ANDAMENTO"
    assert dados_c["progresso_percentual"] == 25.0
    assert dados_c["valor_acordado"] == 1200.0

    dados_b = client.get(f"/api/matriculas/{mat_b_id}").get_json()
    assert dados_b["status"] == "EM_ANDAMENTO"
    assert dados_b["progresso_percentual"] == 0.0
    assert dados_b["valor_acordado"] == 1000.0

    # Avança as horas da Carla para 16h via PUT e verifica conclusão automática
    client.put(f"/api/matriculas/{mat_c_id}", json={"horas_realizadas": 16})
    dados_c_atualizados = client.get(f"/api/matriculas/{mat_c_id}").get_json()
    assert dados_c_atualizados["status"] == "CONCLUIDO"
    assert dados_c_atualizados["progresso_percentual"] == 100.0
    assert dados_c_atualizados["data_conclusao"] is not None

    # Verifica se o curso lista todas as 3 alunas e matrículas
    dados_curso = client.get(f"/api/cursos/{curso_id}").get_json()
    assert len(dados_curso["alunos"]) == 3
    assert len(dados_curso["matriculas"]) == 3


def test_pagamento_vinculado_a_matricula_e_forma_dinheiro(client):
    """ Testa lançamento financeiro vinculado diretamente à matrícula e pago em DINHEIRO. """
    curso_id = client.post("/api/cursos", json={
        "nome": "Nail Art Avançada",
        "numero_aulas": 2,
        "carga_horaria_total": 8,
        "valor_total": 600.00,
    }).get_json()["id"]

    aluno_id = client.post("/api/alunos", json={
        "nome": "Fernanda",
        "telefone": "11912345678",
        "matricula": "M-FER",
    }).get_json()["id"]

    matricula_id = client.post("/api/matriculas", json={
        "aluno_id": aluno_id,
        "curso_id": curso_id,
        "valor_acordado": 550.00,
    }).get_json()["id"]

    # Cria pagamento informando apenas matricula_id (aluno_id e curso_id são inferidos automaticamente)
    resp_pag = client.post("/api/pagamentos", json={
        "matricula_id": matricula_id,
        "tipo_cobranca": "MATRICULA",
        "status": "PAGO",
        "valor_esperado": 550.00,
        "valor_pago": 550.00,
        "data_vencimento": "2026-10-21",
        "data_pagamento": "2026-10-21",
        "forma_pagamento": "DINHEIRO",
    })
    assert resp_pag.status_code == 201
    pag_id = resp_pag.get_json()["id"]

    dados_pag = client.get(f"/api/pagamentos/{pag_id}").get_json()
    assert dados_pag["matricula_id"] == matricula_id
    assert dados_pag["aluno_id"] == aluno_id
    assert dados_pag["curso_id"] == curso_id
    assert dados_pag["forma_pagamento"] == "DINHEIRO"
    assert dados_pag["valor_pago"] == 550.0
