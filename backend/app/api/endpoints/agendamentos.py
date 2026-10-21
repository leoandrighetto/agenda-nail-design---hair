""" Rotas para a gestão de agendamentos do salão. """
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Agendamento, Cliente, Servico

agendamentos_bp = Blueprint("agendamentos", __name__)


def converter_data_hora(valor_str):
    """ Converte string ISO (YYYY-MM-DDTHH:MM ou YYYY-MM-DD HH:MM) para datetime. """
    if not valor_str:
        return None
    return datetime.fromisoformat(valor_str)


def serializar_agendamento(agendamento):
    """ Converte um objeto Agendamento para dicionário. """
    return {
        "id": agendamento.id,
        "data_hora_inicio": agendamento.data_hora_inicio.isoformat() if agendamento.data_hora_inicio else None,
        "data_hora_fim": agendamento.data_hora_fim.isoformat() if agendamento.data_hora_fim else None,
        "status": agendamento.status,
        "cliente_id": agendamento.cliente_id,
        "cliente_nome": agendamento.cliente.nome if agendamento.cliente else None,
        "servico_id": agendamento.servico_id,
        "servico_nome": agendamento.servico.nome if agendamento.servico else None,
    }


@agendamentos_bp.route("", methods=["GET"])
def get_agendamentos():
    """ Retorna todos os agendamentos cadastrados. """
    agendamentos = Agendamento.query.all()
    return jsonify([serializar_agendamento(a) for a in agendamentos]), 200


@agendamentos_bp.route("", methods=["POST"])
def criar_agendamento():
    """ Cria um novo agendamento calculando o término com base na duração do serviço se necessário. """
    dados = request.get_json()
    if (
        not dados
        or not dados.get("cliente_id")
        or not dados.get("servico_id")
        or not dados.get("data_hora_inicio")
    ):
        return jsonify({"erro": "Cliente, serviço e data/hora de início são obrigatórios"}), 400

    cliente = db.session.get(Cliente, dados.get("cliente_id"))
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    servico = db.session.get(Servico, dados.get("servico_id"))
    if not servico:
        return jsonify({"erro": "Serviço não encontrado"}), 404

    try:
        inicio = converter_data_hora(dados.get("data_hora_inicio"))
        if dados.get("data_hora_fim"):
            fim = converter_data_hora(dados.get("data_hora_fim"))
        else:
            # calcula automaticamente o horário de término pela duração do serviço
            duracao = servico.duracao_minutos or 30
            fim = inicio + timedelta(minutes=duracao)
    except ValueError:
        return jsonify({"erro": "Formato de data/hora inválido. Use YYYY-MM-DDTHH:MM:SS"}), 400

    novo_agendamento = Agendamento(
        cliente_id=cliente.id,
        servico_id=servico.id,
        data_hora_inicio=inicio,
        data_hora_fim=fim,
        status=dados.get("status", "Pendente"),
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
    """ Atualiza os dados de um agendamento existente. """
    agendamento = db.session.get(Agendamento, agendamento_id)
    if not agendamento:
        return jsonify({"erro": "Agendamento não encontrado"}), 404

    dados = request.get_json() or {}
    if "cliente_id" in dados and dados.get("cliente_id"):
        if not db.session.get(Cliente, dados.get("cliente_id")):
            return jsonify({"erro": "Cliente não encontrado"}), 404
        agendamento.cliente_id = dados.get("cliente_id")

    if "servico_id" in dados and dados.get("servico_id"):
        if not db.session.get(Servico, dados.get("servico_id")):
            return jsonify({"erro": "Serviço não encontrado"}), 404
        agendamento.servico_id = dados.get("servico_id")

    try:
        if "data_hora_inicio" in dados and dados.get("data_hora_inicio"):
            agendamento.data_hora_inicio = converter_data_hora(dados.get("data_hora_inicio"))
        if "data_hora_fim" in dados and dados.get("data_hora_fim"):
            agendamento.data_hora_fim = converter_data_hora(dados.get("data_hora_fim"))
    except ValueError:
        return jsonify({"erro": "Formato de data/hora inválido. Use YYYY-MM-DDTHH:MM:SS"}), 400

    if "status" in dados and dados.get("status"):
        agendamento.status = dados.get("status")

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

