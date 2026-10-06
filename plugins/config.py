import os


class Config:
    API_ID = int(os.environ.get("API_ID", "24776633"))
    API_HASH = os.environ.get(
        "API_HASH",
        "57b1f632044b4e718f5dce004a988d69"
    )
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    OWNER_ID = int(os.environ.get("OWNER_ID", "8248792819"))

    # Web Service Port
    PORT = int(os.environ.get("PORT", "8080"))
