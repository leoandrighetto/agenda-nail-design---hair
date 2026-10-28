""" Rotas para o controle financeiro e gestão de pagamentos de cursos e matrículas. """
from datetime import date
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Pagamento, Pessoa, Curso, Matricula
from app.models.entities.pagamento import TIPOS_COBRANCA, STATUS_PAGAMENTO, FORMAS_PAGAMENTO

pagamentos_bp = Blueprint("pagamentos", __name__)


def converter_data(valor_str):
    """ Converte uma string no formato YYYY-MM-DD para objeto date. """
    if not valor_str:
        return None
    return date.fromisoformat(valor_str)


def serializar_pagamento(pagamento: Pagamento) -> dict:
    """ Converte um objeto Pagamento para dicionário incluindo indicador de atraso. """
    em_atraso = bool(
        pagamento.status == "PENDENTE"
        and pagamento.data_vencimento
        and pagamento.data_vencimento < date.today()
    )
    return {
        "id": pagamento.id,
        "aluno_id": pagamento.aluno_id,
        "aluno_nome": pagamento.aluno.nome if pagamento.aluno else None,
        "curso_id": pagamento.curso_id,
        "curso_nome": pagamento.curso.nome if pagamento.curso else None,
        "matricula_id": pagamento.matricula_id,
        "tipo_cobranca": pagamento.tipo_cobranca,
        "status": pagamento.status,
        "em_atraso": em_atraso,
        "valor_esperado": float(pagamento.valor_esperado) if pagamento.valor_esperado is not None else 0.0,
        "valor_pago": float(pagamento.valor_pago) if pagamento.valor_pago is not None else None,
        "data_vencimento": pagamento.data_vencimento.isoformat() if pagamento.data_vencimento else None,
        "data_pagamento": pagamento.data_pagamento.isoformat() if pagamento.data_pagamento else None,
        "forma_pagamento": pagamento.forma_pagamento,
    }


@pagamentos_bp.route("", methods=["GET"])
def get_pagamentos():
    """ Retorna todos os pagamentos cadastrados, permitindo filtros opcionais. """
    query = Pagamento.query
    aluno_id = request.args.get("aluno_id", type=int)
    curso_id = request.args.get("curso_id", type=int)
    matricula_id = request.args.get("matricula_id", type=int)
    status = request.args.get("status")

    if aluno_id:
        query = query.filter_by(aluno_id=aluno_id)
    if curso_id:
        query = query.filter_by(curso_id=curso_id)
    if matricula_id:
        query = query.filter_by(matricula_id=matricula_id)
    if status:
        query = query.filter_by(status=status)

    pagamentos = query.all()
    return jsonify([serializar_pagamento(p) for p in pagamentos]), 200


@pagamentos_bp.route("", methods=["POST"])
def criar_pagamento():
    """ Cria um novo lançamento de pagamento para um aluno em um curso/matrícula. """
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados de pagamento são obrigatórios"}), 400

    matricula_id = dados.get("matricula_id")
    aluno_id = dados.get("aluno_id")
    curso_id = dados.get("curso_id")

    if matricula_id:
        mat = db.session.get(Matricula, matricula_id)
        if not mat:
            return jsonify({"erro": "Matrícula não encontrada"}), 404
        aluno_id = aluno_id or mat.aluno_id
        curso_id = curso_id or mat.curso_id

    if (
        not aluno_id
        or not curso_id
        or not dados.get("tipo_cobranca")
        or dados.get("valor_esperado") is None
        or not dados.get("data_vencimento")
    ):
        return jsonify({
            "erro": "Aluno (ou matrícula), curso, tipo de cobrança, valor esperado e data de vencimento são obrigatórios"
        }), 400

    aluno = db.session.get(Pessoa, aluno_id)
    if not aluno or not aluno.eh_aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404
    if not db.session.get(Curso, curso_id):
        return jsonify({"erro": "Curso não encontrado"}), 404

    tipo_cobranca = dados.get("tipo_cobranca")
    if tipo_cobranca not in TIPOS_COBRANCA:
        return jsonify({"erro": f"Tipo de cobrança inválido. Use: {', '.join(TIPOS_COBRANCA)}"}), 400

    status = dados.get("status", "PENDENTE")
    if status not in STATUS_PAGAMENTO:
        return jsonify({"erro": f"Status inválido. Use: {', '.join(STATUS_PAGAMENTO)}"}), 400

    forma_pagamento = dados.get("forma_pagamento")
    if forma_pagamento and forma_pagamento not in FORMAS_PAGAMENTO:
        return jsonify({"erro": f"Forma de pagamento inválida. Use: {', '.join(FORMAS_PAGAMENTO)}"}), 400

    try:
        data_vencimento = converter_data(dados.get("data_vencimento"))
        data_pagamento = converter_data(dados.get("data_pagamento"))
    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use YYYY-MM-DD"}), 400

    novo_pagamento = Pagamento(
        aluno_id=aluno_id,
        curso_id=curso_id,
        matricula_id=matricula_id,
        tipo_cobranca=tipo_cobranca,
        status=status,
        valor_esperado=float(dados.get("valor_esperado")),
        valor_pago=float(dados.get("valor_pago")) if dados.get("valor_pago") is not None else None,
        data_vencimento=data_vencimento,
        data_pagamento=data_pagamento,
        forma_pagamento=forma_pagamento,
    )
    db.session.add(novo_pagamento)
    db.session.commit()

    return jsonify({"mensagem": "Pagamento criado com sucesso", "id": novo_pagamento.id}), 201


@pagamentos_bp.route("/<int:pagamento_id>", methods=["GET"])
def visualizar_pagamento(pagamento_id):
    """ Retorna os dados de um pagamento específico. """
    pagamento = db.session.get(Pagamento, pagamento_id)
    if not pagamento:
        return jsonify({"erro": "Pagamento não encontrado"}), 404

    return jsonify(serializar_pagamento(pagamento)), 200


@pagamentos_bp.route("/<int:pagamento_id>", methods=["PUT"])
def atualizar_pagamento(pagamento_id):
    """ Atualiza os dados de um pagamento existente (baixa, status, valores). """
    pagamento = db.session.get(Pagamento, pagamento_id)
    if not pagamento:
        return jsonify({"erro": "Pagamento não encontrado"}), 404

    dados = request.get_json() or {}
    if "tipo_cobranca" in dados and dados.get("tipo_cobranca"):
        if dados.get("tipo_cobranca") not in TIPOS_COBRANCA:
            return jsonify({"erro": "Tipo de cobrança inválido"}), 400
        pagamento.tipo_cobranca = dados.get("tipo_cobranca")

    if "status" in dados and dados.get("status"):
        if dados.get("status") not in STATUS_PAGAMENTO:
            return jsonify({"erro": "Status inválido"}), 400
        pagamento.status = dados.get("status")

    if "forma_pagamento" in dados:
        forma = dados.get("forma_pagamento")
        if forma and forma not in FORMAS_PAGAMENTO:
            return jsonify({"erro": "Forma de pagamento inválida"}), 400
        pagamento.forma_pagamento = forma

    if "valor_esperado" in dados and dados.get("valor_esperado") is not None:
        pagamento.valor_esperado = float(dados.get("valor_esperado"))

    if "valor_pago" in dados:
        val_pago = dados.get("valor_pago")
        pagamento.valor_pago = float(val_pago) if val_pago is not None else None

    if "matricula_id" in dados:
        pagamento.matricula_id = dados.get("matricula_id")

    try:
        if "data_vencimento" in dados and dados.get("data_vencimento"):
            pagamento.data_vencimento = converter_data(dados.get("data_vencimento"))
        if "data_pagamento" in dados:
            pagamento.data_pagamento = converter_data(dados.get("data_pagamento"))
    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use YYYY-MM-DD"}), 400

    db.session.commit()
    return jsonify({"mensagem": "Pagamento atualizado com sucesso"}), 200


@pagamentos_bp.route("/<int:pagamento_id>", methods=["DELETE"])
def deletar_pagamento(pagamento_id):
    """ Deleta um pagamento existente. """
    pagamento = db.session.get(Pagamento, pagamento_id)
    if not pagamento:
        return jsonify({"erro": "Pagamento não encontrado"}), 404

    db.session.delete(pagamento)
    db.session.commit()
    return jsonify({"mensagem": "Pagamento deletado com sucesso"}), 200
