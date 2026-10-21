""" Modelo da entidade Agendamento. """
from app.extensions import db


class Agendamento(db.Model):
    """ Entidade agendamento, unindo cliente (Pessoa), serviço e horário. """
    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)
    data_hora_inicio = db.Column(db.DateTime, nullable=False)
    data_hora_fim = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="Pendente")

    cliente_id = db.Column(db.Integer, db.ForeignKey("pessoas.id"), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey("servicos.id"), nullable=False)

    cliente = db.relationship("Pessoa", backref=db.backref("agendamentos", lazy=True))
    servico = db.relationship("Servico", backref=db.backref("agendamentos", lazy=True))
