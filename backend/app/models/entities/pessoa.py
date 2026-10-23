""" Modelo da entidade unificada Pessoa com papéis cumulativos (Cliente e/ou Aluno). """
from app.extensions import db


class Pessoa(db.Model):
    """
    Entidade que armazena os dados de qualquer pessoa no sistema.
    Os papéis no salão são controlados pelas flags booleanas (checkboxes)
    `eh_cliente` e `eh_aluno`, permitindo que uma mesma pessoa seja
    simultaneamente cliente de procedimentos e aluna de cursos.
    """
    __tablename__ = "pessoas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    endereco = db.Column(db.Text, nullable=True)

    # flags de papéis (checkboxes ativas ou não)
    eh_cliente = db.Column(db.Boolean, nullable=False, default=False, server_default=db.text("0"))
    eh_aluno = db.Column(db.Boolean, nullable=False, default=False, server_default=db.text("0"))

    # código de matrícula (preenchido quando eh_aluno=True)
    matricula = db.Column(db.String(50), nullable=True)

    __table_args__ = (
        db.UniqueConstraint("matricula", name="uq_pessoas_matricula"),
    )

    @property
    def cursos(self):
        """ Retorna os cursos nos quais a pessoa possui matrícula vinculada. """
        return [m.curso for m in getattr(self, "matriculas", []) if m.curso is not None]
