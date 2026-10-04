import asyncio
from pyrogram import Client
from info import API_ID, API_HASH, BOT_TOKEN, SESSION
from utils.logger import logger

app = Client(SESSION, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

from database.mongodb import init_db
from plugins.duplicate import register as register_duplicate
from plugins.rename import register as register_rename
from plugins.caption import register as register_caption
from plugins.channel_log import register as register_channel_log

init_db()
register_duplicate(app)
register_rename(app)
register_caption(app)
register_channel_log(app)

@app.on_message()
async def catch_error(client, message):
    try:
        # Plugins register their own handlers; this handler only provides a safe log hook.
        return
    except Exception:
        logger.exception("Unhandled message handler error")

async def main():
    try:
        logger.info("Bot starting...")
        await app.start()
        me = await app.get_me()
        logger.info("Bot started: @%s", me.username or me.id)
        await asyncio.Event().wait()
    except Exception:
        logger.exception("FATAL: bot failed to start or stopped unexpectedly")
        raise
    finally:
        try: await app.stop()
        except Exception: logger.exception("Error while stopping bot")

if __name__ == "__main__":
    asyncio.run(main())
