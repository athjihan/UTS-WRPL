import streamlit as st
from database import get_connection

st.title("🔍 Cari Event")

search = st.text_input("Masukkan nama event:")

if search:
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Events WHERE nama_event LIKE %s", (f"%{search}%",))
        results = cursor.fetchall()
        if results:
            for row in results:
                st.subheader(row['nama_event'])
                st.write(f"Kategori: {row['kategori']}")
                st.write(f"Lokasi: {row['lokasi']}")
                st.write(f"Tanggal: {row['tanggal']}")
        else:
            st.warning("Event tidak ditemukan.")
