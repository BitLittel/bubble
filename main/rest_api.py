# -*- coding: utf-8 -*-
from main import main, mail
from flask_mail import Message
from flask import render_template, request, redirect, url_for, jsonify, g
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from datetime import datetime, timedelta
from main.database import Session, User, Music, Token
import re
import os
import hashlib


def hash_password(password: str) -> str:
    h = hashlib.new('sha1')
    h.update(password.encode('utf-8'))
    return h.hexdigest()


def send_mail(user_email: str, subject: str, html_text: str) -> bool:
    with mail.connect() as conn:
        message = Message(
            subject=subject,
            recipients=[user_email],
            html=html_text,
            charset='utf-8'
        )
        conn.send(message)
    return Tru


@main.route('/test', methods=['GET'])
def test():
    send_mail(
        'opera.operaciy@yandex.ru',
        'Подтвердить почту',
        f'<a href="http://127.0.0.1:5000/kakish/{hash_password("opera.operaciy@yandex.ru")}">Тыкни меня</a>'
    )
    return 'kek'


@main.route('/api/v1/get/audio', methods=['GET'])
def api_get_audio():
    return jsonify()


# @main.route('/add_music', methods=['GET', 'POST'])
# @login_required
# def add_music():
#     if request.method == 'POST':
#         files = request.files.getlist('files')
#         for f in files:
#             filename = f.filename
#             name = filename.split('-')
#             artist = name[0].strip()
#             music_name = name[1].split('.')[0].strip()
#             file_extend = name[1].split('.')[1].strip()
#             finaly_path = os.path.join(main.config['UPLOAD_FOLDER'],
#                                        current_user.username,
#                                        f'{artist}-{music_name}.{file_extend}')
#             print(f'{artist}-{music_name}.{file_extend}')
#             f.save(finaly_path)
#             Music(name=music_name, author=artist, path=finaly_path)
#             g.db.add(Music)
#             g.db.commit()
#     return render_template('add_music.html')


@main.route('/api/v1/login', methods=['GET'])
def api_login():
    return jsonify()


@main.route('/api/v1/registration', methods=['GET'])
def api_registration() -> jsonify:
    if request.method == 'GET':
        try:
            login = request.args.get('login').strip()
        except AttributeError:
            return jsonify(dict(reg=False, message='Логин введён не корректно'))

        try:
            email = request.args.get('email').strip()
        except AttributeError:
            return jsonify(dict(reg=False, message='Почта введена не корректно'))

        try:
            password = request.args.get('password').strip()
        except AttributeError:
            return jsonify(dict(reg=False, message='Пароль введён не корректно'))

        try:
            password_repeat = request.args.get('password_repeat').strip()
        except AttributeError:
            return jsonify(dict(reg=False, message='Повторный пароль введён не корректно'))

        if re.search(r'^([a-zA-Z0-9_-]+\.)*[a-zA-Z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$', email) is None:
            return jsonify(dict(reg=False, message='Почта введена не корректно'))

        if re.search(r'^[\w\d_\W]{5,20}$', login) is None:
            return jsonify(dict(reg=False, message='Логин введён не корректно'))

        if len(password) < 8:
            return jsonify(dict(reg=False, message='Пароль слишком короткий. Должен быть от 8 до 20 символов'))

        if re.search(r'^[\w\d_\W]{8,20}$', password) is None:
            return jsonify(dict(reg=False, message='Пароль не соответствует требованиям.'
                                                   'Допускаются латинские символы, цифры и спец.символы.'
                                                   'Суммарная длинны от 8 до 20 символов'))

        if password != password_repeat:
            return jsonify(dict(reg=False, message='Пароли не совпадают'))

        if g.db.query(User).filter(User.login == login).first() is not None:
            return jsonify(dict(reg=False, message='Пользователь с таким логином уже существует'))

        if g.db.query(User).filter(User.email == email).first() is not None:
            return jsonify(dict(reg=False, message='Пользователь с такой почтой уже существует'))

        new_user = User(login=login, email=email, password=hash_password(password))
        new_token_str = hash_password(email+login)
        new_token = Token(token=new_token_str,
                          date_to_active=datetime.now()+timedelta(days=7),
                          user_token=new_user)


        g.db.add(new_user)
        g.db.add(new_token)
        g.db.commit()

        send_mail(
            'opera.operaciy@yandex.ru',
            'Подтвердить почту',
            f'<a href="{main.config["MAIN_URL"]}/token/{new_token_str}">Тыкни меня</a>'
        )

        return jsonify(dict(reg=True, message='Регистрация прошла успешно.'
                                              'Мы отправили вам письмо на почту для подтверждения аккаунта'))
    else:
        return jsonify(dict(error='Method not allowed!'))
