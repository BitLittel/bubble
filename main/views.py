# -*- coding: utf-8 -*-
import re
import os
import hashlib
from flask import render_template, request, redirect, url_for, jsonify, g
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from main import main
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import select
from main.database import Session, User, Music

login_manager = LoginManager()
login_manager.init_app(main)
login_manager.session_protection = "strong"
csrf = CSRFProtect(main)


@main.before_request
def before_request():
    g.db = Session()


@login_manager.user_loader
def load_user(uid):
    return g.db.query(User).filter(User.id == uid).first()


@login_manager.unauthorized_handler
def unauth():
    return redirect(url_for("login", next=request.path))


@main.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@main.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    try:
        auth = current_user.is_authenticated()
    except:
        auth = False
    return render_template('index.html', auth=auth)


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


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
