""" Definição das entidades do sistema de agendamento. """
from app.extensions import db

class Cliente(db.Model):
    """ Entidade cliente. """
    __tablename__ = "clientes"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)

class Servico(db.Model):
    """ Entidade serviço oferecido pelo salão. """
    __tablename__ = "servicos"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=True)

class Agendamento(db.Model):
    """ Entidade agendamento, unindo cliente, serviço e horário. """
    __tablename__ = "agendamentos"
    
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="Pendente")
    
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey("servicos.id"), nullable=False)
    
    cliente = db.relationship("Cliente", backref=db.backref("agendamentos", lazy=True))
    servico = db.relationship("Servico", backref=db.backref("agendamentos", lazy=True))
