# ============================================================
# Telegram Auto Cleaner - Start Plugin
# File: plugins/start.py
# ============================================================

import logging

from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from plugins.config import Config


LOGGER = logging.getLogger(__name__)

OWNER_ID = Config.OWNER_ID


@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message):

    # ========================================================
    # DEBUG - START COMMAND RECEIVED
    # ========================================================

    user_id = message.from_user.id if message.from_user else None
    username = message.from_user.username if message.from_user else None

    LOGGER.info(
        "START RECEIVED | user_id=%s | username=%s | owner_id=%s",
        user_id,
        username,
        OWNER_ID
    )

    # ========================================================
    # OWNER CHECK
    # ========================================================

    if not message.from_user:
        LOGGER.warning("START received without from_user")
        return

    if message.from_user.id != OWNER_ID:

        LOGGER.warning(
            "Access denied | user_id=%s | owner_id=%s",
            message.from_user.id,
            OWNER_ID
        )

        await message.reply_text(
            "⚠️ <b>Access Denied</b>\n\n"
            "এই বট শুধুমাত্র এডমিনের জন্য নির্মিত।\n\n"
            f"🆔 আপনার ID: <code>{message.from_user.id}</code>",
            parse_mode=enums.ParseMode.HTML
        )

        return

    # ========================================================
    # OWNER START MESSAGE
    # ========================================================

    text = (
        "👋 <b>স্বাগতম, এডমিন!</b>\n\n"
        "🤖 এটি একটি <b>Auto Cleaner Bot</b>। "
        "এটি আপনার টেলিগ্রাম চ্যানেলের ভিডিও, অডিও বা "
        "ডকুমেন্ট পোস্টের ক্যাপশন থেকে অটোমেটিক্যালি "
        "অযাচিত টেক্সট বা কপিরাইট ট্যাগ মুছে ফেলবে।\n\n"
        "নিচের বাটন চেপে ক্লিনার সেটিংস খুলুন "
        "অথবা সরাসরি <code>/cleaner</code> কমান্ড ব্যবহার করুন।"
    )

    # ========================================================
    # INLINE KEYBOARD
    # ========================================================

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🧹 Open Cleaner Settings",
                    callback_data="ac_refresh"
                )
            ],
            [
                InlineKeyboardButton(
                    "📂 Old Post Cleaner",
                    callback_data="ac_oldclean"
                )
            ]
        ]
    )

    # ========================================================
    # SEND MESSAGE
    # ========================================================

    try:

        await message.reply_text(
            text,
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )

        LOGGER.info(
            "Start command executed successfully by Owner: %s",
            message.from_user.id
        )

    except Exception:
        LOGGER.exception(
            "Failed to send /start response | user_id=%s",
            message.from_user.id
        )
