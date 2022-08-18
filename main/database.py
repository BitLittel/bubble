# -*- coding: utf-8 -*-
from main import db


class Users(db.Document):
    meta = {'collection': 'users'}
    username = db.StringField(required=True, max_length=50, unique=True)
    password = db.StringField(required=True, max_length=255)
    avatar = db.StringField(max_length=255, default="")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


class Musics(db.Document):
    meta = {'collection': 'musics'}
    name = db.StringField(required=True, max_length=255, default="Без названия")
    artist = db.StringField(required=True, max_length=255, default="Неизвестен")
    file_path = db.StringField(required=True, max_length=255)
    photo_album = db.StringField(max_length=255, default="")


class Messages(db.Document):
    meta = {'collection': 'messages'}
    send_from = db.StringField(max_length=255, default="")
    sent_to = db.StringField(max_length=255, default="")
    send_music = db.StringField(max_length=255, default="")
    send_playlist = db.StringField(max_length=255, default="")
    message_read = db.StringField(max_length=255, default="")
