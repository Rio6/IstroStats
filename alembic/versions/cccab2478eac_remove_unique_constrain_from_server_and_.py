"""Remove unique constrain from server and match players

Revision ID: cccab2478eac
Revises: 663aac85374e
Create Date: 2020-03-24 19:43:31.407888+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cccab2478eac'
down_revision = '663aac85374e'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('match_players_matchId_playerId_key', 'match_players')
    op.drop_constraint('server_players_serverId_playerId_key', 'server_players')
