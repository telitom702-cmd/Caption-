# ============================================================
# Telegram Auto Cleaner - Channel Settings
# File: plugins/channel_settings.py
# ============================================================

import re
import html
import logging

from pyrogram import Client, filters, enums
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from plugins.database.database import db
from plugins.config import Config

LOGGER = logging.getLogger(__name__)

COLLECTION_NAME = "auto_cleaner"
cleaner_col = db.db[COLLECTION_NAME]

OWNER_ID = Config.OWNER_ID

CHANNEL_STATE = {}

async def get_settings():
    data = await cleaner_col.find_one({"_id": "settings"})
    if not data:
        return {
            "_id": "settings", "enabled": False,
            "caption_cleaner": True, "filename_cleaner": False,
            "remove_texts": [], "channels": {}, "deleted_channels": []
        }
    changed = False
    if "channels" not in data: data["channels"] = {}; changed = True
    if "deleted_channels" not in data: data["deleted_channels"] = []; changed = True
    if changed:
        await cleaner_col.update_one({"_id": "settings"}, {"$set": {"channels": data["channels"], "deleted_channels": data["deleted_channels"]}}, upsert=True)
    return data

async def update_settings(data):
    await cleaner_col.update_one({"_id": "settings"}, {"$set": data}, upsert=True)

async def get_channels():
    return (await get_settings()).get("channels", {})

async def get_deleted_channels():
    return (await get_settings()).get("deleted_channels", [])

async def is_channel_deleted(chat_id):
    deleted = await get_deleted_channels()
    return str(chat_id) in [str(x) for x in deleted]

async def is_channel_enabled(chat_id):
    channels = await get_channels()
    return bool(channels.get(str(chat_id), False))

async def set_channel_status(chat_id, status):
    settings = await get_settings()
    channels = settings.get("channels", {})
    channels[str(chat_id)] = bool(status)
    await update_settings({"channels": channels})

async def add_channel(chat_id, status=True):
    settings = await get_settings()
    channels = settings.get("channels", {})
    deleted = settings.get("deleted_channels", [])
    channels[str(chat_id)] = bool(status)
    deleted = [str(x) for x in deleted if str(x) != str(chat_id)]
    await update_settings({"channels": channels, "deleted_channels": deleted})

async def delete_channel(chat_id):
    settings = await get_settings()
    channels = settings.get("channels", {})
    deleted = settings.get("deleted_channels", [])
    channels.pop(str(chat_id), None)
    if str(chat_id) not in [str(x) for x in deleted]:
        deleted.append(str(chat_id))
    await update_settings({"channels": channels, "deleted_channels": deleted})

async def register_channel(message):
    if not message.chat: return False
    chat_id = str(message.chat.id)
    if await is_channel_deleted(chat_id): return False
    settings = await get_settings()
    channels = settings.get("channels", {})
    if chat_id not in channels:
        channels[chat_id] = True
        await update_settings({"channels": channels})
        LOGGER.info("New channel auto-registered: %s", chat_id)
    return True

async def channel_settings_text():
    channels = await get_channels()
    if not channels: return "📢 <b>Channel Settings</b>\n\nএখনো কোনো channel add হয়নি।\n\n➕ Add Channel চাপুন।"
    lines = []
    for chat_id, status in channels.items():
        status_text = "🟢 ON" if status else "🔴 OFF"
        lines.append(f"📢 <code>{html.escape(str(chat_id))}</code> — <b>{status_text}</b>")
    return "📢 <b>Channel Settings</b>\n\n" + "\n".join(lines) + "\n\nপ্রতিটি Channel আলাদাভাবে ON/OFF বা Delete করা যাবে।"

async def channel_settings_keyboard():
    channels = await get_channels()
    buttons = []
    for chat_id, status in channels.items():
        chat_id = str(chat_id)
        status_button = "🔴 Turn OFF" if status else "🟢 Turn ON"
        buttons.append([
            InlineKeyboardButton(status_button, callback_data=f"ac_ch_toggle:{chat_id}"),
            InlineKeyboardButton("🗑️ Delete", callback_data=f"ac_ch_delete:{chat_id}")
        ])
        buttons.append([InlineKeyboardButton("🧹 Clean Old Posts", callback_data=f"ac_old_channel:{chat_id}")])
    buttons.append([InlineKeyboardButton("➕ Add Channel", callback_data="ac_ch_add")])
    buttons.append([InlineKeyboardButton("🔄 Refresh", callback_data="ac_channels"), InlineKeyboardButton("🔙 Back", callback_data="ac_refresh")])
    return InlineKeyboardMarkup(buttons)

@Client.on_callback_query(filters.regex(r"^ac_(channels|ch_)"))
async def channel_settings_callback(client, query):
    if query.from_user.id != OWNER_ID:
        return await query.answer("এটি শুধুমাত্র এডমিনের জন্য!", show_alert=True)
    
    user_id = query.from_user.id
    data = query.data

    if data == "ac_channels":
        await query.message.edit_text(await channel_settings_text(), reply_markup=await channel_settings_keyboard(), parse_mode=enums.ParseMode.HTML)
        await query.answer()
        return

    if data == "ac_ch_add":
        CHANNEL_STATE[user_id] = "add_channel"
        await query.message.edit_text(
            "➕ <b>Add Channel</b>\n\nChannel ID পাঠান।\n\nউদাহরণ:\n<code>-1001234567890</code>\n\n⚠️ Bot-কে ওই Channel-এর Admin হতে হবে।\n\nCancel করতে /cancel পাঠান।",
            parse_mode=enums.ParseMode.HTML
        )
        await query.answer()
        return

    if data.startswith("ac_ch_toggle:"):
        chat_id = data.split(":", 1)[1]
        channels = await get_channels()
        if chat_id not in channels: return await query.answer("Channel not found!", show_alert=True)
        await set_channel_status(chat_id, not bool(channels[chat_id]))
        await query.answer("Channel status updated!")
        await query.message.edit_text(await channel_settings_text(), reply_markup=await channel_settings_keyboard(), parse_mode=enums.ParseMode.HTML)
        return

    if data.startswith("ac_ch_delete:"):
        chat_id = data.split(":", 1)[1]
        await query.message.edit_text(
            f"⚠️ <b>Delete Channel?</b>\n\nChannel ID:\n<code>{html.escape(chat_id)}</code>\n\nDelete করলে Channel Settings থেকে channel মুছে যাবে এবং নতুন post এলে automatically আবার add হবে না।",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Yes, Delete", callback_data=f"ac_ch_confirm_delete:{chat_id}"), InlineKeyboardButton("❌ Cancel", callback_data="ac_channels")]
            ]),
            parse_mode=enums.ParseMode.HTML
        )
        await query.answer()
        return

    if data.startswith("ac_ch_confirm_delete:"):
        chat_id = data.split(":", 1)[1]
        await delete_channel(chat_id)
        await query.answer("Channel deleted successfully!")
        await query.message.edit_text(await channel_settings_text(), reply_markup=await channel_settings_keyboard(), parse_mode=enums.ParseMode.HTML)
        return

async def cancel_channel_state(user_id):
    if user_id in CHANNEL_STATE:
        CHANNEL_STATE.pop(user_id, None)
        return True
    return False
