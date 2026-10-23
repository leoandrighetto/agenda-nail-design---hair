"""adiciona_matriculas_e_atualiza_pagamentos_servicos

Revision ID: 0b8885302643
Revises: 330eae0a949c
Create Date: 2026-10-21 12:55:06.241958

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b8885302643'
down_revision = '330eae0a949c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'matriculas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('aluno_id', sa.Integer(), nullable=False),
        sa.Column('curso_id', sa.Integer(), nullable=False),
        sa.Column('horas_realizadas', sa.Integer(), nullable=False),
        sa.Column('valor_acordado', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            'status',
            sa.Enum('EM_ANDAMENTO', 'CONCLUIDO', 'CANCELADO', 'TRANCADO', name='status_matricula_enum'),
            nullable=False,
        ),
        sa.Column('data_matricula', sa.Date(), nullable=False),
        sa.Column('data_conclusao', sa.Date(), nullable=True),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['aluno_id'], ['pessoas.id'], name='fk_matriculas_aluno_id_pessoas'),
        sa.ForeignKeyConstraint(['curso_id'], ['cursos.id'], name='fk_matriculas_curso_id_cursos'),
        sa.PrimaryKeyConstraint('id'),
    )

    # Migra vínculos anteriores de curso_aluno para matriculas antes de remover curso_aluno
    op.execute(
        "INSERT INTO matriculas (aluno_id, curso_id, horas_realizadas, valor_acordado, status, data_matricula) "
        "SELECT ca.aluno_id, ca.curso_id, COALESCE(c.horas_realizadas, 0), COALESCE(c.valor_total, 0), "
        "'EM_ANDAMENTO', CURRENT_DATE "
        "FROM curso_aluno ca JOIN cursos c ON c.id = ca.curso_id"
    )

    op.drop_table('curso_aluno')

    with op.batch_alter_table('pagamentos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('matricula_id', sa.Integer(), nullable=True))
        batch_op.alter_column(
            'forma_pagamento',
            existing_type=sa.VARCHAR(length=6),
            type_=sa.Enum(
                'PIX',
                'DINHEIRO',
                'CARTAO',
                'CARTAO_CREDITO',
                'CARTAO_DEBITO',
                'BOLETO',
                'TRANSFERENCIA',
                name='forma_pagamento_enum',
            ),
            existing_nullable=True,
        )
        batch_op.create_foreign_key(
            'fk_pagamentos_matricula_id_matriculas',
            'matriculas',
            ['matricula_id'],
            ['id'],
        )

    with op.batch_alter_table('servicos', schema=None) as batch_op:
        batch_op.alter_column(
            'preco',
            existing_type=sa.FLOAT(),
            type_=sa.Numeric(precision=10, scale=2),
            existing_nullable=True,
        )


def downgrade():
    with op.batch_alter_table('servicos', schema=None) as batch_op:
        batch_op.alter_column(
            'preco',
            existing_type=sa.Numeric(precision=10, scale=2),
            type_=sa.FLOAT(),
            existing_nullable=True,
        )

    with op.batch_alter_table('pagamentos', schema=None) as batch_op:
        batch_op.drop_constraint('fk_pagamentos_matricula_id_matriculas', type_='foreignkey')
        batch_op.alter_column(
            'forma_pagamento',
            existing_type=sa.Enum(
                'PIX',
                'DINHEIRO',
                'CARTAO',
                'CARTAO_CREDITO',
                'CARTAO_DEBITO',
                'BOLETO',
                'TRANSFERENCIA',
                name='forma_pagamento_enum',
            ),
            type_=sa.VARCHAR(length=6),
            existing_nullable=True,
        )
        batch_op.drop_column('matricula_id')

    op.create_table(
        'curso_aluno',
        sa.Column('curso_id', sa.INTEGER(), nullable=False),
        sa.Column('aluno_id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['aluno_id'], ['pessoas.id'], name='fk_curso_aluno_aluno_id_pessoas'),
        sa.ForeignKeyConstraint(['curso_id'], ['cursos.id'], name='fk_curso_aluno_curso_id_cursos'),
        sa.PrimaryKeyConstraint('curso_id', 'aluno_id'),
    )
    op.execute(
        "INSERT OR IGNORE INTO curso_aluno (curso_id, aluno_id) "
        "SELECT curso_id, aluno_id FROM matriculas"
    )
    op.drop_table('matriculas')
