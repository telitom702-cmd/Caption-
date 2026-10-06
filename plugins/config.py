import os

class Config:
    API_ID = int(os.environ.get("API_ID", 24776633))
    API_HASH = os.environ.get("API_HASH", "আপনার_API_HASH_দিন")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "আপনার_BOT_TOKEN_দিন")
    OWNER_ID = int(os.environ.get("OWNER_ID", 123456789)) # আপনার টেলিগ্রাম আইডি
