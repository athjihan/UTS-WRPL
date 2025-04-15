import streamlit as st
from database import get_connection
import qrcode
import io
import uuid
import pandas as pd

st.title("📝 Transaksi Tiket")

conn = get_connection()
with conn.cursor() as cursor:
    cursor.execute("SELECT * FROM Events")
    events = cursor.fetchall()

event_names = [f"{e['nama_event']} - {e['tanggal']}" for e in events]
selected = st.selectbox("Pilih Event", event_names)

if selected:
    selected_event = events[event_names.index(selected)]

    st.write("### Isi Data Pemesan")
    nama = st.text_input("Nama Lengkap")
    email = st.text_input("Email")
    jumlah = st.number_input("Jumlah Tiket", min_value=1, step=1)

    if st.button("Pesan Tiket"):
        if nama and email:
            kode_pemesanan = str(uuid.uuid4())[:8]
            cursor.execute("""
                INSERT INTO Transaksi (kode_pemesanan, nama_pemesan, email, event_id, jumlah, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (kode_pemesanan, nama, email, selected_event['id'], jumlah, 'Belum Dibayar'))
            conn.commit()

            # Buat QR Code
            qr_data = f"Pemesanan: {kode_pemesanan}"
            img = qrcode.make(qr_data)
            buf = io.BytesIO()
            img.save(buf)
            st.image(buf.getvalue(), caption="QR Code Pemesanan")

            st.success(f"Pemesanan berhasil! Kode: {kode_pemesanan}")
        else:
            st.warning("Harap isi semua data.")
