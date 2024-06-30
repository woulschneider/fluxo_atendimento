"""migracao inicial

Revision ID: 830632c6f94a
Revises: 
Create Date: 2024-06-30 11:51:46.428692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '830632c6f94a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('paciente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=64), nullable=True),
    sa.Column('diagnostico', sa.String(length=128), nullable=True),
    sa.Column('cid', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('paciente', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_paciente_nome'), ['nome'], unique=True)

    op.create_table('servico_especializado',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('servico_especializado', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_servico_especializado_nome'), ['nome'], unique=True)

    op.create_table('servico_manejo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('servico_manejo', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_servico_manejo_nome'), ['nome'], unique=True)

    op.create_table('diagnostico',
    sa.Column('cid', sa.String(length=10), nullable=False),
    sa.Column('descricao', sa.String(length=128), nullable=True),
    sa.Column('servico_especializado_id', sa.Integer(), nullable=True),
    sa.Column('servico_manejo_ids', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['servico_especializado_id'], ['servico_especializado.id'], ),
    sa.PrimaryKeyConstraint('cid')
    )
    op.create_table('fluxo_atendimento',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('paciente_id', sa.Integer(), nullable=True),
    sa.Column('diagnostico_cid', sa.String(length=10), nullable=True),
    sa.Column('etapa', sa.String(length=64), nullable=True),
    sa.Column('data', sa.DateTime(), nullable=True),
    sa.Column('proximo_passo', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['diagnostico_cid'], ['diagnostico.cid'], ),
    sa.ForeignKeyConstraint(['paciente_id'], ['paciente.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fluxo_atendimento')
    op.drop_table('diagnostico')
    with op.batch_alter_table('servico_manejo', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_servico_manejo_nome'))

    op.drop_table('servico_manejo')
    with op.batch_alter_table('servico_especializado', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_servico_especializado_nome'))

    op.drop_table('servico_especializado')
    with op.batch_alter_table('paciente', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_paciente_nome'))

    op.drop_table('paciente')
    # ### end Alembic commands ###
