# এখানে আগের auto_cleaner.py কোডটি থাকবে। 
# শুধু নিচের channel_settings import এবং Text Input অংশটুকু যুক্ত করে নেবেন।

import re
import html
import logging
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.database.database import db
from plugins.config import Config
from plugins.channel_settings import (
    get_channels, get_deleted_channels, is_channel_deleted, 
    is_channel_enabled, register_channel, cancel_channel_state, 
    add_channel, CHANNEL_STATE # এখানে CHANNEL_STATE এবং add_channel import করা হয়েছে
)

# ... (আগের কোডগুলো এখানে থাকবে) ...

@Client.on_message(
    filters.private
    & filters.text
    & ~filters.command([ "cancel", "start", "cleaner", "oldclean" ])
)
async def cleaner_text_input(client, message):
    if not message.from_user: return
    if message.from_user.id != OWNER_ID: return

    user_id = message.from_user.id
    state = CLEANER_STATE.get(user_id)
    channel_state = CHANNEL_STATE.get(user_id)

    # --- ADD CHANNEL ---
    if channel_state == "add_channel":
        value = message.text.strip()
        if not re.fullmatch(r"-100\d{5,}", value):
            await message.reply_text("⚠️ সঠিক Channel ID দিন।\n\nউদাহরণ:\n<code>-1001234567890</code>\n\nআবার চেষ্টা করুন অথবা /cancel দিন।", parse_mode=enums.ParseMode.HTML)
            return

        chat_id = int(value)
        try:
            chat = await client.get_chat(chat_id)
        except Exception as e:
            LOGGER.error("Channel verification failed: %s", e)
            await message.reply_text("❌ Channel পাওয়া যাচ্ছে না।\n\nচেক করুন:\n• Channel ID সঠিক কিনা\n• Bot ওই Channel-এ আছে কিনা")
            return

        try:
            me = await client.get_me()
            member = await client.get_chat_member(chat_id, me.id)
            if member.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
                await message.reply_text("⚠️ Bot এই Channel-এর Admin নয়। প্রথমে Bot-কে Channel-এর Admin করুন।")
                return
        except Exception as e:
            LOGGER.warning("Could not verify bot admin status: %s", e)

        await add_channel(chat_id, True)
        CHANNEL_STATE.pop(user_id, None)
        channel_title = getattr(chat, "title", None) or "Unknown Channel"

        await message.reply_text(
            "✅ <b>Channel Added Successfully</b>\n\n"
            f"📢 Name: <b>{html.escape(str(channel_title))}</b>\n"
            f"🆔 ID: <code>{chat_id}</code>\n"
            "📊 Status: <b>🟢 ON</b>",
            parse_mode=enums.ParseMode.HTML
        )
        return

    # --- ADD REMOVE TEXT ---
    if state == "add_text":
        value = message.text.strip()
        if not value:
            await message.reply_text("⚠️ Empty text দেওয়া যাবে না।")
            return

        await add_remove_text(value)
        CLEANER_STATE.pop(user_id, None)
        await message.reply_text("✅ <b>Remove Text Added</b>\n\n" f"<code>{html.escape(value)}</code>", parse_mode=enums.ParseMode.HTML)
        return
