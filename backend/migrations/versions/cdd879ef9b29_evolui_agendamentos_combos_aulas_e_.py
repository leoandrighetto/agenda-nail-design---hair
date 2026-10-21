"""evolui_agendamentos_combos_aulas_e_conflitos

Revision ID: cdd879ef9b29
Revises: f91e281d815b
Create Date: 2026-10-21 13:02:27.438614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdd879ef9b29'
down_revision = 'f91e281d815b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'agendamento_servico',
        sa.Column('agendamento_id', sa.Integer(), nullable=False),
        sa.Column('servico_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['agendamento_id'], ['agendamentos.id'], name='fk_agendamento_servico_agendamento_id'),
        sa.ForeignKeyConstraint(['servico_id'], ['servicos.id'], name='fk_agendamento_servico_servico_id'),
        sa.PrimaryKeyConstraint('agendamento_id', 'servico_id'),
    )
    with op.batch_alter_table('agendamentos', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('tipo_agendamento', sa.String(length=30), server_default=sa.text("'SERVICO'"), nullable=False)
        )
        batch_op.add_column(sa.Column('valor_total', sa.Numeric(precision=10, scale=2), nullable=True))
        batch_op.add_column(sa.Column('observacoes', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('curso_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('matricula_id', sa.Integer(), nullable=True))
        batch_op.alter_column(
            'status',
            existing_type=sa.VARCHAR(length=20),
            nullable=False,
        )
        batch_op.alter_column(
            'cliente_id',
            existing_type=sa.INTEGER(),
            nullable=True,
        )
        batch_op.alter_column(
            'servico_id',
            existing_type=sa.INTEGER(),
            nullable=True,
        )
        batch_op.create_foreign_key('fk_agendamentos_curso_id_cursos', 'cursos', ['curso_id'], ['id'])
        batch_op.create_foreign_key('fk_agendamentos_matricula_id_matriculas', 'matriculas', ['matricula_id'], ['id'])

    # Popula tabela associativa agendamento_servico para agendamentos preexistentes
    op.execute(
        "INSERT OR IGNORE INTO agendamento_servico (agendamento_id, servico_id) "
        "SELECT id, servico_id FROM agendamentos WHERE servico_id IS NOT NULL"
    )


def downgrade():
    with op.batch_alter_table('agendamentos', schema=None) as batch_op:
        batch_op.drop_constraint('fk_agendamentos_matricula_id_matriculas', type_='foreignkey')
        batch_op.drop_constraint('fk_agendamentos_curso_id_cursos', type_='foreignkey')
        batch_op.alter_column(
            'servico_id',
            existing_type=sa.INTEGER(),
            nullable=False,
        )
        batch_op.alter_column(
            'cliente_id',
            existing_type=sa.INTEGER(),
            nullable=False,
        )
        batch_op.alter_column(
            'status',
            existing_type=sa.VARCHAR(length=20),
            nullable=True,
        )
        batch_op.drop_column('matricula_id')
        batch_op.drop_column('curso_id')
        batch_op.drop_column('observacoes')
        batch_op.drop_column('valor_total')
        batch_op.drop_column('tipo_agendamento')

    op.drop_table('agendamento_servico')
