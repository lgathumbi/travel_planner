"""create tables

Revision ID: a16dc99f3d51
Revises: 
Create Date: 2025-02-03 10:34:11.601658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a16dc99f3d51'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('destinations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('itineraries',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_itineraries_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('itinerary_destinations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('itinerary_id', sa.Integer(), nullable=False),
    sa.Column('destination_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['destination_id'], ['destinations.id'], name=op.f('fk_itinerary_destinations_destination_id_destinations')),
    sa.ForeignKeyConstraint(['itinerary_id'], ['itineraries.id'], name=op.f('fk_itinerary_destinations_itinerary_id_itineraries')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('itinerary_destinations')
    op.drop_table('itineraries')
    op.drop_table('users')
    op.drop_table('destinations')
    # ### end Alembic commands ###
