from telegram.ext import (Updater)
from pathlib import Path
from dotenv import load_dotenv
import os


def create_connection() -> Updater:
    load_dotenv(verbose=False)
    env_path = Path('./env') / '.env'
    load_dotenv(dotenv_path=str(env_path))
    TOKEN = os.getenv('TOKEN')
    PROXY = os.getenv('PROXY')
    if PROXY == 'True':
        REQUEST_KWARGS = {'proxy_url': os.getenv('REQUEST_KWARGS'), 'read_timeout': 30, 'connect_timeout': 30}
        update = Updater(token=TOKEN, request_kwargs=REQUEST_KWARGS)
    else:
        update = Updater(token=TOKEN, request_kwargs={'read_timeout': 30, 'connect_timeout': 30})
    return update
