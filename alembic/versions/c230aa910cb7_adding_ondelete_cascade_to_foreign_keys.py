"""Adding ondelete = cascade to foreign keys

Revision ID: c230aa910cb7
Revises: 940898f2b2f8
Create Date: 2020-03-26 06:29:39.433251+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c230aa910cb7'
down_revision = '940898f2b2f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('match_players_matchId_fkey', 'match_players', type_='foreignkey')
    op.drop_constraint('match_players_playerId_fkey', 'match_players', type_='foreignkey')
    op.create_foreign_key('match_players_matchId_fkey', 'match_players', 'matches', ['matchId'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('match_players_playerId_fkey', 'match_players', 'players', ['playerId'], ['id'], ondelete='CASCADE')
    op.drop_constraint('server_players_serverId_fkey', 'server_players', type_='foreignkey')
    op.drop_constraint('server_players_playerId_fkey', 'server_players', type_='foreignkey')
    op.create_foreign_key('server_players_serverId_fkey', 'server_players', 'servers', ['serverId'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('server_players_playerId_fkey', 'server_players', 'players', ['playerId'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('server_players_serverId_fkey', 'server_players', type_='foreignkey')
    op.drop_constraint('server_players_playerId_fkey', 'server_players', type_='foreignkey')
    op.create_foreign_key('server_players_serverId_fkey', 'server_players', 'servers', ['serverId'], ['id'])
    op.create_foreign_key('server_players_playerId_fkey', 'server_players', 'players', ['playerId'], ['id'])
    op.drop_constraint('match_players_matchId_fkey', 'match_players', type_='foreignkey')
    op.drop_constraint('match_players_playerId_fkey', 'match_players', type_='foreignkey')
    op.create_foreign_key('match_players_matchId_fkey', 'match_players', 'matches', ['matchId'], ['id'])
    op.create_foreign_key('match_players_playerId_fkey', 'match_players', 'players', ['playerId'], ['id'])
    # ### end Alembic commands ###
