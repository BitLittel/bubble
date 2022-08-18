# -*- coding: utf-8 -*-
import re
import os
import hashlib
from flask import render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from main import main
from werkzeug.utils import secure_filename
from main.database import Users, Musics

login_manager = LoginManager()
login_manager.init_app(main)


def hash_password(password):
    h = hashlib.new('sha1')
    h.update(password.encode('utf-8'))
    return h.hexdigest()


@login_manager.user_loader
def load_user(username):
    user = Users.objects(username=username).first()
    user.list_music = os.listdir(os.path.join(main.config['UPLOAD_FOLDER'], user.username))
    return user


@login_manager.unauthorized_handler
def unauth():
    return redirect(url_for("login", next=request.path))


@main.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@main.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@main.route('/reg', methods=['GET', 'POST'])
def reg():
    error = ['', '']
    if request.method == 'POST':
        username = request.form.get('username')
        password_1 = request.form.get('password')
        password_2 = request.form.get('password_repeat')

        if re.search(r'^[a-zA-Z0-9-_.]{5,50}$', username) is None:
            error[0] = 'Логин введён не коректно. От 5 до 50 символов'
            return render_template('registration.html', error=error, username=username)

        check_username = Users.objects(username=username).first()
        if check_username is not None:
            error[0] = 'Логин занят'
            return render_template('registration.html', error=error, username=username)

        if re.search(r'^[a-zA-Z0-9_.]{5,20}$', password_1) is None:
            error[1] = 'Пароль введён не коректно. От 5 до 20 символов'
            return render_template('registration.html', error=error, username=username)

        if password_1 != password_2:
            error[1] = 'Пароли не совподают'
            return render_template('registration.html', error=error, username=username)

        new_user = Users(username=username, password=hash_password(password_1)).save()
        login_user(new_user, remember=True)
        os.makedirs(os.path.join(main.config['UPLOAD_FOLDER'], new_user.username))

        return redirect(url_for('index'))
    return render_template('registration.html', error=error)


@main.route('/login', methods=['GET', 'POST'])
def login():
    error = ['', '']
    if request.method == 'POST':
        error = ['', '']

        username = request.form.get('username')
        password = request.form.get('password')

        check_user = Users.objects(username=username).first()
        if check_user is None:
            error[0] = 'Логин введён не верно'
            return render_template('login.html', error=error, username=username)

        if check_user.password != hash_password(password):
            error[1] = 'Пароль введён не верно'
            return render_template('login.html', error=error, username=username)

        login_user(check_user, remember=True)
        return redirect(url_for('index'))
    return render_template('login.html', error=error)


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', cur=current_user)


@main.route('/add_music', methods=['GET', 'POST'])
@login_required
def download_music():
    if request.method == 'POST':
        files = request.files.getlist('files')
        for f in files:
            filename = f.filename
            name = filename.split('-')
            artist = name[0].strip()
            music_name = name[1].split('.')[0].strip()
            file_extend = name[1].split('.')[1].strip()
            finaly_path = os.path.join(main.config['UPLOAD_FOLDER'],
                                       current_user.username,
                                       f'{artist}-{music_name}.{file_extend}')
            Musics(name=music_name, artist=artist, file_path=finaly_path).save()
            f.save(finaly_path)
    return render_template('add_music.html')


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
