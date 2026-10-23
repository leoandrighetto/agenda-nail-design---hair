""" Rotas para a gestão de alunos (Pessoa com eh_aluno=True). """
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Pessoa

alunos_bp = Blueprint("alunos", __name__)


def serializar_aluno(aluno: Pessoa) -> dict:
    """ Converte um objeto Pessoa (perfil aluno) para dicionário. """
    return {
        "id": aluno.id,
        "nome": aluno.nome,
        "telefone": aluno.telefone,
        "cpf": aluno.cpf,
        "email": aluno.email,
        "endereco": aluno.endereco,
        "eh_cliente": aluno.eh_cliente,
        "eh_aluno": aluno.eh_aluno,
        "matricula": aluno.matricula,
        "cursos": [{"id": c.id, "nome": c.nome} for c in aluno.cursos],
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


@alunos_bp.route("", methods=["GET"])
def get_alunos():
    """ Retorna todos os alunos cadastrados (Pessoa com eh_aluno=True). """
    alunos = Pessoa.query.filter_by(eh_aluno=True).all()
    return jsonify([serializar_aluno(a) for a in alunos]), 200


@alunos_bp.route("", methods=["POST"])
def criar_aluno():
    """
    Cria um novo aluno (Pessoa com eh_aluno=True). Nome, telefone e matrícula são obrigatórios.
    Caso a pessoa já exista apenas como cliente (mesmo CPF/e-mail ou pessoa_id),
    ativa a flag eh_aluno=True e atribui a matrícula na mesma Pessoa.
    """
    dados = request.get_json()
    if not dados or not dados.get("nome") or not dados.get("telefone") or not dados.get("matricula"):
        return jsonify({"erro": "Nome, telefone e matrícula são obrigatórios"}), 400

    matricula = dados.get("matricula")
    cpf = dados.get("cpf") or None
    email = dados.get("email") or None
    pessoa_id = dados.get("pessoa_id")

    # verifica se já existe outro aluno com a mesma matrícula
    aluno_mesma_mat = Pessoa.query.filter_by(matricula=matricula).first()
    if aluno_mesma_mat:
        return jsonify({"erro": "Já existe um aluno com esta matrícula"}), 400

    pessoa_existente = _buscar_pessoa_existente(cpf, email, pessoa_id)
    if pessoa_existente and not pessoa_existente.eh_aluno:
        pessoa_existente.eh_aluno = True
        pessoa_existente.matricula = matricula
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
            "mensagem": "Cliente existente ativado também como aluno com sucesso",
            "id": pessoa_existente.id,
        }), 201

    novo_aluno = Pessoa(
        nome=dados.get("nome"),
        telefone=dados.get("telefone"),
        cpf=cpf,
        email=email,
        endereco=dados.get("endereco"),
        eh_cliente=bool(dados.get("eh_cliente", False)),
        eh_aluno=bool(dados.get("eh_aluno", True)),
        matricula=matricula,
    )
    db.session.add(novo_aluno)
    db.session.commit()

    return jsonify({"mensagem": "Aluno criado com sucesso", "id": novo_aluno.id}), 201


@alunos_bp.route("/<int:aluno_id>", methods=["GET"])
def visualizar_aluno(aluno_id):
    """ Retorna os dados de um aluno específico. """
    aluno = db.session.get(Pessoa, aluno_id)
    if not aluno or not aluno.eh_aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    return jsonify(serializar_aluno(aluno)), 200


@alunos_bp.route("/<int:aluno_id>", methods=["PUT"])
def atualizar_aluno(aluno_id):
    """ Atualiza os dados e checkboxes (eh_aluno / eh_cliente) de um aluno existente. """
    aluno = db.session.get(Pessoa, aluno_id)
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
    if "eh_cliente" in dados and dados.get("eh_cliente") is not None:
        aluno.eh_cliente = bool(dados.get("eh_cliente"))
    if "eh_aluno" in dados and dados.get("eh_aluno") is not None:
        aluno.eh_aluno = bool(dados.get("eh_aluno"))

    db.session.commit()
    return jsonify({"mensagem": "Aluno atualizado com sucesso"}), 200


@alunos_bp.route("/<int:aluno_id>", methods=["DELETE"])
def deletar_aluno(aluno_id):
    """ Deleta um aluno existente. """
    aluno = db.session.get(Pessoa, aluno_id)
    if not aluno or not aluno.eh_aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    db.session.delete(aluno)
    db.session.commit()
    return jsonify({"mensagem": "Aluno deletado com sucesso"}), 200
