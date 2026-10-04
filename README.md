# Duplicate Check Bot

Features:
- Duplicate file checking using Telegram file_unique_id
- Duplicate log to LOG_CHANNEL
- File name, link, unique ID and caption in log
- Rotating local error log: logs/bot.log
- Modular plugins for future features

Environment:
SESSION
API_ID
API_HASH
BOT_TOKEN
MONGO_URI
LOG_CHANNEL

Run:
python bot.py

When something fails, check:
logs/bot.log

Every major handler uses logger.exception(), so traceback and exact error are recorded.
