import logging
from pyrogram import Client
from Info import API_ID, API_HASH, BOT_TOKEN

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

plugins = dict(root="plugins")

app = Client(
    "@UploaderXNTBot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    sleep_threshold=300,
    plugins=plugins
)

if __name__ == "__main__":
    app.run()
