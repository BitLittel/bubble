# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, jsonify, g
from flask_login import current_user, login_required, login_user, LoginManager, logout_user
from main.database import Session, User, Music, Token
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from main import main
import re
import os
import hashlib

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


@main.route('/token/<user_token>', methods=['GET', 'POST'])
def activate_token(user_token):
    find_token = g.db.query(Token).filter(Token.token == user_token).first()

    if find_token is None:
        return render_template('404.html'), 404

    if find_token.date_activate != None:
        return render_template('404.html'), 404

    if find_token.date_to_active < datetime.now():
        return render_template('404.html'), 404

    find_token.date_activate = datetime.now()
    g.db.commit()
    find_user = g.db.query(User).filter(User.id == find_token.user_id).first()
    login_user(find_user, remember=True)

    return redirect(url_for('index'))


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
