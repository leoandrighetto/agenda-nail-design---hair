""" Rotas para a gestão de clientes. """
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Cliente

clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("", methods=["GET"])
def get_clientes():
    """ Retorna todos os clientes. """
    clientes = Cliente.query.all()
    resultado = [{
        "id": c.id, 
        "nome": c.nome, 
        "telefone": c.telefone,
        "cpf": c.cpf,
        "email": c.email,
        "endereco": c.endereco
    } for c in clientes]
    return jsonify(resultado), 200

@clientes_bp.route("", methods=["POST"])
def criar_cliente():
    """ Cria um novo cliente. Nome e telefone são obrigatórios. """
    dados = request.get_json()
    if not dados or not dados.get("nome") or not dados.get("telefone"):
        return jsonify({"erro": "Nome e telefone são obrigatórios"}), 400
    
    novo_cliente = Cliente(
        nome=dados.get("nome"),
        telefone=dados.get("telefone"),
        cpf=dados.get("cpf") or None,
        email=dados.get("email") or None,
        endereco=dados.get("endereco")
    )
    db.session.add(novo_cliente)
    db.session.commit()
    
    return jsonify({"mensagem": "Cliente criado com sucesso", "id": novo_cliente.id}), 201


@clientes_bp.route("/<int:cliente_id>", methods=["GET"])
def visualizar_cliente(cliente_id):
    """ Retorna os dados de um cliente específico. """
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    return jsonify({
        "id": cliente.id,
        "nome": cliente.nome,
        "telefone": cliente.telefone,
        "cpf": cliente.cpf,
        "email": cliente.email,
        "endereco": cliente.endereco
    }), 200

@clientes_bp.route("/<int:cliente_id>", methods=["PUT"])
def atualizar_cliente(cliente_id):
    """ Atualiza os dados de um cliente existente. """
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
        
    dados = request.get_json()
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
        
    db.session.commit()
    return jsonify({"mensagem": "Cliente atualizado com sucesso"}), 200

@clientes_bp.route("/<int:cliente_id>", methods=["DELETE"])
def deletar_cliente(cliente_id):
    """ Deleta um cliente existente. """
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
        
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensagem": "Cliente deletado com sucesso"}), 200
