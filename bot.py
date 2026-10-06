import logging
import asyncio

from aiohttp import web
from pyrogram import Client

from plugins.config import Config


logging.basicConfig(level=logging.INFO)


# ============================================================
# Pyrogram Plugins
# ============================================================

plugins = dict(root="plugins")


# ============================================================
# Bot
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
# Web Server
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

    # Render / Railway / VPS port
    port = int(getattr(Config, "PORT", 8080))

    runner = web.AppRunner(web_app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()

    logging.info(f"Web Service started on port {port}")


# ============================================================
# Main
# ============================================================

async def main():

    # Start Bot
    await app.start()

    me = await app.get_me()

    logging.info(
        f"Bot Started: @{me.username}"
    )

    # Start Web Service
    await start_web_server()

    # Keep running forever
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
