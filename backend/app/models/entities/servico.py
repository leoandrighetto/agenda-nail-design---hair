""" Modelo da entidade Servico e seus relacionamentos com materiais e equipamentos. """
from app.extensions import db

# tabela associativa entre serviços e materiais necessários para a execução
servico_material = db.Table(
    "servico_material",
    db.Column("servico_id", db.Integer, db.ForeignKey("servicos.id"), primary_key=True),
    db.Column("material_id", db.Integer, db.ForeignKey("materiais.id"), primary_key=True),
)

# tabela associativa entre serviços e equipamentos necessários para a execução
servico_equipamento = db.Table(
    "servico_equipamento",
    db.Column("servico_id", db.Integer, db.ForeignKey("servicos.id"), primary_key=True),
    db.Column("equipamento_id", db.Integer, db.ForeignKey("equipamentos.id"), primary_key=True),
)


class Servico(db.Model):
    """ Entidade serviço oferecido pelo salão. """
    __tablename__ = "servicos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    duracao_minutos = db.Column(db.Integer, nullable=False, default=30)
    preco = db.Column(db.Numeric(10, 2), nullable=True)

    # relacionamentos muitos-para-muitos com materiais e equipamentos
    materiais = db.relationship(
        "Material",
        secondary=servico_material,
        backref=db.backref("servicos", lazy=True),
    )
    equipamentos = db.relationship(
        "Equipamento",
        secondary=servico_equipamento,
        backref=db.backref("servicos", lazy=True),
    )
