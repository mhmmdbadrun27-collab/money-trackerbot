from telegram import Update
from telegram.ext import ContextTypes

from keyboards import (
    main_keyboard,
    kategori_keyboard,
 )

from utils import rupiah

from database import (
    simpan_transaksi,
    statistik,
    saldo
)

user_data = {}
async def menu(update):

    user_id = update.effective_user.id
    text = update.message.text

    if text != "Menu":
        return False

    user_data.pop(user_id, None)

    await update.message.reply_text(
        "Menu Utama",
        reply_markup=main_keyboard
    )

    return True

async def tambah_pemasukan(update):

    user_id = update.effective_user.id
    text = update.message.text

    if text != "Tambah Pemasukan":
        return False

    user_data[user_id] = {
        "mode": "pemasukan",
        "step": "nominal"
    }

    await update.message.reply_text(
        "Masukkan nominal pemasukan."
    )

    return True

async def tambah_pengeluaran(update):

    user_id = update.effective_user.id
    text = update.message.text

    if text != "Tambah Pengeluaran":
        return False

    user_data[user_id] = {
        "mode": "pengeluaran",
        "step": "nominal"
    }

    await update.message.reply_text(
        "Masukkan nominal pengeluaran.\n\nContoh:\n25000"
    )

    return True

async def input_nominal(update):

    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_data:
        return False

    if user_data[user_id]["step"] != "nominal":
        return False

    try:

        nominal = int(
            text.replace(".", "").replace(",", "")
        )

    except:

        await update.message.reply_text(
            "❌ Nominal tidak valid.\n\nContoh:\n25000"
        )

        return True

    user_data[user_id]["nominal"] = nominal

    # Jika pengeluaran lanjut pilih kategori
    if user_data[user_id]["mode"] == "pengeluaran":

        user_data[user_id]["step"] = "kategori"

        await update.message.reply_text(
            f"💰 Nominal : {rupiah(nominal)}\n\n"
            "Pilih kategori.",
            reply_markup=kategori_keyboard
        )

        return True

    # Jika pemasukan langsung simpan
    if user_data[user_id]["mode"] == "pemasukan":

        simpan_transaksi(
            user_id,
            update.effective_user.full_name,
            nominal,
            "Pemasukan",
            "-"
        )

        user_data.pop(user_id)
        sisa = saldo(user_id)

        await update.message.reply_text(
    f"""✅ Pemasukan berhasil disimpan

💵 {rupiah(nominal)}

━━━━━━━━━━━━━━
💳 Saldo Saat Ini

{rupiah(sisa)}
""",
    reply_markup=main_keyboard
)

        return True

async def pilih_kategori(update):

    user_id = update.effective_user.id
    text = update.message.text

    kategori = {
        "Makan": "Makan",
        "Transportasi": "Transportasi",
        "Belanja": "Belanja",
        "Lainnya": "Lainnya"
    }

    if user_id not in user_data:
        return False

    if user_data[user_id]["step"] != "kategori":
        return False

    if text not in kategori:

        await update.message.reply_text(
            "Silakan pilih kategori menggunakan tombol."
        )

        return True

    simpan_transaksi(
        user_id,
        update.effective_user.full_name,
        user_data[user_id]["nominal"],
        "Pengeluaran",
        kategori[text]
    )

    nominal = user_data[user_id]["nominal"]
    sisa = saldo(user_id
                 )
    user_data.pop(user_id)

    await update.message.reply_text(
    f"""✅ Pengeluaran berhasil disimpan

{rupiah(nominal)}

{kategori[text]}

━━━━━━━━━━━━━━
Sisa Saldo

{rupiah(sisa)}
""",
    reply_markup=main_keyboard
)

    return True

async def statistik_menu(update):

    user_id = update.effective_user.id
    text = update.message.text

    if text != "Statistik":
        return False

    data = statistik(user_id)

    if len(data) == 0:

        await update.message.reply_text(
            "Belum ada data pengeluaran.",
            reply_markup=main_keyboard
        )

        return True

    pesan = "Statistik Pengeluaran\n\n"

    total = 0

    for kategori, jumlah in data:

        pesan += f"{kategori}\n{rupiah(jumlah)}\n\n"
        total += jumlah

    pesan += "────────────────\n"
    pesan += f"Total\n{rupiah(total)}"

    await update.message.reply_text(
        pesan,
        reply_markup=main_keyboard
    )

    return True

async def saldo_menu(update):

    user_id = update.effective_user.id
    text = update.message.text

    if text != "Saldo":
        return False

    total = saldo(user_id)

    await update.message.reply_text(
        f"""Saldo Anda

{rupiah(total)}
""",
        reply_markup=main_keyboard
    )

    return True