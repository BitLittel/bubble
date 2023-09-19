import os

DATABASE_NAME = 'bubble'
DATABASE_IP = 'localhost'
DATABASE_PORT = 5432
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = 'root'
MAIN_URL = 'http://127.0.0.1:8000'
DEFAULT_AVATAR = f'{MAIN_URL}/static/img/default_img.jpg'
API_IMAGE = f'{MAIN_URL}/api/image/'
API_MUSIC = f'{MAIN_URL}/api/music/'
MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024
PHOTO_FORMAT = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
AUDIO_FORMAT = ['audio/x-flac', 'audio/webm', 'audio/mpeg', 'audio/flac']
MAIN_PATH = os.path.dirname(os.path.realpath(__file__))[:-5]
MUSICS_FOLDER = os.path.join(MAIN_PATH, 'stored_files', 'musics')
PHOTOS_FOLDER = os.path.join(MAIN_PATH, 'stored_files', 'photos')
