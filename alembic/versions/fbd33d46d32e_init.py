"""init

Revision ID: fbd33d46d32e
Revises: 
Create Date: 2022-04-23 19:38:10.406126+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbd33d46d32e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('matches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('server', sa.String(), nullable=False),
    sa.Column('finished', sa.DateTime(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('winningSide', sa.String(), nullable=True),
    sa.Column('time', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_matches_finished'), 'matches', ['finished'], unique=False)
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('rank', sa.Integer(), nullable=True),
    sa.Column('faction', sa.String(), nullable=True),
    sa.Column('color', sa.String(), nullable=True),
    sa.Column('ai', sa.Boolean(), nullable=True),
    sa.Column('lastActive', sa.DateTime(), nullable=True),
    sa.Column('mode', sa.String(), nullable=True),
    sa.Column('logonTime', sa.DateTime(), nullable=True),
    sa.Column('hidden', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_players_name'), 'players', ['name'], unique=False)
    op.create_table('servers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('observers', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.Column('hidden', sa.Boolean(), nullable=True),
    sa.Column('runningSince', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('match_players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('matchId', sa.Integer(), nullable=False),
    sa.Column('playerId', sa.Integer(), nullable=False),
    sa.Column('winner', sa.Boolean(), nullable=True),
    sa.Column('side', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['matchId'], ['matches.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['playerId'], ['players.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_match_players_matchId'), 'match_players', ['matchId'], unique=False)
    op.create_index(op.f('ix_match_players_playerId'), 'match_players', ['playerId'], unique=False)
    op.create_table('server_players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('serverId', sa.Integer(), nullable=False),
    sa.Column('playerId', sa.Integer(), nullable=False),
    sa.Column('side', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['playerId'], ['players.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['serverId'], ['servers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('server_players')
    op.drop_index(op.f('ix_match_players_playerId'), table_name='match_players')
    op.drop_index(op.f('ix_match_players_matchId'), table_name='match_players')
    op.drop_table('match_players')
    op.drop_table('servers')
    op.drop_index(op.f('ix_players_name'), table_name='players')
    op.drop_table('players')
    op.drop_index(op.f('ix_matches_finished'), table_name='matches')
    op.drop_table('matches')
    # ### end Alembic commands ###
