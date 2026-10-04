from pyrogram import filters
from utils.logger import logger

def register(app):
    @app.on_message(filters.command("caption") & filters.private)
    async def caption_help(client, message):
        try:
            await message.reply_text("Caption edit করার handler এখানে extend করা যাবে।")
        except Exception: logger.exception("Caption command failed")
