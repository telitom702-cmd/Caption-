import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pyrogram import Client
from plugins.config import Config

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# ---------------------------------------------------------
# Dummy Web Server for Render Port Binding
# ---------------------------------------------------------
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def start_dummy_server():
    # Render সাধারণত PORT এনভায়রনমেন্ট ভ্যারিয়েবল দিয়ে দেয়
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    server.serve_forever()
# ---------------------------------------------------------

plugins = dict(root="plugins")

app = Client(
    "@UploaderXNTBot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    sleep_threshold=300,
    plugins=plugins
)

if __name__ == "__main__":
    # ১. ব্যাকগ্রাউন্ডে ফেইক সার্ভার চালু করা
    server_thread = threading.Thread(target=start_dummy_server, daemon=True)
    server_thread.start()
    logging.info(f"Dummy web server started on port {os.environ.get('PORT', 8000)}")

    # ২. মূল টেলিগ্রাম বট চালু করা
    app.run()
