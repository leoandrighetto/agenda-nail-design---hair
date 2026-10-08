""" Rota de status da API. """
from flask import Blueprint, jsonify

status_bp = Blueprint("status", __name__)

@status_bp.route("", methods=["GET"])
def api_status():
    """ Rota de teste para checar se a api está no ar. """
    return jsonify({"status": "ok", "mensagem": "API da Agenda de Salão rodando!"}), 200
