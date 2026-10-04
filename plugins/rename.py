from pyrogram import filters
from utils.logger import logger

def register(app):
    @app.on_message(filters.command("rename") & filters.private)
    async def rename_help(client, message):
        try:
            await message.reply_text("Rename করার জন্য আগে একটি file reply করে /rename NewName পাঠান।")
        except Exception: logger.exception("Rename command failed")
