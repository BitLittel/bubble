from multiprocessing import cpu_count
import os

# Socket Path
main_path = os.path.dirname(os.path.realpath(__file__))
bind = f'unix:{main_path}/gunicorn.sock'


# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = f'{main_path}/access_log'
errorlog = f'{main_path}/error_log'
