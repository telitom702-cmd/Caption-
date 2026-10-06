import logging
import asyncio

from aiohttp import web
from pyrogram import Client, idle

from plugins.config import Config


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

LOGGER = logging.getLogger(__name__)


# ============================================================
# PYROGRAM PLUGINS
# ============================================================

plugins = dict(root="plugins")


# ============================================================
# TELEGRAM BOT
# ============================================================

app = Client(
    "@UploaderXNTBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=300,
    plugins=plugins
)


# ============================================================
# WEB SERVER
# ============================================================

async def home(request):
    return web.Response(
        text="UploaderXNTBot is Running ✅",
        content_type="text/plain"
    )


async def health(request):
    return web.Response(
        text="OK",
        content_type="text/plain"
    )


async def start_web_server():
    web_app = web.Application()

    # Routes
    web_app.router.add_get("/", home)
    web_app.router.add_get("/health", health)

    # Render PORT
    port = int(getattr(Config, "PORT", 8080))

    runner = web.AppRunner(web_app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()

    LOGGER.info(
        "🌐 Web Service started on port %s",
        port
    )

    return runner


# ============================================================
# MAIN
# ============================================================

async def main():

    # --------------------------------------------------------
    # Start Telegram Bot
    # --------------------------------------------------------

    try:
        await app.start()

        me = await app.get_me()

        LOGGER.info(
            "🤖 Bot Started Successfully: @%s",
            me.username
        )

    except Exception:
        LOGGER.exception("❌ Telegram Bot failed to start!")
        raise


    # --------------------------------------------------------
    # Start Web Service
    # --------------------------------------------------------

    try:
        await start_web_server()

    except Exception:
        LOGGER.exception("❌ Web Service failed to start!")
        await app.stop()
        raise


    # --------------------------------------------------------
    # Keep Bot Running
    # --------------------------------------------------------

    LOGGER.info("✅ Bot + Web Service are running.")

    await idle()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        LOGGER.info("🛑 Bot stopped by user.")

    except Exception:
        LOGGER.exception("❌ Fatal error occurred.")
