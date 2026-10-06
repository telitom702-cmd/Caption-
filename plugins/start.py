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
    
    # যদি ইউজার এডমিন (OWNER) না হয়, তবে তাকে ব্যবহার করতে দেবে না
    if message.from_user.id != OWNER_ID:
        await message.reply_text(
            "⚠️ <b>Access Denied</b>\n\n"
            "এই বট শুধুমাত্র এডমিনের জন্য নির্মিত।",
            parse_mode=enums.ParseMode.HTML
        )
        return

    # এডমিন হলে স্টার্ট মেসেজ পাঠাবে
    text = (
        "👋 <b>স্বাগতম, এডমিন!</b>\n\n"
        "🤖 এটি একটি <b>Auto Cleaner Bot</b>। এটি আপনার টেলিগ্রাম চ্যানেলের "
        "ভিডিও, অডিও বা ডকুমেন্ট পোস্টের ক্যাপশন থেকে অটোমেটিক্যালি "
        "অযাচিত টেক্সট বা কপিরাইট ট্যাগ মুছে ফেলবে।\n\n"
        "নিচের বাটন চেপে ক্লিনার সেটিংস খুলুন অথবা সরাসরি <code>/cleaner</code> কমান্ড ব্যবহার করুন।"
    )

    # ইনলাইন কীবোর্ড তৈরি
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🧹 Open Cleaner Settings",
                    callback_data="ac_refresh" # এটি সরাসরি auto_cleaner.py এর মেনু খুলবে
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

    await message.reply_text(
        text,
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True
    )

    LOGGER.info("Start command executed by Owner: %s", message.from_user.id)
