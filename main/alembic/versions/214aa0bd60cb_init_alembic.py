"""Init Alembic

Revision ID: 214aa0bd60cb
Revises: 
Create Date: 2024-01-24 17:50:58.769469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '214aa0bd60cb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE EXTENSION "uuid-ossp"')
    op.create_table('Images',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('content_type', sa.String(length=30), nullable=False),
    sa.Column('file_name', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.execute('insert into "Images" (content_type, file_name) values (\'image/jpeg\', \'default_img.jpg\')')
    op.create_table('Users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=70), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('avatar', sa.BigInteger(), nullable=False),
    sa.Column('online', sa.Boolean(), nullable=True),
    sa.Column('liked_playlist', sa.ARRAY(sa.BigInteger()), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['avatar'], ['Images.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Friends',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('user_id_to', sa.BigInteger(), nullable=False),
    sa.Column('status', sa.SmallInteger(), nullable=False),
    sa.Column('datetime_add', sa.DateTime(), nullable=False),
    sa.Column('datetime_change_status', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['user_id_to'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Musics',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('author', sa.String(length=200), nullable=False),
    sa.Column('genre', sa.String(length=200), nullable=True),
    sa.Column('cover', sa.BigInteger(), nullable=False),
    sa.Column('hashsum', sa.String(length=100), nullable=True),
    sa.Column('filename', sa.String(length=75), nullable=False),
    sa.Column('duration', sa.String(length=20), nullable=True),
    sa.Column('datetime_add', sa.DateTime(), nullable=False),
    sa.Column('user_id_add', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['cover'], ['Images.id'], ),
    sa.ForeignKeyConstraint(['user_id_add'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('PlayLists',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('cover', sa.BigInteger(), nullable=False),
    sa.Column('datetime_add', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['cover'], ['Images.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Tokens',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=False),
    sa.Column('token', sa.UUID(as_uuid=False), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('datetime_create', sa.DateTime(), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Tokens_token'), 'Tokens', ['token'], unique=True)
    op.create_table('UserData',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('last_readed_message_id', sa.BigInteger(), nullable=True),
    sa.Column('last_user_from_readed', sa.BigInteger(), nullable=True),
    sa.Column('another', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Actions',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('music_id', sa.BigInteger(), nullable=False),
    sa.Column('datetime_add', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['music_id'], ['Musics.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Collections',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('datetime_add', sa.DateTime(), nullable=False),
    sa.Column('music_id', sa.BigInteger(), nullable=False),
    sa.Column('playlist_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['music_id'], ['Musics.id'], ),
    sa.ForeignKeyConstraint(['playlist_id'], ['PlayLists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Messages',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('user_id_from', sa.BigInteger(), nullable=False),
    sa.Column('user_id_to', sa.BigInteger(), nullable=False),
    sa.Column('message_reply_id', sa.BigInteger(), nullable=True),
    sa.Column('playlist_id', sa.BigInteger(), nullable=True),
    sa.Column('music_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['music_id'], ['Musics.id'], ),
    sa.ForeignKeyConstraint(['playlist_id'], ['PlayLists.id'], ),
    sa.ForeignKeyConstraint(['user_id_from'], ['Users.id'], ),
    sa.ForeignKeyConstraint(['user_id_to'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Messages')
    op.drop_table('Collections')
    op.drop_table('Actions')
    op.drop_table('UserData')
    op.drop_index(op.f('ix_Tokens_token'), table_name='Tokens')
    op.drop_table('Tokens')
    op.drop_table('PlayLists')
    op.drop_table('Musics')
    op.drop_table('Friends')
    op.drop_table('Users')
    op.drop_table('Images')
    # ### end Alembic commands ###
