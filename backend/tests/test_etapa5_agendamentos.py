"""
Testes automatizados da Etapa 5:
- Agendamento com múltiplos serviços (combos), cálculo automático de duração total e valor_total
- Preservação do preço histórico (valor_total) no agendamento mesmo após reajuste na tabela servicos
- Inclusão de aulas de cursos (AULA_CURSO) e bloqueios na mesma agenda
- Detecção e bloqueio de conflito de horários (HTTP 409 Conflict) e liberação após cancelamento
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


def test_agendamento_combo_multiplos_servicos_e_preco_historico(client):
    """
    Testa agendamento de combo (2 serviços simultâneos):
    - Soma durações automaticamente (90m + 30m = 120m)
    - Soma preços automaticamente (150.00 + 50.00 = 200.00)
    - Mantém valor_total histórico caso o preço do serviço sofra reajuste futuro
    """
    cli_id = client.post("/api/clientes", json={
        "nome": "Cliente Combo",
        "telefone": "11988881111",
    }).get_json()["id"]

    s1_id = client.post("/api/servicos", json={
        "nome": "Alongamento em Gel",
        "duracao_minutos": 90,
        "preco": 150.00,
    }).get_json()["id"]

    s2_id = client.post("/api/servicos", json={
        "nome": "Pedicure Simples",
        "duracao_minutos": 30,
        "preco": 50.00,
    }).get_json()["id"]

    resp_ag = client.post("/api/agendamentos", json={
        "cliente_id": cli_id,
        "servicos_ids": [s1_id, s2_id],
        "data_hora_inicio": "2026-10-28T09:00:00",
        "observacoes": "Cliente prefere esmalte hipoalergênico.",
    })
    assert resp_ag.status_code == 201
    ag_id = resp_ag.get_json()["id"]

    detalhe = client.get(f"/api/agendamentos/{ag_id}").get_json()
    assert detalhe["data_hora_inicio"] == "2026-10-28T09:00:00"
    assert detalhe["data_hora_fim"] == "2026-10-28T11:00:00"  # +120 minutos
    assert detalhe["valor_total"] == 200.00
    assert detalhe["observacoes"] == "Cliente prefere esmalte hipoalergênico."
    assert len(detalhe["servicos"]) == 2

    # Reajusta preço do serviço s1 para R$ 190,00 no catálogo
    client.put(f"/api/servicos/{s1_id}", json={"preco": 190.00})

    # O valor_total histórico do agendamento já salvo deve permanecer R$ 200,00
    detalhe_pos_reajuste = client.get(f"/api/agendamentos/{ag_id}").get_json()
    assert detalhe_pos_reajuste["valor_total"] == 200.00


def test_aula_curso_na_agenda_e_bloqueio_de_conflito_horario(client):
    """
    Testa unificação da agenda:
    - Agenda uma AULA_CURSO das 13:00 às 17:00
    - Tenta agendar um procedimento estético às 15:00 do mesmo dia -> bloqueia com 409 Conflict
    - Cancela a aula -> permite agendar o procedimento das 15:00 normalmente
    """
    cli_id = client.post("/api/clientes", json={"nome": "Mariana", "telefone": "11977771111"}).get_json()["id"]
    alu_id = client.post("/api/alunos", json={
        "nome": "Aluna Curso",
        "telefone": "11966661111",
        "matricula": "MAT-AULA-1",
    }).get_json()["id"]

    serv_id = client.post("/api/servicos", json={
        "nome": "Esmaltação em Gel",
        "duracao_minutos": 60,
        "preco": 75.00,
    }).get_json()["id"]

    curso_id = client.post("/api/cursos", json={
        "nome": "Curso Molde F1",
        "numero_aulas": 2,
        "carga_horaria_total": 8,
        "valor_total": 800.00,
    }).get_json()["id"]

    mat_id = client.post("/api/matriculas", json={
        "aluno_id": alu_id,
        "curso_id": curso_id,
    }).get_json()["id"]

    # 1. Agenda aula do curso das 13:00 às 17:00
    resp_aula = client.post("/api/agendamentos", json={
        "tipo_agendamento": "AULA_CURSO",
        "matricula_id": mat_id,
        "data_hora_inicio": "2026-10-29T13:00:00",
        "data_hora_fim": "2026-10-29T17:00:00",
        "observacoes": "Aula prática 1 - trazer modelo.",
    })
    assert resp_aula.status_code == 201
    aula_ag_id = resp_aula.get_json()["id"]

    # 2. Tenta agendar cliente às 15:00 do mesmo dia -> Conflito 409!
    resp_conflito = client.post("/api/agendamentos", json={
        "cliente_id": cli_id,
        "servico_id": serv_id,
        "data_hora_inicio": "2026-10-29T15:00:00",
    })
    assert resp_conflito.status_code == 409
    assert resp_conflito.get_json()["conflito_id"] == aula_ag_id

    # 3. Cancela a aula de curso -> horário das 15:00 fica disponível
    client.put(f"/api/agendamentos/{aula_ag_id}", json={"status": "Cancelado"})

    resp_liberado = client.post("/api/agendamentos", json={
        "cliente_id": cli_id,
        "servico_id": serv_id,
        "data_hora_inicio": "2026-10-29T15:00:00",
    })
    assert resp_liberado.status_code == 201
