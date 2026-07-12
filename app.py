import os
import threading

from flask import Flask
from bot import main

app = Flask(__name__)

@app.get("/")
def home():
    return "Money Tracker Bot is running!"

if __name__ == "__main__":

    bot_thread = threading.Thread(
        target=main,
        daemon=True
    )

    bot_thread.start()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )