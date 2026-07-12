from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)
from config import TOKEN

from handlers import (
    menu,
    tambah_pemasukan,
    tambah_pengeluaran,
    input_nominal,
    pilih_kategori,
    saldo_menu,
    statistik_menu
)

app = Flask(__name__)

@app.get("/")
def home():
    return "Money Tracker Bot is running!"

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )