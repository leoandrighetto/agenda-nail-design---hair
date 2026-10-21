""" Rotas para a gestão de modalidades dos cursos e seus recursos. """
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Modalidade, Material, Equipamento

modalidades_bp = Blueprint("modalidades", __name__)


def serializar_modalidade(modalidade):
    """ Converte um objeto Modalidade para dicionário incluindo disponibilidade de estoque. """
    materiais = [
        {
            "id": m.id,
            "nome": m.nome,
            "quantidade": m.quantidade,
            "disponivel": m.disponivel,
        }
        for m in modalidade.materiais
    ]
    equipamentos = [
        {
            "id": e.id,
            "nome": e.nome,
            "quantidade": e.quantidade,
            "disponivel": e.disponivel,
        }
        for e in modalidade.equipamentos
    ]

    materiais_ok = all(m.disponivel and m.quantidade > 0 for m in modalidade.materiais)
    equipamentos_ok = all(e.disponivel and e.quantidade > 0 for e in modalidade.equipamentos)

    return {
        "id": modalidade.id,
        "nome": modalidade.nome,
        "duracao": modalidade.duracao,
        "caracteristicas": modalidade.caracteristicas,
        "materiais": materiais,
        "equipamentos": equipamentos,
        "recursos_disponiveis": materiais_ok and equipamentos_ok,
    }


@modalidades_bp.route("", methods=["GET"])
def get_modalidades():
    """ Retorna todas as modalidades cadastradas. """
    modalidades = Modalidade.query.all()
    return jsonify([serializar_modalidade(m) for m in modalidades]), 200


@modalidades_bp.route("", methods=["POST"])
def criar_modalidade():
    """ Cria uma nova modalidade e associa materiais e equipamentos necessários. """
    dados = request.get_json()
    if not dados or not dados.get("nome"):
        return jsonify({"erro": "O nome da modalidade é obrigatório"}), 400

    nova_modalidade = Modalidade(
        nome=dados.get("nome"),
        duracao=dados.get("duracao"),
        caracteristicas=dados.get("caracteristicas"),
    )
    db.session.add(nova_modalidade)

    materiais_ids = dados.get("materiais_ids", [])
    if materiais_ids:
        nova_modalidade.materiais = Material.query.filter(Material.id.in_(materiais_ids)).all()

    equipamentos_ids = dados.get("equipamentos_ids", [])
    if equipamentos_ids:
        nova_modalidade.equipamentos = Equipamento.query.filter(Equipamento.id.in_(equipamentos_ids)).all()

    db.session.commit()

    return jsonify({"mensagem": "Modalidade criada com sucesso", "id": nova_modalidade.id}), 201


@modalidades_bp.route("/<int:modalidade_id>", methods=["GET"])
def visualizar_modalidade(modalidade_id):
    """ Retorna os dados de uma modalidade específica. """
    modalidade = db.session.get(Modalidade, modalidade_id)
    if not modalidade:
        return jsonify({"erro": "Modalidade não encontrada"}), 404

    return jsonify(serializar_modalidade(modalidade)), 200


@modalidades_bp.route("/<int:modalidade_id>", methods=["PUT"])
def atualizar_modalidade(modalidade_id):
    """ Atualiza os dados e recursos de uma modalidade existente. """
    modalidade = db.session.get(Modalidade, modalidade_id)
    if not modalidade:
        return jsonify({"erro": "Modalidade não encontrada"}), 404

    dados = request.get_json() or {}
    if dados.get("nome"):
        modalidade.nome = dados.get("nome")
    if "duracao" in dados:
        modalidade.duracao = dados.get("duracao")
    if "caracteristicas" in dados:
        modalidade.caracteristicas = dados.get("caracteristicas")

    if "materiais_ids" in dados:
        ids = dados.get("materiais_ids") or []
        modalidade.materiais = Material.query.filter(Material.id.in_(ids)).all() if ids else []

    if "equipamentos_ids" in dados:
        ids = dados.get("equipamentos_ids") or []
        modalidade.equipamentos = Equipamento.query.filter(Equipamento.id.in_(ids)).all() if ids else []

    db.session.commit()
    return jsonify({"mensagem": "Modalidade atualizada com sucesso"}), 200


@modalidades_bp.route("/<int:modalidade_id>", methods=["DELETE"])
def deletar_modalidade(modalidade_id):
    """ Deleta uma modalidade existente. """
    modalidade = db.session.get(Modalidade, modalidade_id)
    if not modalidade:
        return jsonify({"erro": "Modalidade não encontrada"}), 404

    db.session.delete(modalidade)
    db.session.commit()
    return jsonify({"mensagem": "Modalidade deletada com sucesso"}), 200
