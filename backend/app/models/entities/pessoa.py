""" Modelo da entidade base Pessoa utilizando herança de tabelas. """
from app.extensions import db


class Pessoa(db.Model):
    """ Entidade base que armazena os dados comuns de pessoas no sistema. """
    __tablename__ = "pessoas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    endereco = db.Column(db.Text, nullable=True)
    tipo_pessoa = db.Column(db.String(50), nullable=False)

    # configura o polimorfismo para diferenciar as classes filhas
    __mapper_args__ = {
        "polymorphic_on": tipo_pessoa,
        "polymorphic_identity": "pessoa",
    }

