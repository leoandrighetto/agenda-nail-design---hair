""" Modelo da entidade Material para controle de insumos e estoque. """
from app.extensions import db


class Material(db.Model):
    """ Entidade que representa os materiais consumíveis utilizados em serviços e modalidades. """
    __tablename__ = "materiais"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    disponivel = db.Column(db.Boolean, nullable=False, default=True)

