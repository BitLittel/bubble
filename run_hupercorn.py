import asyncio
from hypercorn.config import Config
from hypercorn.asyncio import serve
import os

from main import main

MAIN_PATH = os.path.dirname(os.path.realpath(__file__))

config = Config()
config.bind = ["127.0.0.1:8000"]
config.certfile = os.path.join(MAIN_PATH, "cert.pem")
config.keyfile = os.path.join(MAIN_PATH, "key.pem")
# venv/bin/hypercorn -c hypercorn_conf.toml main:main
asyncio.run(serve(main, config))
