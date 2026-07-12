import sqlite3
import requests
from datetime import datetime

from config import SCRIPT_URL

conn = sqlite3.connect("expenses.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    nominal INTEGER,
    tipe TEXT,
    kategori TEXT,
    tanggal TEXT
)
""")

conn.commit()

def simpan_transaksi(user_id, username, nominal, tipe, kategori):

    cursor.execute(
        """
        INSERT INTO transactions
        (user_id, nominal, tipe, kategori, tanggal)
        VALUES (?,?,?,?,?)
        """,
        (
            user_id,
            nominal,
            tipe,
            kategori,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()

    try:

        response = requests.post(
            SCRIPT_URL,
            json={
                "user_id": user_id,
                "username": username,
                "tipe": tipe,
                "kategori": kategori,
                "nominal": nominal
            },
            timeout=10
        )

        print(response.status_code)

    except Exception as e:
        print(e)
        
def statistik(user_id):

    cursor.execute(
         """
    SELECT kategori, SUM(nominal)
    FROM transactions
    WHERE user_id=? AND tipe='Pengeluaran'
    GROUP BY kategori
    """,
    (user_id,)
    )

    return cursor.fetchall()

def saldo(user_id):

    cursor.execute("""
        SELECT
            SUM(CASE
                    WHEN tipe='Pemasukan'
                    THEN nominal
                    ELSE 0
                END),

            SUM(CASE
                    WHEN tipe='Pengeluaran'
                    THEN nominal
                    ELSE 0
                END)

        FROM transactions
        WHERE user_id=?
    """, (user_id,))

    pemasukan, pengeluaran = cursor.fetchone()

    pemasukan = pemasukan or 0
    pengeluaran = pengeluaran or 0

    return pemasukan - pengeluaran