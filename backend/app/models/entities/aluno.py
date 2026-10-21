""" Modelo da entidade Aluno herdando de Pessoa. """
from app.extensions import db
from .pessoa import Pessoa


class Aluno(Pessoa):
    """ Entidade aluno matriculado em cursos do salão, associada à tabela base de pessoas. """
    __tablename__ = "alunos"

    id = db.Column(db.Integer, db.ForeignKey("pessoas.id"), primary_key=True)
    matricula = db.Column(db.String(50), unique=True, nullable=False)

    # define a identidade polimórfica para registros de alunos
    __mapper_args__ = {
        "polymorphic_identity": "aluno",
    }

