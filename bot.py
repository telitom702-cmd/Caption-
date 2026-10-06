import logging
from pyrogram import Client
from plugins.config import Config # এখান থেকে ইমপোর্ট করা হয়েছে

logging.basicConfig(level=logging.INFO)

plugins = dict(root="plugins")

app = Client(
    "@UploaderXNTBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=300,
    plugins=plugins
)

if __name__ == "__main__":
    app.run()
