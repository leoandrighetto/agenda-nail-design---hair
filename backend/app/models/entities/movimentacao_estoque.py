""" Modelo da entidade MovimentacaoEstoque para histórico de entradas, saídas e ajustes. """
from datetime import datetime
from app.extensions import db

TIPOS_MOVIMENTACAO = ("ENTRADA", "SAIDA", "AJUSTE")


class MovimentacaoEstoque(db.Model):
    """ Registra cada entrada, baixa ou ajuste no estoque de um Material. """
    __tablename__ = "movimentacoes_estoque"

    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey("materiais.id"), nullable=False)
    tipo_movimentacao = db.Column(
        db.Enum(*TIPOS_MOVIMENTACAO, name="tipo_movimentacao_estoque_enum"),
        nullable=False,
    )
    quantidade = db.Column(db.Numeric(10, 2), nullable=False)
    motivo = db.Column(db.String(200), nullable=True)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.now)

    material = db.relationship(
        "Material",
        backref=db.backref("movimentacoes", lazy=True, cascade="all, delete-orphan"),
    )

