""" Rotas para a gestão de cursos, matrículas de alunos e vínculo de modalidades. """
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Curso, Aluno, Modalidade

cursos_bp = Blueprint("cursos", __name__)


def serializar_curso(curso):
    """ Converte um objeto Curso para dicionário. """
    return {
        "id": curso.id,
        "nome": curso.nome,
        "numero_aulas": curso.numero_aulas,
        "duracao_no_dia": curso.duracao_no_dia,
        "carga_horaria_total": curso.carga_horaria_total,
        "horas_realizadas": curso.horas_realizadas,
        "ativo": curso.ativo,
        "valor_total": float(curso.valor_total) if curso.valor_total is not None else 0.0,
        "alunos": [{"id": a.id, "nome": a.nome, "matricula": a.matricula} for a in curso.alunos],
        "modalidades": [{"id": m.id, "nome": m.nome} for m in curso.modalidades],
    }


@cursos_bp.route("", methods=["GET"])
def get_cursos():
    """ Retorna todos os cursos cadastrados. """
    cursos = Curso.query.all()
    return jsonify([serializar_curso(c) for c in cursos]), 200


@cursos_bp.route("", methods=["POST"])
def criar_curso():
    """ Cria um novo curso e vincula alunos e modalidades se informados. """
    dados = request.get_json()
    if (
        not dados
        or not dados.get("nome")
        or dados.get("numero_aulas") is None
        or dados.get("carga_horaria_total") is None
        or dados.get("valor_total") is None
    ):
        return jsonify({"erro": "Nome, número de aulas, carga horária total e valor total são obrigatórios"}), 400

    novo_curso = Curso(
        nome=dados.get("nome"),
        numero_aulas=int(dados.get("numero_aulas")),
        duracao_no_dia=dados.get("duracao_no_dia"),
        carga_horaria_total=int(dados.get("carga_horaria_total")),
        horas_realizadas=int(dados.get("horas_realizadas", 0)),
        ativo=bool(dados.get("ativo", True)),
        valor_total=float(dados.get("valor_total")),
    )
    db.session.add(novo_curso)

    alunos_ids = dados.get("alunos_ids", [])
    if alunos_ids:
        novo_curso.alunos = Aluno.query.filter(Aluno.id.in_(alunos_ids)).all()

    modalidades_ids = dados.get("modalidades_ids", [])
    if modalidades_ids:
        novo_curso.modalidades = Modalidade.query.filter(Modalidade.id.in_(modalidades_ids)).all()

    db.session.commit()

    return jsonify({"mensagem": "Curso criado com sucesso", "id": novo_curso.id}), 201


@cursos_bp.route("/<int:curso_id>", methods=["GET"])
def visualizar_curso(curso_id):
    """ Retorna os dados de um curso específico. """
    curso = db.session.get(Curso, curso_id)
    if not curso:
        return jsonify({"erro": "Curso não encontrado"}), 404

    return jsonify(serializar_curso(curso)), 200


@cursos_bp.route("/<int:curso_id>", methods=["PUT"])
def atualizar_curso(curso_id):
    """ Atualiza os dados, horas realizadas e vínculos de um curso existente. """
    curso = db.session.get(Curso, curso_id)
    if not curso:
        return jsonify({"erro": "Curso não encontrado"}), 404

    dados = request.get_json() or {}
    if dados.get("nome"):
        curso.nome = dados.get("nome")
    if "numero_aulas" in dados and dados.get("numero_aulas") is not None:
        curso.numero_aulas = int(dados.get("numero_aulas"))
    if "duracao_no_dia" in dados:
        curso.duracao_no_dia = dados.get("duracao_no_dia")
    if "carga_horaria_total" in dados and dados.get("carga_horaria_total") is not None:
        curso.carga_horaria_total = int(dados.get("carga_horaria_total"))
    if "horas_realizadas" in dados and dados.get("horas_realizadas") is not None:
        curso.horas_realizadas = int(dados.get("horas_realizadas"))
    if "ativo" in dados and dados.get("ativo") is not None:
        curso.ativo = bool(dados.get("ativo"))
    if "valor_total" in dados and dados.get("valor_total") is not None:
        curso.valor_total = float(dados.get("valor_total"))

    if "alunos_ids" in dados:
        ids = dados.get("alunos_ids") or []
        curso.alunos = Aluno.query.filter(Aluno.id.in_(ids)).all() if ids else []

    if "modalidades_ids" in dados:
        ids = dados.get("modalidades_ids") or []
        curso.modalidades = Modalidade.query.filter(Modalidade.id.in_(ids)).all() if ids else []

    db.session.commit()
    return jsonify({"mensagem": "Curso atualizado com sucesso"}), 200


@cursos_bp.route("/<int:curso_id>", methods=["DELETE"])
def deletar_curso(curso_id):
    """ Deleta um curso existente. """
    curso = db.session.get(Curso, curso_id)
    if not curso:
        return jsonify({"erro": "Curso não encontrado"}), 404

    db.session.delete(curso)
    db.session.commit()
    return jsonify({"mensagem": "Curso deletado com sucesso"}), 200
