import os
from os import environ

def get_int(value, default=0):
    try: return int(value)
    except (TypeError, ValueError): return default

SESSION = environ.get('SESSION', 'duplicate_bot')
API_ID = get_int(environ.get('API_ID', ''), 0)
API_HASH = environ.get('API_HASH', '')
BOT_TOKEN = environ.get('BOT_TOKEN', '')
MONGO_URI = environ.get('MONGO_URI', '')
LOG_CHANNEL = get_int(environ.get('LOG_CHANNEL', ''), 0)
