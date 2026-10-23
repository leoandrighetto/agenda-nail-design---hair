""" Rotas para a gestão de clientes (Pessoa com eh_cliente=True). """
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Pessoa

clientes_bp = Blueprint("clientes", __name__)


def serializar_cliente(pessoa: Pessoa) -> dict:
    """ Converte um objeto Pessoa (perfil cliente) para dicionário. """
    return {
        "id": pessoa.id,
        "nome": pessoa.nome,
        "telefone": pessoa.telefone,
        "cpf": pessoa.cpf,
        "email": pessoa.email,
        "endereco": pessoa.endereco,
        "eh_cliente": pessoa.eh_cliente,
        "eh_aluno": pessoa.eh_aluno,
        "matricula": pessoa.matricula,
    }


def _buscar_pessoa_existente(cpf: str | None, email: str | None, pessoa_id: int | None = None):
    """ Busca uma Pessoa existente por ID, CPF ou E-mail para evitar duplicação entre papéis. """
    if pessoa_id:
        return db.session.get(Pessoa, pessoa_id)
    if cpf:
        existente = Pessoa.query.filter_by(cpf=cpf).first()
        if existente:
            return existente
    if email:
        existente = Pessoa.query.filter_by(email=email).first()
        if existente:
            return existente
    return None


@clientes_bp.route("", methods=["GET"])
def get_clientes():
    """ Retorna todas as pessoas com a flag eh_cliente ativa. """
    clientes = Pessoa.query.filter_by(eh_cliente=True).all()
    return jsonify([serializar_cliente(c) for c in clientes]), 200


@clientes_bp.route("", methods=["POST"])
def criar_cliente():
    """
    Cria um novo cliente (Pessoa com eh_cliente=True).
    Caso a pessoa já exista apenas como aluna (mesmo CPF/e-mail ou pessoa_id),
    ativa a flag eh_cliente=True no cadastro existente.
    """
    dados = request.get_json()
    if not dados or not dados.get("nome") or not dados.get("telefone"):
        return jsonify({"erro": "Nome e telefone são obrigatórios"}), 400

    cpf = dados.get("cpf") or None
    email = dados.get("email") or None
    pessoa_id = dados.get("pessoa_id")

    pessoa_existente = _buscar_pessoa_existente(cpf, email, pessoa_id)
    if pessoa_existente and not pessoa_existente.eh_cliente:
        pessoa_existente.eh_cliente = True
        pessoa_existente.nome = dados.get("nome") or pessoa_existente.nome
        pessoa_existente.telefone = dados.get("telefone") or pessoa_existente.telefone
        if cpf:
            pessoa_existente.cpf = cpf
        if email:
            pessoa_existente.email = email
        if dados.get("endereco") is not None:
            pessoa_existente.endereco = dados.get("endereco")
        db.session.commit()
        return jsonify({
            "mensagem": "Pessoa já cadastrada (ex: aluna) ativada como cliente com sucesso",
            "id": pessoa_existente.id,
        }), 201

    novo_cliente = Pessoa(
        nome=dados.get("nome"),
        telefone=dados.get("telefone"),
        cpf=cpf,
        email=email,
        endereco=dados.get("endereco"),
        eh_cliente=bool(dados.get("eh_cliente", True)),
        eh_aluno=bool(dados.get("eh_aluno", False)),
        matricula=dados.get("matricula") or None,
    )
    db.session.add(novo_cliente)
    db.session.commit()

    return jsonify({"mensagem": "Cliente criado com sucesso", "id": novo_cliente.id}), 201


@clientes_bp.route("/<int:cliente_id>", methods=["GET"])
def visualizar_cliente(cliente_id):
    """ Retorna os dados de um cliente específico. """
    cliente = db.session.get(Pessoa, cliente_id)
    if not cliente or not cliente.eh_cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    return jsonify(serializar_cliente(cliente)), 200


@clientes_bp.route("/<int:cliente_id>", methods=["PUT"])
def atualizar_cliente(cliente_id):
    """ Atualiza os dados e checkboxes (eh_cliente / eh_aluno) de um cliente existente. """
    cliente = db.session.get(Pessoa, cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    dados = request.get_json() or {}
    if dados.get("nome"):
        cliente.nome = dados.get("nome")
    if dados.get("telefone"):
        cliente.telefone = dados.get("telefone")
    if "cpf" in dados:
        cliente.cpf = dados.get("cpf") or None
    if "email" in dados:
        cliente.email = dados.get("email") or None
    if "endereco" in dados:
        cliente.endereco = dados.get("endereco")
    if "eh_cliente" in dados and dados.get("eh_cliente") is not None:
        cliente.eh_cliente = bool(dados.get("eh_cliente"))
    if "eh_aluno" in dados and dados.get("eh_aluno") is not None:
        cliente.eh_aluno = bool(dados.get("eh_aluno"))
    if "matricula" in dados:
        cliente.matricula = dados.get("matricula") or None

    db.session.commit()
    return jsonify({"mensagem": "Cliente atualizado com sucesso"}), 200


@clientes_bp.route("/<int:cliente_id>", methods=["DELETE"])
def deletar_cliente(cliente_id):
    """ Deleta um cliente existente. """
    cliente = db.session.get(Pessoa, cliente_id)
    if not cliente or not cliente.eh_cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensagem": "Cliente deletado com sucesso"}), 200
