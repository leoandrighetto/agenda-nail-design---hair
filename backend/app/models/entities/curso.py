""" Modelo da entidade Curso (Catálogo) e vínculo com Modalidades e Matrículas. """
from app.extensions import db

# tabela intermediária do relacionamento muitos-para-muitos entre cursos e modalidades
curso_modalidade = db.Table(
    "curso_modalidade",
    db.Column("curso_id", db.Integer, db.ForeignKey("cursos.id"), primary_key=True),
    db.Column("modalidade_id", db.Integer, db.ForeignKey("modalidades.id"), primary_key=True),
)


class Curso(db.Model):
    """ Entidade catálogo de curso oferecido pelo salão. """
    __tablename__ = "cursos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    numero_aulas = db.Column(db.Integer, nullable=False)
    duracao_no_dia = db.Column(db.String(50), nullable=True)
    carga_horaria_total = db.Column(db.Integer, nullable=False)
    horas_realizadas = db.Column(db.Integer, nullable=False, default=0)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)

    # relacionamento muitos-para-muitos com modalidades
    modalidades = db.relationship(
        "Modalidade",
        secondary=curso_modalidade,
        backref=db.backref("cursos", lazy=True),
    )

    @property
    def alunos(self):
        """ Retorna a lista de alunos inscritos neste curso através das matrículas. """
        return [m.aluno for m in getattr(self, "matriculas", []) if m.aluno is not None]
