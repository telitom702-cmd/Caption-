from pyrogram import filters
from utils.logger import logger
from database.mongodb import find_file, save_file
from info import LOG_CHANNEL

def get_media(message):
    if message.document: return message.document, "document"
    if message.video: return message.video, "video"
    if message.audio: return message.audio, "audio"
    if message.photo: return message.photo, "photo"
    return None, None

def register(app):
    @app.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.photo), group=10)
    async def duplicate_check(client, message):
        try:
            media, media_type = get_media(message)
            if not media: return
            unique_id = getattr(media, "file_unique_id", None)
            file_id = getattr(media, "file_id", None)
            name = getattr(media, "file_name", None) or "unknown"
            caption = message.caption or ""
            if not unique_id:
                logger.warning("No file_unique_id for %s", name)
                return
            old = await find_file(unique_id)
            if old:
                text = f"⚠️ DUPLICATE FILE\n\n📁 Name: {name}\n🔗 Link: {message.link or 'Private message'}\n🆔 Unique ID: {unique_id}\n📝 Caption: {caption[:1000]}"
                logger.warning("Duplicate found: %s | %s", name, unique_id)
                if LOG_CHANNEL:
                    try: await client.send_message(LOG_CHANNEL, text)
                    except Exception: logger.exception("Failed to send duplicate log to LOG_CHANNEL")
                await message.reply_text("⚠️ এই ফাইলটি Duplicate হিসেবে পাওয়া গেছে।")
            else:
                await save_file({"file_unique_id": unique_id, "file_id": file_id, "file_name": name, "caption": caption, "type": media_type})
                logger.info("New file saved: %s | %s", name, unique_id)
        except Exception:
            logger.exception("Duplicate check failed")
            try: await message.reply_text("❌ File check করতে error হয়েছে। logs/bot.log দেখুন।")
            except Exception: logger.exception("Failed to send duplicate error message")
