# -*- coding: utf-8 -*-

from hashlib import md5
from sqlalchemy import Column, Integer, create_engine, DateTime, ForeignKey, Text, PickleType, Boolean, String
from sqlalchemy.sql import func, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.scoping import scoped_session
from main import main

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    login = Column(String(length=255))
    password = Column(String(length=255))
    email = Column(String(length=255))

    user_music = relationship('MusicInUser', backref='user_music', lazy='dynamic')
    user_message = relationship('Message', backref='user_message', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def __repr__(self):
        return "<User(%r, %r, %r)>" % (self.id, self.login, self.password)


class Music(Base):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=255))
    author = Column(String(length=255))
    path = Column(String(length=255))
    ban = Column(Boolean, default=False)


class MusicInUser(Base):
    __tablename__ = 'musicinuser'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    music_id = Column(Integer, ForeignKey(Music.id))


class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    user_from = Column(Integer, ForeignKey(User.id))
    user_to = Column(Integer)
    text = Column(Text)


engine = create_engine('postgresql+pg8000://%s:%s@%s/%s' % (main.config['DATABASE_USER'],
                                                              main.config['DATABASE_PASSWORD'],
                                                              main.config['DATABASE_IP'],
                                                              main.config['DATABASE_NAME']),
                       encoding='utf8', echo=False, pool_recycle=300, query_cache_size=0, pool_pre_ping=True)
Base.metadata.create_all(engine)

Session = scoped_session(sessionmaker())
Session.configure(bind=engine)
