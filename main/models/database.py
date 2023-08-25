# -*- coding: utf-8 -*-
from sqlalchemy import Column, DateTime, ForeignKey, Text, Boolean, String, BigInteger, UUID, SmallInteger, ARRAY
from sqlalchemy import func, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs
import hashlib
import main.config as config


def hash_password(password: str) -> str:
    h = hashlib.new('sha256')
    h.update(password.encode('utf-8'))
    return h.hexdigest()


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Images(Base):
    __tablename__ = 'Images'
    id = Column(BigInteger, primary_key=True)
    content_type = Column(String(length=30), nullable=False)
    file_name = Column(String(length=40), nullable=False)


class Users(Base):
    __tablename__ = 'Users'
    id = Column(BigInteger, primary_key=True)
    username = Column(String(length=30), nullable=False)
    password = Column(String(length=70), nullable=False)
    email = Column(String(length=100), nullable=False)
    avatar = Column(BigInteger, ForeignKey(Images.id), nullable=False)
    online = Column(Boolean, default=False)
    liked_playlist = Column(ARRAY(BigInteger), default=list())
    is_active = Column(Boolean, default=False)


class Friends(Base):
    __tablename__ = 'Friends'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey(Users.id), nullable=False)
    user_id_to = Column(BigInteger, ForeignKey(Users.id), nullable=False)
    status = Column(SmallInteger, nullable=False)  # 1 - заявка отправлена и ожидает, 0 - заявка принята,
    # 2 - заявка отклонена и можно будет повторно отправить через 24 часа
    datetime_add = Column(DateTime, default=func.now(), nullable=False)
    datetime_change_status = Column(DateTime, default=func.now(), nullable=False)


class Tokens(Base):
    __tablename__ = 'Tokens'
    id = Column(BigInteger, primary_key=True)
    type = Column(String(length=100), nullable=False, default='regular')
    token = Column(UUID(as_uuid=False), unique=True, nullable=False, index=True,
                   server_default=text('uuid_generate_v4()'))
    datetime_create = Column(DateTime, default=func.now(), nullable=False)
    expires = Column(DateTime, nullable=False)

    # Foreign Key
    user_id = Column(BigInteger, ForeignKey(Users.id), nullable=False)


class UserData(Base):
    __tablename__ = 'UserData'
    id = Column(BigInteger, primary_key=True)
    last_readed_message_id = Column(BigInteger, nullable=True)
    last_user_from_readed = Column(BigInteger, nullable=True)
    another = Column(String(length=255), nullable=True)
    # Сюда можно всякий хлам накидать что можно использовать в будущем

    # Foreign Key
    user_id = Column(BigInteger, ForeignKey(Users.id), nullable=False)


class PlayLists(Base):
    __tablename__ = 'PlayLists'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=30), nullable=False)
    cover = Column(BigInteger, ForeignKey(Images.id), nullable=False)  # Column(String(length=255), nullable=True)
    datetime_add = Column(DateTime, nullable=False, default=func.now())

    # Foreign Key
    user_id = Column(BigInteger, ForeignKey(Users.id), nullable=False)


class Musics(Base):
    __tablename__ = 'Musics'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=200), nullable=False)
    author = Column(String(length=200), nullable=False)
    genre = Column(String(length=20), nullable=True)
    cover = Column(BigInteger, ForeignKey(Images.id), nullable=False)
    hashsum = Column(String(length=100), nullable=True)
    filename = Column(String(length=75), nullable=False)
    duration = Column(String(length=20), nullable=True)
    datetime_add = Column(DateTime, nullable=False, default=func.now())

    # Foreign Key
    user_id_add = Column(BigInteger, ForeignKey(Users.id), nullable=False)


class Actions(Base):
    __tablename__ = 'Actions'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey(Users.id), nullable=False)
    music_id = Column(BigInteger, ForeignKey(Musics.id), nullable=False)
    datetime_add = Column(DateTime, nullable=False, default=func.now())


class Collections(Base):
    __tablename__ = 'Collections'
    id = Column(BigInteger, primary_key=True)
    track_number = Column(BigInteger, nullable=False)
    datetime_add = Column(DateTime, nullable=False, default=func.now())
    # Foreign Key
    music_id = Column(BigInteger, ForeignKey(Musics.id), nullable=False)
    playlist_id = Column(BigInteger, ForeignKey(PlayLists.id), nullable=False)


class Messages(Base):
    __tablename__ = 'Messages'
    id = Column(BigInteger, primary_key=True)
    text = Column(Text, nullable=True)

    # Foreign Key
    user_id_from = Column(BigInteger, ForeignKey(Users.id), nullable=False)
    user_id_to = Column(BigInteger, ForeignKey(Users.id), nullable=False)
    message_reply_id = Column(BigInteger, nullable=True)
    playlist_id = Column(BigInteger, ForeignKey(PlayLists.id), nullable=True)
    music_id = Column(BigInteger, ForeignKey(Musics.id), nullable=True)


engine = create_async_engine(
        f'postgresql+asyncpg://{config.DATABASE_USER}'
        f':{config.DATABASE_PASSWORD}'
        f'@{config.DATABASE_IP}'
        f'/{config.DATABASE_NAME}',
        echo=False,
        pool_recycle=300,
        query_cache_size=0,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=2,
        pool_use_lifo=True
    )

Session = async_sessionmaker(engine, expire_on_commit=False)


async def start() -> None:
    await query_execute(query_text='CREATE EXTENSION "uuid-ossp";', fetch_all=False, type_query='insert')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await query_execute(
        query_text='insert into "Images" (content_type, file_name) '
                   'values (\'image/jpeg\', \'default_img.jpg\')',
        fetch_all=False,
        type_query='insert'
    )


async def query_execute(query_text: str, fetch_all: bool = False, type_query: str = 'read'):
    async with Session() as db:
        print(query_text, fetch_all, type_query)
        query_object = await db.execute(text(query_text))
        if type_query == 'read':
            return query_object.fetchall() if fetch_all else query_object.fetchone()
        else:
            await db.execute(text('commit'))
            return True
