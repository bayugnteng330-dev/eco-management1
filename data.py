import sqlite3
import pandas as pd

NAMA_DATABASE = "database.db"


def koneksi():
    return sqlite3.connect(NAMA_DATABASE)


def buat_tabel():
    with koneksi() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sampah (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                kategori TEXT NOT NULL,
                berat REAL NOT NULL,
                tanggal TEXT NOT NULL,
                keterangan TEXT
            )
        """)


def tambah_data(nama, kategori, berat, tanggal, keterangan):
    with koneksi() as conn:
        conn.execute("""
            INSERT INTO sampah
            (nama, kategori, berat, tanggal, keterangan)
            VALUES (?, ?, ?, ?, ?)
        """, (nama, kategori, berat, tanggal, keterangan))


def ambil_data():
    with koneksi() as conn:
        return pd.read_sql_query(
            "SELECT * FROM sampah ORDER BY id DESC",
            conn
        )


def ubah_data(id_data, nama, kategori, berat, tanggal, keterangan):
    with koneksi() as conn:
        conn.execute("""
            UPDATE sampah
            SET nama = ?, kategori = ?, berat = ?,
                tanggal = ?, keterangan = ?
            WHERE id = ?
        """, (
            nama,
            kategori,
            berat,
            tanggal,
            keterangan,
            id_data
        ))


def hapus_data(id_data):
    with koneksi() as conn:
        conn.execute(
            "DELETE FROM sampah WHERE id = ?",
            (id_data,)
        )
