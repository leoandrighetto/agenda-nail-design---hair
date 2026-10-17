""" Modelo da entidade Pagamento para controle financeiro dos cursos e alunos. """
from app.extensions import db

# opções válidas para os campos do tipo enum no banco de dados
TIPOS_COBRANCA = ("MATRICULA", "MENSALIDADE", "TAXA_EXTRA")
STATUS_PAGAMENTO = ("PENDENTE", "PAGO", "ATRASADO", "CANCELADO")
FORMAS_PAGAMENTO = ("PIX", "CARTAO", "BOLETO")


class Pagamento(db.Model):
    """ Entidade responsável por registrar cobranças e pagamentos de alunos em cursos. """
    __tablename__ = "pagamentos"

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey("cursos.id"), nullable=False)

    tipo_cobranca = db.Column(
        db.Enum(*TIPOS_COBRANCA, name="tipo_cobranca_enum"),
        nullable=False,
    )
    status = db.Column(
        db.Enum(*STATUS_PAGAMENTO, name="status_pagamento_enum"),
        nullable=False,
        default="PENDENTE",
    )

    valor_esperado = db.Column(db.Numeric(10, 2), nullable=False)
    valor_pago = db.Column(db.Numeric(10, 2), nullable=True)
    data_vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=True)

    forma_pagamento = db.Column(
        db.Enum(*FORMAS_PAGAMENTO, name="forma_pagamento_enum"),
        nullable=True,
    )

    # relacionamentos com aluno (1:N) e curso (1:N)
    aluno = db.relationship("Aluno", backref=db.backref("pagamentos", lazy=True))
    curso = db.relationship("Curso", backref=db.backref("pagamentos", lazy=True))

