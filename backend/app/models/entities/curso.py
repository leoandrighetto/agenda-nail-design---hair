""" Modelo da entidade Curso e suas tabelas associativas com alunos (Pessoa) e modalidades. """
from app.extensions import db

# tabela intermediária do relacionamento muitos-para-muitos entre cursos e alunos (pessoas)
curso_aluno = db.Table(
    "curso_aluno",
    db.Column("curso_id", db.Integer, db.ForeignKey("cursos.id"), primary_key=True),
    db.Column("aluno_id", db.Integer, db.ForeignKey("pessoas.id"), primary_key=True),
)

# tabela intermediária do relacionamento muitos-para-muitos entre cursos e modalidades
curso_modalidade = db.Table(
    "curso_modalidade",
    db.Column("curso_id", db.Integer, db.ForeignKey("cursos.id"), primary_key=True),
    db.Column("modalidade_id", db.Integer, db.ForeignKey("modalidades.id"), primary_key=True),
)


class Curso(db.Model):
    """ Entidade curso oferecido pelo salão, com controle de carga horária e matrículas. """
    __tablename__ = "cursos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    numero_aulas = db.Column(db.Integer, nullable=False)
    duracao_no_dia = db.Column(db.String(50), nullable=True)
    carga_horaria_total = db.Column(db.Integer, nullable=False)
    horas_realizadas = db.Column(db.Integer, nullable=False, default=0)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)

    # relacionamentos muitos-para-muitos com alunos e modalidades
    alunos = db.relationship(
        "Pessoa",
        secondary=curso_aluno,
        backref=db.backref("cursos", lazy=True),
    )
    modalidades = db.relationship(
        "Modalidade",
        secondary=curso_modalidade,
        backref=db.backref("cursos", lazy=True),
    )
