import streamlit as st
from database import get_connection
import pandas as pd

st.title("💳 Konfirmasi Pembayaran")

kode = st.text_input("Masukkan Kode Pemesanan")

if kode:
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT T.kode_pemesanan, T.nama_pemesan, T.email, T.jumlah, T.status, E.nama_event, E.tanggal, E.lokasi
            FROM Transaksi T JOIN Events E ON T.event_id = E.id
            WHERE T.kode_pemesanan = %s
        """, (kode,))
        data = cursor.fetchone()

        if data:
            st.write("### Detail Pesanan")
            st.json(data)

            if data["status"] == "Belum Dibayar":
                if st.button("Konfirmasi Pembayaran"):
                    cursor.execute("UPDATE Transaksi SET status='Sudah Dibayar' WHERE kode_pemesanan=%s", (kode,))
                    conn.commit()
                    st.success("Pembayaran berhasil dikonfirmasi!")
            else:
                st.success("Pembayaran sudah dikonfirmasi.")
        else:
            st.error("Kode pemesanan tidak ditemukan.")
