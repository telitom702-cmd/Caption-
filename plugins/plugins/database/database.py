import os
import logging
import motor.motor_asyncio

LOGGER = logging.getLogger(__name__)

# যদি ডেটাবেস URL এনভায়রনমেন্টে না থাকে, লোকাল ডিফল্ট দিয়ে চালু হবে
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")

class Database:
    def __init__(self):
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
            self.db = self.client["telegram_auto_cleaner_db"]
            LOGGER.info("MongoDB Connected Successfully!")
        except Exception as e:
            LOGGER.error(f"MongoDB Connection Failed: {e}")
            self.db = None

# এটি অন্যান্য ফাইলে import করার জন্য ব্যবহৃত হবে
db = Database()
