""" Rotas para a gestão de materiais, unidades de medida e controle/movimentação de estoque. """
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Material, MovimentacaoEstoque, UNIDADES_MEDIDA, TIPOS_MOVIMENTACAO

materiais_bp = Blueprint("materiais", __name__)


def serializar_material(material: Material) -> dict:
    """ Converte um objeto Material para dicionário. """
    return {
        "id": material.id,
        "nome": material.nome,
        "descricao": material.descricao,
        "quantidade": float(material.quantidade) if material.quantidade is not None else 0.0,
        "unidade_medida": material.unidade_medida,
        "estoque_minimo": float(material.estoque_minimo) if material.estoque_minimo is not None else 0.0,
        "custo_unitario": float(material.custo_unitario) if material.custo_unitario is not None else None,
        "disponivel": material.disponivel,
        "estoque_baixo": material.estoque_baixo,
    }


def serializar_movimentacao(mov: MovimentacaoEstoque) -> dict:
    """ Converte um objeto MovimentacaoEstoque para dicionário. """
    return {
        "id": mov.id,
        "material_id": mov.material_id,
        "material_nome": mov.material.nome if mov.material else None,
        "tipo_movimentacao": mov.tipo_movimentacao,
        "quantidade": float(mov.quantidade) if mov.quantidade is not None else 0.0,
        "motivo": mov.motivo,
        "data_hora": mov.data_hora.isoformat() if mov.data_hora else None,
    }


@materiais_bp.route("", methods=["GET"])
def get_materiais():
    """ Retorna todos os materiais cadastrados, permitindo filtrar por estoque_baixo=true. """
    materiais = Material.query.all()
    apenas_estoque_baixo = request.args.get("estoque_baixo", "").lower() in ("true", "1")
    if apenas_estoque_baixo:
        materiais = [m for m in materiais if m.estoque_baixo]
    return jsonify([serializar_material(m) for m in materiais]), 200


@materiais_bp.route("", methods=["POST"])
def criar_material():
    """ Cria um novo material no estoque com unidade de medida e estoque mínimo. """
    dados = request.get_json()
    if not dados or not dados.get("nome"):
        return jsonify({"erro": "O nome do material é obrigatório"}), 400

    unidade_medida = dados.get("unidade_medida", "un")
    if unidade_medida not in UNIDADES_MEDIDA:
        return jsonify({"erro": f"Unidade de medida inválida. Use: {', '.join(UNIDADES_MEDIDA)}"}), 400

    quantidade = float(dados.get("quantidade", 0))
    estoque_minimo = float(dados.get("estoque_minimo", 0))
    custo_unitario = float(dados.get("custo_unitario")) if dados.get("custo_unitario") is not None else None
    disponivel = dados.get("disponivel", quantidade > 0)

    novo_material = Material(
        nome=dados.get("nome"),
        descricao=dados.get("descricao"),
        quantidade=quantidade,
        unidade_medida=unidade_medida,
        estoque_minimo=estoque_minimo,
        custo_unitario=custo_unitario,
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
    if "unidade_medida" in dados and dados.get("unidade_medida"):
        if dados.get("unidade_medida") not in UNIDADES_MEDIDA:
            return jsonify({"erro": f"Unidade de medida inválida. Use: {', '.join(UNIDADES_MEDIDA)}"}), 400
        material.unidade_medida = dados.get("unidade_medida")
    if "quantidade" in dados and dados.get("quantidade") is not None:
        material.quantidade = float(dados.get("quantidade"))
    if "estoque_minimo" in dados and dados.get("estoque_minimo") is not None:
        material.estoque_minimo = float(dados.get("estoque_minimo"))
    if "custo_unitario" in dados:
        val = dados.get("custo_unitario")
        material.custo_unitario = float(val) if val is not None else None
    if "disponivel" in dados and dados.get("disponivel") is not None:
        material.disponivel = bool(dados.get("disponivel"))

    db.session.commit()
    return jsonify({"mensagem": "Material atualizado com sucesso"}), 200


@materiais_bp.route("/<int:material_id>/movimentar", methods=["POST"])
def movimentar_estoque(material_id):
    """
    Registra uma movimentação de estoque (ENTRADA, SAIDA ou AJUSTE),
    atualizando automaticamente o saldo do material e sua disponibilidade.
    """
    material = db.session.get(Material, material_id)
    if not material:
        return jsonify({"erro": "Material não encontrado"}), 404

    dados = request.get_json() or {}
    tipo = dados.get("tipo_movimentacao")
    if tipo not in TIPOS_MOVIMENTACAO:
        return jsonify({"erro": f"Tipo de movimentação inválido. Use: {', '.join(TIPOS_MOVIMENTACAO)}"}), 400

    if dados.get("quantidade") is None or float(dados.get("quantidade")) <= 0:
        return jsonify({"erro": "A quantidade movimentada deve ser maior que zero"}), 400

    qtd_mov = float(dados.get("quantidade"))
    saldo_atual = float(material.quantidade or 0)

    if tipo == "ENTRADA":
        novo_saldo = saldo_atual + qtd_mov
    elif tipo == "SAIDA":
        if qtd_mov > saldo_atual:
            return jsonify({"erro": "Saldo insuficiente em estoque para realizar esta saída"}), 400
        novo_saldo = saldo_atual - qtd_mov
    else:  # AJUSTE define diretamente o novo saldo
        novo_saldo = qtd_mov

    material.quantidade = novo_saldo
    material.disponivel = novo_saldo > 0

    mov = MovimentacaoEstoque(
        material_id=material.id,
        tipo_movimentacao=tipo,
        quantidade=qtd_mov,
        motivo=dados.get("motivo"),
    )
    db.session.add(mov)
    db.session.commit()

    return jsonify({
        "mensagem": "Movimentação de estoque registrada com sucesso",
        "movimentacao_id": mov.id,
        "saldo_atual": float(material.quantidade),
        "estoque_baixo": material.estoque_baixo,
    }), 201


@materiais_bp.route("/<int:material_id>/movimentacoes", methods=["GET"])
def listar_movimentacoes_material(material_id):
    """ Retorna o histórico de movimentações de um material específico. """
    material = db.session.get(Material, material_id)
    if not material:
        return jsonify({"erro": "Material não encontrado"}), 404

    return jsonify([serializar_movimentacao(m) for m in material.movimentacoes]), 200


@materiais_bp.route("/<int:material_id>", methods=["DELETE"])
def deletar_material(material_id):
    """ Deleta um material existente. """
    material = db.session.get(Material, material_id)
    if not material:
        return jsonify({"erro": "Material não encontrado"}), 404

    db.session.delete(material)
    db.session.commit()
    return jsonify({"mensagem": "Material deletado com sucesso"}), 200
