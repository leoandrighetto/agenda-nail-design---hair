"""unifica_pessoa_flags_eh_cliente_eh_aluno

Revision ID: 330eae0a949c
Revises: ba818f32c465
Create Date: 2026-10-21 12:50:08.056845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '330eae0a949c'
down_revision = 'ba818f32c465'
branch_labels = None
depends_on = None

NAMING_CONVENTION = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}


def upgrade():
    # 1. Adiciona as novas colunas em pessoas
    with op.batch_alter_table('pessoas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('eh_cliente', sa.Boolean(), server_default=sa.text('0'), nullable=False))
        batch_op.add_column(sa.Column('eh_aluno', sa.Boolean(), server_default=sa.text('0'), nullable=False))
        batch_op.add_column(sa.Column('matricula', sa.String(length=50), nullable=True))
        batch_op.create_unique_constraint('uq_pessoas_matricula', ['matricula'])

    # 2. Migra dados existentes das tabelas clientes e alunos para pessoas
    op.execute("UPDATE pessoas SET eh_cliente = 1 WHERE id IN (SELECT id FROM clientes)")
    op.execute(
        "UPDATE pessoas SET eh_aluno = 1, "
        "matricula = (SELECT alunos.matricula FROM alunos WHERE alunos.id = pessoas.id) "
        "WHERE id IN (SELECT id FROM alunos)"
    )

    # 3. Redireciona chaves estrangeiras para pessoas.id antes de remover clientes e alunos
    with op.batch_alter_table('agendamentos', schema=None, naming_convention=NAMING_CONVENTION) as batch_op:
        batch_op.drop_constraint('fk_agendamentos_cliente_id_clientes', type_='foreignkey')
        batch_op.create_foreign_key('fk_agendamentos_cliente_id_pessoas', 'pessoas', ['cliente_id'], ['id'])

    with op.batch_alter_table('curso_aluno', schema=None, naming_convention=NAMING_CONVENTION) as batch_op:
        batch_op.drop_constraint('fk_curso_aluno_aluno_id_alunos', type_='foreignkey')
        batch_op.create_foreign_key('fk_curso_aluno_aluno_id_pessoas', 'pessoas', ['aluno_id'], ['id'])

    with op.batch_alter_table('pagamentos', schema=None, naming_convention=NAMING_CONVENTION) as batch_op:
        batch_op.drop_constraint('fk_pagamentos_aluno_id_alunos', type_='foreignkey')
        batch_op.create_foreign_key('fk_pagamentos_aluno_id_pessoas', 'pessoas', ['aluno_id'], ['id'])

    # 4. Remove a coluna tipo_pessoa e as tabelas antigas
    with op.batch_alter_table('pessoas', schema=None) as batch_op:
        batch_op.drop_column('tipo_pessoa')

    op.drop_table('alunos')
    op.drop_table('clientes')


def downgrade():
    op.create_table(
        'clientes',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['pessoas.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'alunos',
        sa.Column('id', sa.INTEGER(), nullable=False),
        sa.Column('matricula', sa.VARCHAR(length=50), nullable=False),
        sa.ForeignKeyConstraint(['id'], ['pessoas.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('matricula'),
    )

    with op.batch_alter_table('pessoas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tipo_pessoa', sa.VARCHAR(length=50), server_default=sa.text("'cliente'"), nullable=False))

    op.execute("INSERT INTO clientes (id) SELECT id FROM pessoas WHERE eh_cliente = 1")
    op.execute(
        "INSERT INTO alunos (id, matricula) "
        "SELECT id, COALESCE(matricula, 'MAT-' || id) FROM pessoas WHERE eh_aluno = 1"
    )

    with op.batch_alter_table('pagamentos', schema=None, naming_convention=NAMING_CONVENTION) as batch_op:
        batch_op.drop_constraint('fk_pagamentos_aluno_id_pessoas', type_='foreignkey')
        batch_op.create_foreign_key('fk_pagamentos_aluno_id_alunos', 'alunos', ['aluno_id'], ['id'])

    with op.batch_alter_table('curso_aluno', schema=None, naming_convention=NAMING_CONVENTION) as batch_op:
        batch_op.drop_constraint('fk_curso_aluno_aluno_id_pessoas', type_='foreignkey')
        batch_op.create_foreign_key('fk_curso_aluno_aluno_id_alunos', 'alunos', ['aluno_id'], ['id'])

    with op.batch_alter_table('agendamentos', schema=None, naming_convention=NAMING_CONVENTION) as batch_op:
        batch_op.drop_constraint('fk_agendamentos_cliente_id_pessoas', type_='foreignkey')
        batch_op.create_foreign_key('fk_agendamentos_cliente_id_clientes', 'clientes', ['cliente_id'], ['id'])

    with op.batch_alter_table('pessoas', schema=None) as batch_op:
        batch_op.drop_constraint('uq_pessoas_matricula', type_='unique')
        batch_op.drop_column('matricula')
        batch_op.drop_column('eh_aluno')
        batch_op.drop_column('eh_cliente')
