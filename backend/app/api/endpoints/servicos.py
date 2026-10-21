""" Rotas para a gestão de serviços e verificação de recursos necessários. """
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Servico, Material, Equipamento

servicos_bp = Blueprint("servicos", __name__)


def serializar_servico(servico):
    """ Converte um objeto Servico para dicionário incluindo disponibilidade de estoque. """
    materiais = [
        {
            "id": m.id,
            "nome": m.nome,
            "quantidade": m.quantidade,
            "disponivel": m.disponivel,
        }
        for m in servico.materiais
    ]
    equipamentos = [
        {
            "id": e.id,
            "nome": e.nome,
            "quantidade": e.quantidade,
            "disponivel": e.disponivel,
        }
        for e in servico.equipamentos
    ]

    # verifica se todos os materiais e equipamentos associados estão disponíveis
    materiais_ok = all(m.disponivel and m.quantidade > 0 for m in servico.materiais)
    equipamentos_ok = all(e.disponivel and e.quantidade > 0 for e in servico.equipamentos)

    return {
        "id": servico.id,
        "nome": servico.nome,
        "descricao": servico.descricao,
        "duracao_minutos": servico.duracao_minutos,
        "preco": float(servico.preco) if servico.preco is not None else None,
        "materiais": materiais,
        "equipamentos": equipamentos,
        "recursos_disponiveis": materiais_ok and equipamentos_ok,
    }


@servicos_bp.route("", methods=["GET"])
def get_servicos():
    """ Retorna todos os serviços cadastrados. """
    servicos = Servico.query.all()
    return jsonify([serializar_servico(s) for s in servicos]), 200


@servicos_bp.route("", methods=["POST"])
def criar_servico():
    """ Cria um novo serviço e associa materiais e equipamentos necessários. """
    dados = request.get_json()
    if not dados or not dados.get("nome"):
        return jsonify({"erro": "O nome do serviço é obrigatório"}), 400

    novo_servico = Servico(
        nome=dados.get("nome"),
        descricao=dados.get("descricao"),
        duracao_minutos=dados.get("duracao_minutos", 30),
        preco=float(dados.get("preco")) if dados.get("preco") is not None else None,
    )
    db.session.add(novo_servico)

    # associa os materiais enviados por id
    materiais_ids = dados.get("materiais_ids", [])
    if materiais_ids:
        novo_servico.materiais = Material.query.filter(Material.id.in_(materiais_ids)).all()

    # associa os equipamentos enviados por id
    equipamentos_ids = dados.get("equipamentos_ids", [])
    if equipamentos_ids:
        novo_servico.equipamentos = Equipamento.query.filter(Equipamento.id.in_(equipamentos_ids)).all()

    db.session.commit()

    return jsonify({"mensagem": "Serviço criado com sucesso", "id": novo_servico.id}), 201


@servicos_bp.route("/<int:servico_id>", methods=["GET"])
def visualizar_servico(servico_id):
    """ Retorna os dados detalhados de um serviço específico. """
    servico = db.session.get(Servico, servico_id)
    if not servico:
        return jsonify({"erro": "Serviço não encontrado"}), 404

    return jsonify(serializar_servico(servico)), 200


@servicos_bp.route("/<int:servico_id>", methods=["PUT"])
def atualizar_servico(servico_id):
    """ Atualiza os dados e recursos de um serviço existente. """
    servico = db.session.get(Servico, servico_id)
    if not servico:
        return jsonify({"erro": "Serviço não encontrado"}), 404

    dados = request.get_json() or {}
    if dados.get("nome"):
        servico.nome = dados.get("nome")
    if "descricao" in dados:
        servico.descricao = dados.get("descricao")
    if "duracao_minutos" in dados and dados.get("duracao_minutos") is not None:
        servico.duracao_minutos = dados.get("duracao_minutos")
    if "preco" in dados:
        servico.preco = float(dados.get("preco")) if dados.get("preco") is not None else None

    if "materiais_ids" in dados:
        ids = dados.get("materiais_ids") or []
        servico.materiais = Material.query.filter(Material.id.in_(ids)).all() if ids else []

    if "equipamentos_ids" in dados:
        ids = dados.get("equipamentos_ids") or []
        servico.equipamentos = Equipamento.query.filter(Equipamento.id.in_(ids)).all() if ids else []

    db.session.commit()
    return jsonify({"mensagem": "Serviço atualizado com sucesso"}), 200


@servicos_bp.route("/<int:servico_id>", methods=["DELETE"])
def deletar_servico(servico_id):
    """ Deleta um serviço existente. """
    servico = db.session.get(Servico, servico_id)
    if not servico:
        return jsonify({"erro": "Serviço não encontrado"}), 404

    db.session.delete(servico)
    db.session.commit()
    return jsonify({"mensagem": "Serviço deletado com sucesso"}), 200
