""" Definição das rotas da api em blueprint. """
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.agenda import Cliente, Servico, Agendamento

api_bp = Blueprint("api", __name__)

@api_bp.route("/status", methods=["GET"])
def api_status():
    """ Rota de teste para checar se a api está no ar. """
    return jsonify({"status": "ok", "mensagem": "API da Agenda de Salão rodando!"}), 200

@api_bp.route("/clientes", methods=["GET"])
def get_clientes():
    """ Retorna todos os clientes. """
    clientes = Cliente.query.all()
    resultado = [{"id": c.id, "nome": c.nome, "telefone": c.telefone} for c in clientes]
    return jsonify(resultado), 200
