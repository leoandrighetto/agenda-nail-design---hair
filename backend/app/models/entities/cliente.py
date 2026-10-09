""" Modelo da entidade Cliente. """
from app.extensions import db

class Cliente(db.Model):
    """ Entidade cliente. """
    __tablename__ = "clientes"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(14), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    endereco = db.Column(db.String(200), nullable=True)
