# -*- coding: utf-8 -*-
import re
import os
import hashlib
from flask import render_template, request, redirect, url_for, jsonify, g
# from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from main import main
# from main.database import User, Music

# login_manager = LoginManager()
# login_manager.init_app(main)


# def hash_password(password):
#     h = hashlib.new('sha1')
#     h.update(password.encode('utf-8'))
#     return h.hexdigest()
#
#
# @login_manager.user_loader
# def load_user(uid):
#     return g.db.query(User).filter_by(id=uid).first()
#
#
# @login_manager.unauthorized_handler
# def unauth():
#     return redirect(url_for("login", next=request.path))


@main.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@main.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@main.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# @main.route('/reg', methods=['GET', 'POST'])
# def reg():
#     error = ['', '', '']
#     if request.method == 'POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password_1 = request.form.get('password')
#         password_2 = request.form.get('password_repeat')
#
#         if re.search(r'^[a-zA-Z0-9-_.]{5,50}$', username) is None:
#             error[0] = 'Логин введён не коректно. От 5 до 50 символов'
#             return render_template('registration.html', error=error, username=username, email=email)
#
#         check_username = g.db.query(User).filter(User.login == username).first()
#         if check_username:
#             error[0] = 'Логин занят'
#             return render_template('registration.html', error=error, username=username, email=email)
#
#         check_email = g.db.query(User).filter(User.email == email).first()
#         if check_email:
#             error[2] = 'Почта уже занята'
#             return render_template('registration.html', error=error, username=username, email=email)
#
#         if re.search(r'^[a-zA-Z0-9_.]{5,20}$', password_1) is None:
#             error[1] = 'Пароль введён не коректно. От 5 до 20 символов'
#             return render_template('registration.html', error=error, username=username, email=email)
#
#         if password_1 != password_2:
#             error[1] = 'Пароли не совподают'
#             return render_template('registration.html', error=error, username=username, email=email)
#
#         new_user = User(login=username, password=hash_password(password_1), email=email)
#         login_user(new_user, remember=True)
#         # os.makedirs(os.path.join(main.config['UPLOAD_FOLDER'], new_user.username))
#
#         return redirect(url_for('index'))
#     return render_template('registration.html', error=error)


# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     error = ['', '']
#     if request.method == 'POST':
#         error = ['', '']
#
#         username = request.form.get('username')
#         password = request.form.get('password')
#
#         check_user = g.db.query(User).filter(User.login == username).first()
#         if check_user is None:
#             error[0] = 'Логин введён не верно'
#             return render_template('login.html', error=error, username=username)
#
#         if check_user.password != hash_password(password):
#             error[1] = 'Пароль введён не верно'
#             return render_template('login.html', error=error, username=username)
#
#         login_user(check_user, remember=True)
#         return redirect(url_for('index'))
#     return render_template('login.html', error=error)


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
# @login_required
def index():
    return render_template('index.html')  # , current_user=current_user)


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


# @main.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("login"))
