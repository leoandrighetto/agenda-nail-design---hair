""" Modelo da entidade Modalidade associada aos cursos e seus recursos. """
from app.extensions import db

# tabela associativa entre modalidades e materiais utilizados nas aulas
modalidade_material = db.Table(
    "modalidade_material",
    db.Column("modalidade_id", db.Integer, db.ForeignKey("modalidades.id"), primary_key=True),
    db.Column("material_id", db.Integer, db.ForeignKey("materiais.id"), primary_key=True),
    db.Column(
        "quantidade_consumida",
        db.Numeric(10, 2),
        nullable=False,
        default=1,
        server_default=db.text("1"),
    ),
)

# tabela associativa entre modalidades e equipamentos utilizados nas aulas
modalidade_equipamento = db.Table(
    "modalidade_equipamento",
    db.Column("modalidade_id", db.Integer, db.ForeignKey("modalidades.id"), primary_key=True),
    db.Column("equipamento_id", db.Integer, db.ForeignKey("equipamentos.id"), primary_key=True),
)


class Modalidade(db.Model):
    """ Entidade que descreve uma modalidade de ensino dentro dos cursos. """
    __tablename__ = "modalidades"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    duracao = db.Column(db.String(50), nullable=True)
    caracteristicas = db.Column(db.Text, nullable=True)

    # relacionamentos muitos-para-muitos com materiais e equipamentos necessários
    materiais = db.relationship(
        "Material",
        secondary=modalidade_material,
        backref=db.backref("modalidades", lazy=True),
    )
    equipamentos = db.relationship(
        "Equipamento",
        secondary=modalidade_equipamento,
        backref=db.backref("modalidades", lazy=True),
    )
