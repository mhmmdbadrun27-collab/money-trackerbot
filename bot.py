from telegram import Update

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TOKEN

from telegram_handlers import (
    start,
    handle_message
)

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

   