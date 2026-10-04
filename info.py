import os
from os import environ

def get_int(value, default=0):
    try: return int(value)
    except (TypeError, ValueError): return default

SESSION = environ.get('SESSION', 'duplicate_bot')
API_ID = get_int(environ.get('API_ID', '24776633'), 0)
API_HASH = environ.get('API_HASH', '57b1f632044b4e718f5dce004a988d69')
BOT_TOKEN = environ.get('BOT_TOKEN', '8982103415:AAH5meSpQewu-0nBm-yTk1-BBhLyaaOXjS4')
MONGO_URI = environ.get('MONGO_URI', 'mongodb+srv://rendamd1_db_user:M7vb8ZD9rx0AfHnP@cluster0.uzqvib6.mongodb.net/?appName=Cluster0')
LOG_CHANNEL = get_int(environ.get('LOG_CHANNEL', '-1004456487791'), 0)
