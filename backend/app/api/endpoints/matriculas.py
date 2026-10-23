""" Rotas para a gestão de matrículas individuais de alunos em cursos. """
from datetime import date
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Matricula, Pessoa, Curso, STATUS_MATRICULA

matriculas_bp = Blueprint("matriculas", __name__)


def _converter_data(valor_str):
    if not valor_str:
        return None
    return date.fromisoformat(valor_str)


def serializar_matricula(mat: Matricula) -> dict:
    """ Converte um objeto Matricula para dicionário com progresso e dados do curso/aluno. """
    carga_total = mat.curso.carga_horaria_total if mat.curso else 0
    progresso_pct = (
        round(min((mat.horas_realizadas / carga_total) * 100.0, 100.0), 2)
        if carga_total > 0
        else 0.0
    )
    return {
        "id": mat.id,
        "aluno_id": mat.aluno_id,
        "aluno_nome": mat.aluno.nome if mat.aluno else None,
        "aluno_matricula": mat.aluno.matricula if mat.aluno else None,
        "curso_id": mat.curso_id,
        "curso_nome": mat.curso.nome if mat.curso else None,
        "carga_horaria_total": carga_total,
        "horas_realizadas": mat.horas_realizadas,
        "progresso_percentual": progresso_pct,
        "valor_acordado": float(mat.valor_acordado) if mat.valor_acordado is not None else 0.0,
        "status": mat.status,
        "data_matricula": mat.data_matricula.isoformat() if mat.data_matricula else None,
        "data_conclusao": mat.data_conclusao.isoformat() if mat.data_conclusao else None,
        "observacoes": mat.observacoes,
    }


@matriculas_bp.route("", methods=["GET"])
def get_matriculas():
    """ Retorna todas as matrículas cadastradas, permitindo filtros opcionais. """
    query = Matricula.query
    aluno_id = request.args.get("aluno_id", type=int)
    curso_id = request.args.get("curso_id", type=int)
    status = request.args.get("status")

    if aluno_id:
        query = query.filter_by(aluno_id=aluno_id)
    if curso_id:
        query = query.filter_by(curso_id=curso_id)
    if status:
        query = query.filter_by(status=status)

    matriculas = query.all()
    return jsonify([serializar_matricula(m) for m in matriculas]), 200


@matriculas_bp.route("", methods=["POST"])
def criar_matricula():
    """ Inscreve um aluno em um curso criando uma Matricula individualizada. """
    dados = request.get_json()
    if not dados or not dados.get("aluno_id") or not dados.get("curso_id"):
        return jsonify({"erro": "Aluno e curso são obrigatórios"}), 400

    aluno = db.session.get(Pessoa, dados.get("aluno_id"))
    if not aluno or not aluno.eh_aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    curso = db.session.get(Curso, dados.get("curso_id"))
    if not curso:
        return jsonify({"erro": "Curso não encontrado"}), 404

    status = dados.get("status", "EM_ANDAMENTO")
    if status not in STATUS_MATRICULA:
        return jsonify({"erro": f"Status inválido. Use: {', '.join(STATUS_MATRICULA)}"}), 400

    horas_realizadas = int(dados.get("horas_realizadas", 0))
    valor_acordado = (
        float(dados.get("valor_acordado"))
        if dados.get("valor_acordado") is not None
        else float(curso.valor_total)
    )

    try:
        data_matricula = _converter_data(dados.get("data_matricula")) or date.today()
        data_conclusao = _converter_data(dados.get("data_conclusao"))
    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use YYYY-MM-DD"}), 400

    if horas_realizadas >= curso.carga_horaria_total and status == "EM_ANDAMENTO":
        status = "CONCLUIDO"
        if not data_conclusao:
            data_conclusao = date.today()

    nova_matricula = Matricula(
        aluno_id=aluno.id,
        curso_id=curso.id,
        horas_realizadas=horas_realizadas,
        valor_acordado=valor_acordado,
        status=status,
        data_matricula=data_matricula,
        data_conclusao=data_conclusao,
        observacoes=dados.get("observacoes"),
    )
    db.session.add(nova_matricula)
    db.session.commit()

    return jsonify({"mensagem": "Matrícula criada com sucesso", "id": nova_matricula.id}), 201


@matriculas_bp.route("/<int:matricula_id>", methods=["GET"])
def visualizar_matricula(matricula_id):
    """ Retorna os dados de uma matrícula específica. """
    mat = db.session.get(Matricula, matricula_id)
    if not mat:
        return jsonify({"erro": "Matrícula não encontrada"}), 404

    return jsonify(serializar_matricula(mat)), 200


@matriculas_bp.route("/<int:matricula_id>", methods=["PUT"])
def atualizar_matricula(matricula_id):
    """ Atualiza progresso (horas_realizadas), valor acordado ou status de uma matrícula. """
    mat = db.session.get(Matricula, matricula_id)
    if not mat:
        return jsonify({"erro": "Matrícula não encontrada"}), 404

    dados = request.get_json() or {}
    if "horas_realizadas" in dados and dados.get("horas_realizadas") is not None:
        mat.horas_realizadas = int(dados.get("horas_realizadas"))

    if "valor_acordado" in dados and dados.get("valor_acordado") is not None:
        mat.valor_acordado = float(dados.get("valor_acordado"))

    if "status" in dados and dados.get("status"):
        if dados.get("status") not in STATUS_MATRICULA:
            return jsonify({"erro": f"Status inválido. Use: {', '.join(STATUS_MATRICULA)}"}), 400
        mat.status = dados.get("status")
    elif mat.curso and mat.horas_realizadas >= mat.curso.carga_horaria_total and mat.status == "EM_ANDAMENTO":
        mat.status = "CONCLUIDO"
        if not mat.data_conclusao:
            mat.data_conclusao = date.today()

    try:
        if "data_matricula" in dados and dados.get("data_matricula"):
            mat.data_matricula = _converter_data(dados.get("data_matricula"))
        if "data_conclusao" in dados:
            mat.data_conclusao = _converter_data(dados.get("data_conclusao"))
    except ValueError:
        return jsonify({"erro": "Formato de data inválido. Use YYYY-MM-DD"}), 400

    if "observacoes" in dados:
        mat.observacoes = dados.get("observacoes")

    db.session.commit()
    return jsonify({"mensagem": "Matrícula atualizada com sucesso"}), 200


@matriculas_bp.route("/<int:matricula_id>", methods=["DELETE"])
def deletar_matricula(matricula_id):
    """ Deleta uma matrícula existente. """
    mat = db.session.get(Matricula, matricula_id)
    if not mat:
        return jsonify({"erro": "Matrícula não encontrada"}), 404

    db.session.delete(mat)
    db.session.commit()
    return jsonify({"mensagem": "Matrícula deletada com sucesso"}), 200

