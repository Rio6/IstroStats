"""Fix ai player models

Revision ID: 663aac85374e
Revises: 
Create Date: 2020-03-24 18:16:51.866426+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '663aac85374e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('match_players', 'side',
               existing_type=sa.VARCHAR(length=16),
               type_=sa.String,
               existing_nullable=True)
    op.alter_column('matches', 'server',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.String,
               existing_nullable=False)
    op.alter_column('matches', 'type',
               existing_type=sa.VARCHAR(length=16),
               type_=sa.String,
               existing_nullable=True)
    op.alter_column('matches', 'winningSide',
               existing_type=sa.VARCHAR(length=18),
               type_=sa.String,
               existing_nullable=True)
    op.alter_column('players', 'color',
               existing_type=sa.VARCHAR(length=9),
               type_=sa.String,
               existing_nullable=True)
    op.alter_column('players', 'faction',
               existing_type=sa.VARCHAR(length=8),
               type_=sa.String,
               existing_nullable=True)
    op.alter_column('players', 'mode',
               existing_type=sa.VARCHAR(length=18),
               type_=sa.String,
               existing_nullable=True)
    op.alter_column('players', 'name',
               existing_type=sa.VARCHAR(length=18),
               type_=sa.String,
               existing_nullable=False)
    op.alter_column('server_players', 'side',
               existing_type=sa.VARCHAR(length=18),
               type_=sa.String,
               existing_nullable=True)
    op.alter_column('servers', 'name',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.String,
               existing_nullable=False)
    op.alter_column('servers', 'state',
               existing_type=sa.VARCHAR(length=16),
               type_=sa.String,
               existing_nullable=True)
    op.alter_column('servers', 'type',
               existing_type=sa.VARCHAR(length=16),
               type_=sa.String,
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('servers', 'type',
               existing_type=sa.String,
               type_=sa.VARCHAR(length=16),
               existing_nullable=True)
    op.alter_column('servers', 'state',
               existing_type=sa.String,
               type_=sa.VARCHAR(length=16),
               existing_nullable=True)
    op.alter_column('servers', 'name',
               existing_type=sa.String,
               type_=sa.VARCHAR(length=32),
               existing_nullable=False)
    op.alter_column('server_players', 'side',
               existing_type=sa.String,
               type_=sa.VARCHAR(length=18),
               existing_nullable=True)
    op.alter_column('players', 'name',
               existing_type=sa.String,
               type_=sa.VARCHAR(length=18),
               existing_nullable=False)
    op.alter_column('players', 'mode',
               existing_type=sa.String,
               type_=sa.VARCHAR(length=18),
               existing_nullable=True)
    op.alter_column('players', 'faction',
               existing_type=sa.String,
               type_=sa.VARCHAR(length=8),
               existing_nullable=True)
    op.alter_column('players', 'color',
               existing_type=sa.String,
               type_=sa.VARCHAR(length=9),
               existing_nullable=True)
    op.alter_column('matches', 'winningSide',
               existing_type=sa.String,
               type_=sa.VARCHAR(length=18),
               existing_nullable=True)
    op.alter_column('matches', 'type',
               existing_type=sa.String,
               type_=sa.VARCHAR(length=16),
               existing_nullable=True)
    op.alter_column('matches', 'server',
               existing_type=sa.String,
               type_=sa.VARCHAR(length=32),
               existing_nullable=False)
    op.alter_column('match_players', 'side',
               existing_type=sa.String,
               type_=sa.VARCHAR(length=16),
               existing_nullable=True)
    # ### end Alembic commands ###