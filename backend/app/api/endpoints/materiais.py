""" Rotas para a gestão de materiais e controle de estoque. """
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Material

materiais_bp = Blueprint("materiais", __name__)


def serializar_material(material):
    """ Converte um objeto Material para dicionário. """
    return {
        "id": material.id,
        "nome": material.nome,
        "descricao": material.descricao,
        "quantidade": material.quantidade,
        "disponivel": material.disponivel,
    }


@materiais_bp.route("", methods=["GET"])
def get_materiais():
    """ Retorna todos os materiais cadastrados. """
    materiais = Material.query.all()
    return jsonify([serializar_material(m) for m in materiais]), 200


@materiais_bp.route("", methods=["POST"])
def criar_material():
    """ Cria um novo material no estoque. """
    dados = request.get_json()
    if not dados or not dados.get("nome"):
        return jsonify({"erro": "O nome do material é obrigatório"}), 400

    quantidade = dados.get("quantidade", 0)
    # define disponibilidade padrão de acordo com a quantidade informada se não enviada
    disponivel = dados.get("disponivel", quantidade > 0 if quantidade is not None else True)

    novo_material = Material(
        nome=dados.get("nome"),
        descricao=dados.get("descricao"),
        quantidade=quantidade,
        disponivel=bool(disponivel),
    )
    db.session.add(novo_material)
    db.session.commit()

    return jsonify({"mensagem": "Material criado com sucesso", "id": novo_material.id}), 201


@materiais_bp.route("/<int:material_id>", methods=["GET"])
def visualizar_material(material_id):
    """ Retorna os dados de um material específico. """
    material = db.session.get(Material, material_id)
    if not material:
        return jsonify({"erro": "Material não encontrado"}), 404

    return jsonify(serializar_material(material)), 200


@materiais_bp.route("/<int:material_id>", methods=["PUT"])
def atualizar_material(material_id):
    """ Atualiza os dados de um material existente. """
    material = db.session.get(Material, material_id)
    if not material:
        return jsonify({"erro": "Material não encontrado"}), 404

    dados = request.get_json() or {}
    if dados.get("nome"):
        material.nome = dados.get("nome")
    if "descricao" in dados:
        material.descricao = dados.get("descricao")
    if "quantidade" in dados and dados.get("quantidade") is not None:
        material.quantidade = dados.get("quantidade")
    if "disponivel" in dados and dados.get("disponivel") is not None:
        material.disponivel = bool(dados.get("disponivel"))

    db.session.commit()
    return jsonify({"mensagem": "Material atualizado com sucesso"}), 200


@materiais_bp.route("/<int:material_id>", methods=["DELETE"])
def deletar_material(material_id):
    """ Deleta um material existente. """
    material = db.session.get(Material, material_id)
    if not material:
        return jsonify({"erro": "Material não encontrado"}), 404

    db.session.delete(material)
    db.session.commit()
    return jsonify({"mensagem": "Material deletado com sucesso"}), 200

