from telegram import ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(
    [
        ["Tambah Pemasukan", "Tambah Pengeluaran"],
        ["Saldo", "Statistik"],
    ],
    resize_keyboard=True
)

kategori_keyboard = ReplyKeyboardMarkup(
    [
        ["Makan", "Transportasi"],
        ["Belanja", "Lainnya"],
        ["Menu"]
    ],
    resize_keyboard=True
)