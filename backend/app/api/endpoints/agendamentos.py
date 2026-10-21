""" Rotas para a gestão de agendamentos do salão (serviços/combos, aulas de cursos e bloqueios). """
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import (
    Agendamento,
    Pessoa,
    Servico,
    Curso,
    Matricula,
    TIPOS_AGENDAMENTO,
)

agendamentos_bp = Blueprint("agendamentos", __name__)

STATUS_CANCELADOS = ("Cancelado", "CANCELADO", "cancelado")


def converter_data_hora(valor_str):
    """ Converte string ISO (YYYY-MM-DDTHH:MM ou YYYY-MM-DD HH:MM) para datetime. """
    if not valor_str:
        return None
    return datetime.fromisoformat(valor_str)


def _verificar_conflito_horario(inicio: datetime, fim: datetime, ignorar_id: int | None = None):
    """
    Verifica se já existe algum agendamento ativo (não cancelado) que se sobreponha
    ao intervalo [inicio, fim).
    """
    query = Agendamento.query.filter(
        Agendamento.data_hora_inicio < fim,
        Agendamento.data_hora_fim > inicio,
        ~Agendamento.status.in_(STATUS_CANCELADOS),
    )
    if ignorar_id is not None:
        query = query.filter(Agendamento.id != ignorar_id)
    return query.first()


def _resolver_servicos_agendamento(dados: dict) -> list[Servico]:
    """ Obtém a lista de objetos Servico a partir de servicos_ids (combo) ou servico_id (único). """
    ids = []
    if dados.get("servicos_ids"):
        ids.extend(dados.get("servicos_ids"))
    if dados.get("servico_id") and dados.get("servico_id") not in ids:
        ids.append(dados.get("servico_id"))

    if not ids:
        return []

    servicos = Servico.query.filter(Servico.id.in_(ids)).all()
    if len(servicos) != len(set(ids)):
        return None  # indica que algum ID de serviço não foi encontrado
    return servicos


def serializar_agendamento(agendamento: Agendamento) -> dict:
    """ Converte um objeto Agendamento para dicionário completo. """
    lista_servicos = agendamento.servicos or ([agendamento.servico] if agendamento.servico else [])
    return {
        "id": agendamento.id,
        "tipo_agendamento": agendamento.tipo_agendamento,
        "data_hora_inicio": agendamento.data_hora_inicio.isoformat() if agendamento.data_hora_inicio else None,
        "data_hora_fim": agendamento.data_hora_fim.isoformat() if agendamento.data_hora_fim else None,
        "status": agendamento.status,
        "valor_total": float(agendamento.valor_total) if agendamento.valor_total is not None else None,
        "observacoes": agendamento.observacoes,
        "cliente_id": agendamento.cliente_id,
        "cliente_nome": agendamento.cliente.nome if agendamento.cliente else None,
        "servico_id": agendamento.servico_id,
        "servico_nome": agendamento.servico.nome if agendamento.servico else None,
        "servicos": [
            {
                "id": s.id,
                "nome": s.nome,
                "duracao_minutos": s.duracao_minutos,
                "preco": float(s.preco) if s.preco is not None else 0.0,
            }
            for s in lista_servicos
        ],
        "curso_id": agendamento.curso_id,
        "curso_nome": agendamento.curso.nome if agendamento.curso else None,
        "matricula_id": agendamento.matricula_id,
    }


@agendamentos_bp.route("", methods=["GET"])
def get_agendamentos():
    """ Retorna todos os agendamentos cadastrados, permitindo filtros opcionais. """
    query = Agendamento.query
    tipo = request.args.get("tipo_agendamento")
    cliente_id = request.args.get("cliente_id", type=int)
    curso_id = request.args.get("curso_id", type=int)

    if tipo:
        query = query.filter_by(tipo_agendamento=tipo)
    if cliente_id:
        query = query.filter_by(cliente_id=cliente_id)
    if curso_id:
        query = query.filter_by(curso_id=curso_id)

    agendamentos = query.order_by(Agendamento.data_hora_inicio.asc()).all()
    return jsonify([serializar_agendamento(a) for a in agendamentos]), 200


@agendamentos_bp.route("", methods=["POST"])
def criar_agendamento():
    """
    Cria um novo agendamento (SERVICO/combo, AULA_CURSO ou BLOQUEIO),
    calculando término, valor_total histórico e validando conflitos de horário.
    """
    dados = request.get_json()
    if not dados or not dados.get("data_hora_inicio"):
        return jsonify({"erro": "A data/hora de início é obrigatória"}), 400

    tipo_agendamento = dados.get("tipo_agendamento", "SERVICO")
    if tipo_agendamento not in TIPOS_AGENDAMENTO:
        return jsonify({"erro": f"Tipo de agendamento inválido. Use: {', '.join(TIPOS_AGENDAMENTO)}"}), 400

    try:
        inicio = converter_data_hora(dados.get("data_hora_inicio"))
        fim = converter_data_hora(dados.get("data_hora_fim")) if dados.get("data_hora_fim") else None
    except ValueError:
        return jsonify({"erro": "Formato de data/hora inválido. Use YYYY-MM-DDTHH:MM:SS"}), 400

    cliente_id = dados.get("cliente_id") or dados.get("aluno_id")
    curso_id = dados.get("curso_id")
    matricula_id = dados.get("matricula_id")
    servicos = []
    servico_principal_id = None
    valor_calculado = None

    if tipo_agendamento == "SERVICO":
        if not cliente_id:
            return jsonify({"erro": "Cliente é obrigatório para agendamento de serviço"}), 400
        cliente = db.session.get(Pessoa, cliente_id)
        if not cliente:
            return jsonify({"erro": "Cliente não encontrado"}), 404

        servicos = _resolver_servicos_agendamento(dados)
        if servicos is None:
            return jsonify({"erro": "Serviço não encontrado"}), 404
        if not servicos:
            return jsonify({"erro": "Informe ao menos um serviço (servico_id ou servicos_ids)"}), 400

        servico_principal_id = servicos[0].id
        duracao_total = sum((s.duracao_minutos or 30) for s in servicos)
        if not fim:
            fim = inicio + timedelta(minutes=duracao_total)
        valor_calculado = sum(float(s.preco or 0) for s in servicos)

    elif tipo_agendamento == "AULA_CURSO":
        if matricula_id:
            mat = db.session.get(Matricula, matricula_id)
            if not mat:
                return jsonify({"erro": "Matrícula não encontrada"}), 404
            cliente_id = cliente_id or mat.aluno_id
            curso_id = curso_id or mat.curso_id

        if not curso_id:
            return jsonify({"erro": "Curso (ou matrícula) é obrigatório para agendar uma aula"}), 400
        curso = db.session.get(Curso, curso_id)
        if not curso:
            return jsonify({"erro": "Curso não encontrado"}), 404

        if cliente_id and not db.session.get(Pessoa, cliente_id):
            return jsonify({"erro": "Aluno não encontrado"}), 404

        if not fim:
            duracao_aula_min = int(dados.get("duracao_minutos", 120))
            fim = inicio + timedelta(minutes=duracao_aula_min)

    else:  # BLOQUEIO
        if not fim:
            duracao_bloq = int(dados.get("duracao_minutos", 60))
            fim = inicio + timedelta(minutes=duracao_bloq)

    if fim <= inicio:
        return jsonify({"erro": "A data/hora de término deve ser posterior ao início"}), 400

    status = dados.get("status", "Pendente")
    if status not in STATUS_CANCELADOS:
        conflito = _verificar_conflito_horario(inicio, fim)
        if conflito:
            return jsonify({
                "erro": "Conflito de horário: já existe um agendamento ativo neste período",
                "conflito_id": conflito.id,
            }), 409

    valor_total = (
        float(dados.get("valor_total"))
        if dados.get("valor_total") is not None
        else valor_calculado
    )

    novo_agendamento = Agendamento(
        tipo_agendamento=tipo_agendamento,
        cliente_id=cliente_id,
        servico_id=servico_principal_id,
        curso_id=curso_id,
        matricula_id=matricula_id,
        servicos=servicos,
        data_hora_inicio=inicio,
        data_hora_fim=fim,
        status=status,
        valor_total=valor_total,
        observacoes=dados.get("observacoes"),
    )
    db.session.add(novo_agendamento)
    db.session.commit()

    return jsonify({"mensagem": "Agendamento criado com sucesso", "id": novo_agendamento.id}), 201


@agendamentos_bp.route("/<int:agendamento_id>", methods=["GET"])
def visualizar_agendamento(agendamento_id):
    """ Retorna os dados de um agendamento específico. """
    agendamento = db.session.get(Agendamento, agendamento_id)
    if not agendamento:
        return jsonify({"erro": "Agendamento não encontrado"}), 404

    return jsonify(serializar_agendamento(agendamento)), 200


@agendamentos_bp.route("/<int:agendamento_id>", methods=["PUT"])
def atualizar_agendamento(agendamento_id):
    """ Atualiza os dados de um agendamento existente validando conflitos de horário. """
    agendamento = db.session.get(Agendamento, agendamento_id)
    if not agendamento:
        return jsonify({"erro": "Agendamento não encontrado"}), 404

    dados = request.get_json() or {}
    if "cliente_id" in dados and dados.get("cliente_id"):
        if not db.session.get(Pessoa, dados.get("cliente_id")):
            return jsonify({"erro": "Cliente não encontrado"}), 404
        agendamento.cliente_id = dados.get("cliente_id")

    if "servico_id" in dados or "servicos_ids" in dados:
        servicos = _resolver_servicos_agendamento(dados)
        if servicos is None:
            return jsonify({"erro": "Serviço não encontrado"}), 404
        if servicos:
            agendamento.servicos = servicos
            agendamento.servico_id = servicos[0].id
            if "valor_total" not in dados:
                agendamento.valor_total = sum(float(s.preco or 0) for s in servicos)

    try:
        novo_inicio = (
            converter_data_hora(dados.get("data_hora_inicio"))
            if dados.get("data_hora_inicio")
            else agendamento.data_hora_inicio
        )
        novo_fim = (
            converter_data_hora(dados.get("data_hora_fim"))
            if dados.get("data_hora_fim")
            else agendamento.data_hora_fim
        )
    except ValueError:
        return jsonify({"erro": "Formato de data/hora inválido. Use YYYY-MM-DDTHH:MM:SS"}), 400

    if novo_fim <= novo_inicio:
        return jsonify({"erro": "A data/hora de término deve ser posterior ao início"}), 400

    novo_status = dados.get("status", agendamento.status)
    if novo_status not in STATUS_CANCELADOS:
        conflito = _verificar_conflito_horario(novo_inicio, novo_fim, ignorar_id=agendamento.id)
        if conflito:
            return jsonify({
                "erro": "Conflito de horário: já existe um agendamento ativo neste período",
                "conflito_id": conflito.id,
            }), 409

    agendamento.data_hora_inicio = novo_inicio
    agendamento.data_hora_fim = novo_fim
    agendamento.status = novo_status

    if "valor_total" in dados:
        val = dados.get("valor_total")
        agendamento.valor_total = float(val) if val is not None else None

    if "observacoes" in dados:
        agendamento.observacoes = dados.get("observacoes")

    db.session.commit()
    return jsonify({"mensagem": "Agendamento atualizado com sucesso"}), 200


@agendamentos_bp.route("/<int:agendamento_id>", methods=["DELETE"])
def deletar_agendamento(agendamento_id):
    """ Deleta um agendamento existente. """
    agendamento = db.session.get(Agendamento, agendamento_id)
    if not agendamento:
        return jsonify({"erro": "Agendamento não encontrado"}), 404

    db.session.delete(agendamento)
    db.session.commit()
    return jsonify({"mensagem": "Agendamento deletado com sucesso"}), 200
