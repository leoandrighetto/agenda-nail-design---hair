""" Modelo da entidade Servico. """
from app.extensions import db

class Servico(db.Model):
    """ Entidade serviço oferecido pelo salão. """
    __tablename__ = "servicos"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    duracao_minutos = db.Column(db.Integer, nullable=False, default=30)
    preco = db.Column(db.Float, nullable=True)
