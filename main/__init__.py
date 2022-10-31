from flask import Flask
from flask_mail import Mail

main = Flask(__name__)
main.config.from_object('config')
mail = Mail(main)

from main import views
from main import rest_api
