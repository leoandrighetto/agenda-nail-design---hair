""" Modelo da entidade Agendamento com suporte a combos de serviços, aulas de cursos e bloqueios. """
from app.extensions import db

TIPOS_AGENDAMENTO = ("SERVICO", "AULA_CURSO", "BLOQUEIO")

# tabela associativa para permitir múltiplos serviços (combos) em um mesmo agendamento
agendamento_servico = db.Table(
    "agendamento_servico",
    db.Column("agendamento_id", db.Integer, db.ForeignKey("agendamentos.id"), primary_key=True),
    db.Column("servico_id", db.Integer, db.ForeignKey("servicos.id"), primary_key=True),
)


class Agendamento(db.Model):
    """
    Entidade unificada de agenda do salão.
    Suporta procedimentos estéticos (único ou combo de serviços),
    aulas de cursos (vinculadas a Curso/Matrícula) e bloqueios de horário,
    preservando valor histórico e observações.
    """
    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)
    tipo_agendamento = db.Column(
        db.String(30),
        nullable=False,
        default="SERVICO",
        server_default=db.text("'SERVICO'"),
    )
    data_hora_inicio = db.Column(db.DateTime, nullable=False)
    data_hora_fim = db.Column(db.DateTime, nullable=False)
    status = db.Column(
        db.String(20),
        nullable=False,
        default="Pendente",
        server_default=db.text("'Pendente'"),
    )
    valor_total = db.Column(db.Numeric(10, 2), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    cliente_id = db.Column(db.Integer, db.ForeignKey("pessoas.id"), nullable=True)
    servico_id = db.Column(db.Integer, db.ForeignKey("servicos.id"), nullable=True)
    curso_id = db.Column(db.Integer, db.ForeignKey("cursos.id"), nullable=True)
    matricula_id = db.Column(db.Integer, db.ForeignKey("matriculas.id"), nullable=True)

    cliente = db.relationship(
        "Pessoa",
        backref=db.backref("agendamentos", lazy=True, passive_deletes="all"),
    )
    servico = db.relationship(
        "Servico",
        backref=db.backref("agendamentos", lazy=True, passive_deletes="all"),
    )
    curso = db.relationship(
        "Curso",
        backref=db.backref("agendamentos_aula", lazy=True, passive_deletes="all"),
    )
    matricula = db.relationship(
        "Matricula",
        backref=db.backref("agendamentos_aula", lazy=True, passive_deletes="all"),
    )

    servicos = db.relationship(
        "Servico",
        secondary=agendamento_servico,
        backref=db.backref("agendamentos_combo", lazy=True),
    )
