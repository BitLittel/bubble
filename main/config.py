import os

DATABASE_NAME = 'bubble' if os.getenv('DATABASE_NAME') is None else os.getenv('DATABASE_NAME')
DATABASE_IP = 'localhost' if os.getenv('DATABASE_IP') is None else os.getenv('DATABASE_IP')
DATABASE_PORT = 5432 if os.getenv('DATABASE_PORT') is None else os.getenv('DATABASE_PORT')
DATABASE_USER = 'postgres' if os.getenv('DATABASE_USER') is None else os.getenv('DATABASE_USER')
DATABASE_PASSWORD = 'root' if os.getenv('DATABASE_PASSWORD') is None else os.getenv('DATABASE_PASSWORD')
MAIN_URL = 'http://127.0.0.1:8000' if os.getenv('MAIN_URL') is None else os.getenv('MAIN_URL')
API_IMAGE = f'{MAIN_URL}/api/image/' if os.getenv('API_IMAGE') is None else os.getenv('API_IMAGE')
API_MUSIC = f'{MAIN_URL}/api/music/' if os.getenv('API_MUSIC') is None else os.getenv('API_MUSIC')
MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024 if os.getenv('MAX_FILE_SIZE') is None else os.getenv('MAX_FILE_SIZE')
PHOTO_FORMAT = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
AUDIO_FORMAT = ['audio/x-flac', 'audio/webm', 'audio/mpeg', 'audio/flac']
MAIN_PATH = os.path.dirname(os.path.realpath(__file__))[:-5]
MUSICS_FOLDER = os.path.join(MAIN_PATH, 'stored_files', 'musics')
PHOTOS_FOLDER = os.path.join(MAIN_PATH, 'stored_files', 'photos')
