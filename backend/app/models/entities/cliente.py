""" Modelo da entidade Cliente herdando de Pessoa. """
from app.extensions import db
from .pessoa import Pessoa


class Cliente(Pessoa):
    """ Entidade cliente do salão, associada à tabela base de pessoas. """
    __tablename__ = "clientes"

    id = db.Column(db.Integer, db.ForeignKey("pessoas.id"), primary_key=True)

    # define a identidade polimórfica para registros de clientes
    __mapper_args__ = {
        "polymorphic_identity": "cliente",
    }

