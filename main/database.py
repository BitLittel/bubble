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
    login = Column(String(length=255))
    password = Column(String(length=255))
    avatar = Column(String(length=255))
    email = Column(String(length=255))

    user_music = relationship('UserMusic', backref='user_music', lazy='dynamic')
    user_message = relationship('Message', backref='user_message', lazy='dynamic')
    user_playlist = relationship('Playlist', backref='user_playlist', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return "<User(%r, %r, %r)>" % (self.id, self.login, self.password)


class Playlist(Base):
    __tablename__ = 'Playlist'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255))
    avatar = Column(String(length=255))
    user_id = Column(Integer, ForeignKey(User.id))

    playlist_music = relationship('PlaylistMusic', backref='playlist_music', lazy='dynamic')


class Music(Base):
    __tablename__ = 'Music'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=255))
    author = Column(String(length=255))
    delay = Column(String(length=10))
    avatar = Column(String(length=255))
    path = Column(String(length=255))
    ban = Column(Boolean, default=False)

    music_user = relationship('UserMusic', backref='music_user', lazy='dynamic')
    music_playlist = relationship('PlaylistMusic', backref='music_playlist', lazy='dynamic')


class PlaylistMusic(Base):
    __tablename__ = 'PlaylistMusic'
    id = Column(Integer, primary_key=True, index=True)
    music_id = Column(Integer, ForeignKey(Music.id))
    playlist_id = Column(Integer, ForeignKey(Playlist.id))


class UserMusic(Base):
    __tablename__ = 'UserMusic'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id))
    music_id = Column(Integer, ForeignKey(Music.id))


class Message(Base):
    __tablename__ = 'Message'
    id = Column(Integer, primary_key=True, index=True)
    user_from = Column(Integer, ForeignKey(User.id))
    user_to = Column(Integer)
    text = Column(Text)


engine = create_engine(
    f'postgresql+pg8000://{main.config["DATABASE_USER"]}'
    f':{main.config["DATABASE_PASSWORD"]}'
    f'@{main.config["DATABASE_IP"]}'
    f'/{main.config["DATABASE_NAME"]}',
    encoding='utf8', echo=False, pool_recycle=300, query_cache_size=0, pool_pre_ping=True
)

Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker())
Session.configure(bind=engine)
