from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TOKEN

from keyboards import main_keyboard

from handlers import (
    menu,
    tambah_pemasukan,
    tambah_pengeluaran,
    input_nominal,
    pilih_kategori,
    statistik_menu,
    saldo_menu
   )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(

"""💰 Money Tracker

Selamat datang.

Bot ini membantu mencatat arus keuangan Anda.

Silakan pilih menu di bawah.""",

reply_markup=main_keyboard
)
    
# HANDLE MESSAGE

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

      # MENU UTAMA
    if await menu(update):
        return

    # TAMBAH PEMASUKAN
    if await tambah_pemasukan(update):
        return
    
    # TAMBAH PENGELUARAN
    if await tambah_pengeluaran(update):
        return

    # INPUT NOMINAL
    if await input_nominal(update):
        return
   
    # PILIH KATEGORI
    if await pilih_kategori(update):
        return
 
    # SALDO
    if await saldo_menu(update):
        return

    # STATISTIK
    if await statistik_menu(update):
        return

    # DEFAULT
    await update.message.reply_text(
        "Silakan pilih menu menggunakan tombol di bawah.",
        reply_markup=main_keyboard
    )

# MAIN

def main():

    print("=" * 40)
    print("Money Tracker Bot Berjalan...")
    print("=" * 40)

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()

   