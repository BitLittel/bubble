from flask import Flask
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

main = Flask(__name__)
main.config.from_object('config')
db = MongoEngine(main)
main.session_interface = MongoEngineSessionInterface(db)


from main import views
from main import rest_api
