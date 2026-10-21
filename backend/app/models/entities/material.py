""" Modelo da entidade Material para controle de insumos, unidades de medida e estoque mínimo. """
from app.extensions import db

UNIDADES_MEDIDA = ("un", "ml", "g", "kg", "l", "cx", "par", "pct", "frasco", "rolo")


class Material(db.Model):
    """ Entidade que representa os materiais consumíveis utilizados em serviços e modalidades. """
    __tablename__ = "materiais"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    quantidade = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    unidade_medida = db.Column(
        db.String(20),
        nullable=False,
        default="un",
        server_default=db.text("'un'"),
    )
    estoque_minimo = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0,
        server_default=db.text("0"),
    )
    custo_unitario = db.Column(db.Numeric(10, 2), nullable=True)
    disponivel = db.Column(db.Boolean, nullable=False, default=True)

    @property
    def estoque_baixo(self) -> bool:
        """ Indica se o saldo atual atingiu ou ficou abaixo do estoque mínimo configurado. """
        qtd = float(self.quantidade or 0)
        minimo = float(self.estoque_minimo or 0)
        return qtd <= minimo
