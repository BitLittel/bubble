# -*- coding: utf-8 -*-
from main import main
import re
import os
import hashlib
from flask import render_template, request, redirect, url_for, jsonify, g
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import select
from main.database import Session, User, Music


def hash_password(password: str) -> str:
    h = hashlib.new('sha1')
    h.update(password.encode('utf-8'))
    return h.hexdigest()


@main.route('/api/v1/get/audio', methods=['GET'])
def api_get_audio():
    return jsonify()


@main.route('/api/v1/login', methods=['GET'])
def api_login():
    return jsonify()


@main.route('/api/v1/registration', methods=['GET'])
def api_registration() -> jsonify:
    if request.method == 'GET':
        login = request.args.get('login')
        email = request.args.get('email')
        password = request.args.get('password')
        password_repeat = request.args.get('password_repeat')
        print(login, email, password, password_repeat)

        if re.search(r'^([a-zA-Z0-9_-]+\.)*[a-zA-Z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$', email) is None:
            return jsonify(dict(reg=False, message='Почта введена не корректно'))
        if re.search(r'^[\w\d_\W]{5,20}$', login) is None:
            return jsonify(dict(reg=False, message='Логин введён не корректно'))
        if password != password_repeat:
            return jsonify(dict(reg=False, message='Пароли не совпадают'))
        if g.db.query(User).filter(User.login == login).first() is not None:
            return jsonify(dict(reg=False, message='Пользователь с таким логином уже существует'))
        if g.db.query(User).filter(User.email == email).first() is not None:
            return jsonify(dict(reg=False, message='Пользователь с такой почтой уже существует'))

        new_user = User(login=login, email=email, password=hash_password(password))
        g.db.add(new_user)
        g.db.commit()
        login_user(new_user, remember=True)
        return jsonify(dict(reg=True, message='Регистрация прошла успешно'))
    else:
        return jsonify(dict(error='Method not allowed!'))
