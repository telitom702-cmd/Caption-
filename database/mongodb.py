from motor.motor_asyncio import AsyncIOMotorClient
from info import MONGO_URI
from utils.logger import logger

_client = None
_db = None
_files = None

def init_db():
    global _client, _db, _files
    if not MONGO_URI:
        logger.warning("MONGO_URI is empty; database features are disabled")
        return
    try:
        _client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        _db = _client["duplicate_check_bot"]
        _files = _db["files"]
        logger.info("MongoDB initialized")
    except Exception:
        logger.exception("MongoDB initialization failed")

async def find_file(unique_id):
    if _files is None: return None
    try:
        return await _files.find_one({"file_unique_id": unique_id})
    except Exception:
        logger.exception("MongoDB find_file failed: %s", unique_id)
        return None

async def save_file(data):
    if _files is None: return False
    try:
        await _files.update_one({"file_unique_id": data["file_unique_id"]}, {"$set": data}, upsert=True)
        return True
    except Exception:
        logger.exception("MongoDB save_file failed")
        return False
