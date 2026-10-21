""" Rotas para a gestão de cursos, matrículas de alunos e vínculo de modalidades. """
from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Curso, Pessoa, Modalidade, Matricula

cursos_bp = Blueprint("cursos", __name__)


def _sincronizar_matriculas_curso(curso: Curso, alunos_ids: list[int]):
    """ Sincroniza matrículas de um curso caso uma lista de IDs de alunos seja enviada. """
    alunos_validos = (
        Pessoa.query.filter(Pessoa.id.in_(alunos_ids), Pessoa.eh_aluno.is_(True)).all()
        if alunos_ids
        else []
    )
    ids_desejados = {a.id for a in alunos_validos}
    matriculas_atuais = {m.aluno_id: m for m in curso.matriculas}

    # Remove matrículas que saíram da lista
    for aluno_id, mat in list(matriculas_atuais.items()):
        if aluno_id not in ids_desejados:
            db.session.delete(mat)

    # Cria matrículas para novos alunos adicionados
    for aluno in alunos_validos:
        if aluno.id not in matriculas_atuais:
            nova_mat = Matricula(
                aluno_id=aluno.id,
                curso_id=curso.id,
                valor_acordado=float(curso.valor_total),
                horas_realizadas=0,
                status="EM_ANDAMENTO",
            )
            db.session.add(nova_mat)


def serializar_curso(curso: Curso) -> dict:
    """ Converte um objeto Curso para dicionário incluindo modalidades e matrículas. """
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
        "matriculas": [
            {
                "id": m.id,
                "aluno_id": m.aluno_id,
                "aluno_nome": m.aluno.nome if m.aluno else None,
                "horas_realizadas": m.horas_realizadas,
                "valor_acordado": float(m.valor_acordado) if m.valor_acordado is not None else 0.0,
                "status": m.status,
            }
            for m in curso.matriculas
        ],
        "modalidades": [{"id": m.id, "nome": m.nome} for m in curso.modalidades],
    }


@cursos_bp.route("", methods=["GET"])
def get_cursos():
    """ Retorna todos os cursos cadastrados. """
    cursos = Curso.query.all()
    return jsonify([serializar_curso(c) for c in cursos]), 200


@cursos_bp.route("", methods=["POST"])
def criar_curso():
    """ Cria um novo curso no catálogo e vincula alunos (via Matrícula) e modalidades se informados. """
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
    db.session.flush()

    alunos_ids = dados.get("alunos_ids", [])
    if alunos_ids:
        _sincronizar_matriculas_curso(novo_curso, alunos_ids)

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
    """ Atualiza os dados e vínculos de um curso existente. """
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
        _sincronizar_matriculas_curso(curso, ids)

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
