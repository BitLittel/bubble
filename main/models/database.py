# -*- coding: utf-8 -*-
import asyncio
from sqlalchemy import Column, DateTime, ForeignKey, Text, Boolean, String, BigInteger, UUID, SmallInteger
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


class Users(Base):
    __tablename__ = 'Users'
    id = Column(BigInteger, primary_key=True)
    username = Column(String(length=30), nullable=False)
    password = Column(String(length=255), nullable=False)
    email = Column(String(length=100), nullable=False)
    avatar = Column(String(length=255), nullable=True)
    online = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)

    def verify_password(self, password):
        return self.password == hash_password(password)


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
    cover = Column(String(length=255), nullable=True)

    # Foreign Key
    user_id = Column(BigInteger, ForeignKey(Users.id), nullable=False)


class Musics(Base):
    __tablename__ = 'Musics'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=30), nullable=False)
    author = Column(String(length=30), nullable=False)
    genre = Column(String(length=50), default=False)
    picture = Column(String(length=255), nullable=True)
    path = Column(String(length=255), nullable=False)
    time_duration = Column(String(length=20), default=False)
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


async def start() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


Session = async_sessionmaker(engine, expire_on_commit=False)
# asyncio.run(start())
