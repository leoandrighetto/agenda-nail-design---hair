""" Rotas para a gestão de equipamentos do salão. """
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Equipamento

equipamentos_bp = Blueprint("equipamentos", __name__)


def serializar_equipamento(equipamento):
    """ Converte um objeto Equipamento para dicionário. """
    return {
        "id": equipamento.id,
        "nome": equipamento.nome,
        "descricao": equipamento.descricao,
        "quantidade": equipamento.quantidade,
        "disponivel": equipamento.disponivel,
    }


@equipamentos_bp.route("", methods=["GET"])
def get_equipamentos():
    """ Retorna todos os equipamentos cadastrados. """
    equipamentos = Equipamento.query.all()
    return jsonify([serializar_equipamento(e) for e in equipamentos]), 200


@equipamentos_bp.route("", methods=["POST"])
def criar_equipamento():
    """ Cria um novo equipamento. """
    dados = request.get_json()
    if not dados or not dados.get("nome"):
        return jsonify({"erro": "O nome do equipamento é obrigatório"}), 400

    quantidade = dados.get("quantidade", 1)
    disponivel = dados.get("disponivel", quantidade > 0 if quantidade is not None else True)

    novo_equipamento = Equipamento(
        nome=dados.get("nome"),
        descricao=dados.get("descricao"),
        quantidade=quantidade,
        disponivel=bool(disponivel),
    )
    db.session.add(novo_equipamento)
    db.session.commit()

    return jsonify({"mensagem": "Equipamento criado com sucesso", "id": novo_equipamento.id}), 201


@equipamentos_bp.route("/<int:equipamento_id>", methods=["GET"])
def visualizar_equipamento(equipamento_id):
    """ Retorna os dados de um equipamento específico. """
    equipamento = db.session.get(Equipamento, equipamento_id)
    if not equipamento:
        return jsonify({"erro": "Equipamento não encontrado"}), 404

    return jsonify(serializar_equipamento(equipamento)), 200


@equipamentos_bp.route("/<int:equipamento_id>", methods=["PUT"])
def atualizar_equipamento(equipamento_id):
    """ Atualiza os dados de um equipamento existente. """
    equipamento = db.session.get(Equipamento, equipamento_id)
    if not equipamento:
        return jsonify({"erro": "Equipamento não encontrado"}), 404

    dados = request.get_json() or {}
    if dados.get("nome"):
        equipamento.nome = dados.get("nome")
    if "descricao" in dados:
        equipamento.descricao = dados.get("descricao")
    if "quantidade" in dados and dados.get("quantidade") is not None:
        equipamento.quantidade = dados.get("quantidade")
    if "disponivel" in dados and dados.get("disponivel") is not None:
        equipamento.disponivel = bool(dados.get("disponivel"))

    db.session.commit()
    return jsonify({"mensagem": "Equipamento atualizado com sucesso"}), 200


@equipamentos_bp.route("/<int:equipamento_id>", methods=["DELETE"])
def deletar_equipamento(equipamento_id):
    """ Deleta um equipamento existente. """
    equipamento = db.session.get(Equipamento, equipamento_id)
    if not equipamento:
        return jsonify({"erro": "Equipamento não encontrado"}), 404

    db.session.delete(equipamento)
    db.session.commit()
    return jsonify({"mensagem": "Equipamento deletado com sucesso"}), 200

