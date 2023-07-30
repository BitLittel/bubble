from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

main = FastAPI(title='Bubble')
main.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


from main import views
from main.api import api_user
from main.api import api_music
from main.api import api_auth
from main.api import api_upload_file
