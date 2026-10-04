import asyncio
from aiohttp import web
from pyrogram import Client

from info import API_ID, API_HASH, BOT_TOKEN, SESSION, PORT
from utils.logger import logger

from database.mongodb import init_db
from plugins.duplicate import register as register_duplicate
from plugins.rename import register as register_rename
from plugins.caption import register as register_caption
from plugins.channel_log import register as register_channel_log


# Telegram Bot
app = Client(
    SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# Web Server
async def web_server():
    async def health(request):
        return web.Response(text="Bot is running!")

    web_app = web.Application()
    web_app.router.add_get("/", health)
    web_app.router.add_get("/health", health)

    return web_app


# Safe message error hook
@app.on_message()
async def catch_error(client, message):
    try:
        # Plugins register their own handlers.
        # This handler only provides a safe log hook.
        return
    except Exception:
        logger.exception("Unhandled message handler error")


async def main():
    web_app = None

    try:
        logger.info("Initializing database...")
        init_db()

        logger.info("Registering plugins...")
        register_duplicate(app)
        register_rename(app)
        register_caption(app)
        register_channel_log(app)

        logger.info("Bot starting...")
        await app.start()

        me = await app.get_me()
        logger.info(
            "Bot started: @%s",
            me.username or me.id
        )

        # Start Web Service
        web_app = web.AppRunner(await web_server())
        await web_app.setup()

        bind_address = "0.0.0.0"
        await web.TCPSite(
            web_app,
            bind_address,
            PORT
        ).start()

        logger.info(
            "Web server started on %s:%s",
            bind_address,
            PORT
        )

        # Keep bot and web server running
        await asyncio.Event().wait()

    except Exception:
        logger.exception(
            "FATAL: bot failed to start or stopped unexpectedly"
        )
        raise

    finally:
        # Clean Web Server
        if web_app:
            try:
                await web_app.cleanup()
                logger.info("Web server stopped.")
            except Exception:
                logger.exception(
                    "Error while stopping web server"
                )

        # Clean Telegram Bot
        try:
            if app.is_connected:
                await app.stop()
                logger.info("Bot stopped.")
        except Exception:
            logger.exception(
                "Error while stopping bot"
            )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception:
        logger.exception(
            "Application exited with fatal error."
        )
