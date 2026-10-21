""" Modelo da entidade Matricula que vincula uma Aluna (Pessoa) a um Curso. """
from datetime import date
from app.extensions import db

STATUS_MATRICULA = ("EM_ANDAMENTO", "CONCLUIDO", "CANCELADO", "TRANCADO")


class Matricula(db.Model):
    """
    Entidade associativa rica entre Pessoa (Aluna) e Curso.
    Permite que um mesmo Curso do catálogo seja reutilizado para diversas alunas
    em momentos diferentes, controlando individualmente horas cumpridas,
    valor negociado, status de conclusão e pagamentos.
    """
    __tablename__ = "matriculas"

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("pessoas.id"), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey("cursos.id"), nullable=False)

    horas_realizadas = db.Column(db.Integer, nullable=False, default=0)
    valor_acordado = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(
        db.Enum(*STATUS_MATRICULA, name="status_matricula_enum"),
        nullable=False,
        default="EM_ANDAMENTO",
    )
    data_matricula = db.Column(db.Date, nullable=False, default=date.today)
    data_conclusao = db.Column(db.Date, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    aluno = db.relationship(
        "Pessoa",
        backref=db.backref("matriculas", lazy=True, cascade="all, delete-orphan"),
    )
    curso = db.relationship(
        "Curso",
        backref=db.backref("matriculas", lazy=True, cascade="all, delete-orphan"),
    )
