""" Modelo da entidade Equipamento para controle de ferramentas e aparelhos do salão. """
from app.extensions import db


class Equipamento(db.Model):
    """ Entidade que representa os equipamentos utilizados em serviços e modalidades. """
    __tablename__ = "equipamentos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    disponivel = db.Column(db.Boolean, nullable=False, default=True)

