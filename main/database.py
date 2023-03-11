# -*- coding: utf-8 -*-
from main import main
from sqlalchemy import Column, Integer, create_engine, DateTime, ForeignKey, Text, PickleType, Boolean, String
from sqlalchemy.sql import func, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.scoping import scoped_session


Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(length=20), nullable=False)
    password = Column(String(length=50), nullable=False)
    avatar = Column(String(length=255), nullable=True)
    email = Column(String(length=100), nullable=False)

    user_music = relationship('UserMusic', backref='user_music', lazy='dynamic')
    user_message = relationship('Message', backref='user_message', lazy='dynamic')
    user_playlist = relationship('Playlist', backref='user_playlist', lazy='dynamic')
    user_token = relationship('Token', backref='user_token', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return "<User(%r, %r, %r)>" % (self.id, self.login, self.password)


class Token(Base):
    __tablename__ = 'Token'
    id = Column(Integer, primary_key=True, nullable=False)
    token = Column(String(length=50), index=True, nullable=False)
    date_add = Column(DateTime, default=func.now(), nullable=False)
    date_to_active = Column(DateTime, nullable=False)  # обязательно не забываем заполнять
    date_activate = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)


class Playlist(Base):
    __tablename__ = 'Playlist'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(length=100), nullable=False)
    avatar = Column(String(length=255))
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    playlist_music = relationship('PlaylistMusic', backref='playlist_music', lazy='dynamic')


class Music(Base):
    __tablename__ = 'Music'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100), nullable=False)
    author = Column(String(length=100), nullable=False)
    delay = Column(String(length=10), nullable=False)
    avatar = Column(String(length=255))
    path = Column(String(length=255), nullable=False)
    ban = Column(Boolean, default=False, nullable=False)

    music_user = relationship('UserMusic', backref='music_user', lazy='dynamic')
    music_playlist = relationship('PlaylistMusic', backref='music_playlist', lazy='dynamic')


class PlaylistMusic(Base):
    __tablename__ = 'PlaylistMusic'
    id = Column(Integer, primary_key=True, index=True)
    music_id = Column(Integer, ForeignKey(Music.id), nullable=False)
    playlist_id = Column(Integer, ForeignKey(Playlist.id), nullable=False)


class UserMusic(Base):
    __tablename__ = 'UserMusic'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    music_id = Column(Integer, ForeignKey(Music.id), nullable=False)


class Message(Base):
    __tablename__ = 'Message'
    id = Column(Integer, primary_key=True, index=True)
    user_from = Column(Integer, ForeignKey(User.id), nullable=False)
    user_to = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)


engine = create_engine(
    f'postgresql+psycopg2://{main.config["DATABASE_USER"]}'
    f':{main.config["DATABASE_PASSWORD"]}'
    f'@{main.config["DATABASE_IP"]}'
    f'/{main.config["DATABASE_NAME"]}',
    echo=False,
    pool_recycle=300,
    query_cache_size=0,
    pool_pre_ping=True,
    client_encoding="utf8",
    pool_size=10,
    max_overflow=2,
    pool_use_lifo=True
)

Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker())
Session.configure(bind=engine)
