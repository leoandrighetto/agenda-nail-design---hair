""" Rotas para a gestão de alunos. """
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Aluno

alunos_bp = Blueprint("alunos", __name__)


def serializar_aluno(aluno):
    """ Converte um objeto Aluno para dicionário. """
    return {
        "id": aluno.id,
        "nome": aluno.nome,
        "telefone": aluno.telefone,
        "cpf": aluno.cpf,
        "email": aluno.email,
        "endereco": aluno.endereco,
        "matricula": aluno.matricula,
        "cursos": [{"id": c.id, "nome": c.nome} for c in aluno.cursos],
    }


@alunos_bp.route("", methods=["GET"])
def get_alunos():
    """ Retorna todos os alunos cadastrados. """
    alunos = Aluno.query.all()
    return jsonify([serializar_aluno(a) for a in alunos]), 200


@alunos_bp.route("", methods=["POST"])
def criar_aluno():
    """ Cria um novo aluno. Nome, telefone e matrícula são obrigatórios. """
    dados = request.get_json()
    if not dados or not dados.get("nome") or not dados.get("telefone") or not dados.get("matricula"):
        return jsonify({"erro": "Nome, telefone e matrícula são obrigatórios"}), 400

    # verifica se já existe aluno com a mesma matrícula
    if Aluno.query.filter_by(matricula=dados.get("matricula")).first():
        return jsonify({"erro": "Já existe um aluno com esta matrícula"}), 400

    novo_aluno = Aluno(
        nome=dados.get("nome"),
        telefone=dados.get("telefone"),
        cpf=dados.get("cpf") or None,
        email=dados.get("email") or None,
        endereco=dados.get("endereco"),
        matricula=dados.get("matricula"),
    )
    db.session.add(novo_aluno)
    db.session.commit()

    return jsonify({"mensagem": "Aluno criado com sucesso", "id": novo_aluno.id}), 201


@alunos_bp.route("/<int:aluno_id>", methods=["GET"])
def visualizar_aluno(aluno_id):
    """ Retorna os dados de um aluno específico. """
    aluno = db.session.get(Aluno, aluno_id)
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    return jsonify(serializar_aluno(aluno)), 200


@alunos_bp.route("/<int:aluno_id>", methods=["PUT"])
def atualizar_aluno(aluno_id):
    """ Atualiza os dados de um aluno existente. """
    aluno = db.session.get(Aluno, aluno_id)
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    dados = request.get_json() or {}
    if dados.get("nome"):
        aluno.nome = dados.get("nome")
    if dados.get("telefone"):
        aluno.telefone = dados.get("telefone")
    if "cpf" in dados:
        aluno.cpf = dados.get("cpf") or None
    if "email" in dados:
        aluno.email = dados.get("email") or None
    if "endereco" in dados:
        aluno.endereco = dados.get("endereco")
    if dados.get("matricula"):
        aluno.matricula = dados.get("matricula")

    db.session.commit()
    return jsonify({"mensagem": "Aluno atualizado com sucesso"}), 200


@alunos_bp.route("/<int:aluno_id>", methods=["DELETE"])
def deletar_aluno(aluno_id):
    """ Deleta um aluno existente. """
    aluno = db.session.get(Aluno, aluno_id)
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    db.session.delete(aluno)
    db.session.commit()
    return jsonify({"mensagem": "Aluno deletado com sucesso"}), 200

