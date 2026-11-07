import streamlit as st
import textwrap
import pandas as pd
from datetime import date
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from data import buat_tabel, tambah_data, ambil_data, ubah_data, hapus_data
from statistik import ringkasan, grafik_kategori, grafik_bulanan


# KONFIGURASI HALAMAN

st.set_page_config(
    page_title="Eco Management",
    page_icon="♻️",
    layout="wide"
)


# LOAD CSS

def load_css():
    with open("style.css", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

    st.markdown("""
    <style>
    /* RESPONSIVE MOBILE */
    @media screen and (max-width: 768px) {

        .stApp [data-testid="stMainBlockContainer"] {
            padding: 1rem 0.8rem 2rem 0.8rem !important;
            max-width: 100% !important;
            width: 100% !important;
        }

        .stApp [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 0.75rem !important;
        }

        .stApp [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            flex: 1 1 100% !important;
            width: 100% !important;
            min-width: 100% !important;
        }

        .stApp h1 {
            font-size: 1.65rem !important;
            line-height: 1.25 !important;
            overflow-wrap: anywhere !important;
        }

        .stApp h2 {
            font-size: 1.35rem !important;
        }

        .stApp h3 {
            font-size: 1.1rem !important;
        }

        .stApp p {
            overflow-wrap: anywhere !important;
        }

        .stApp [data-testid="stMetric"] {
            padding: 0.85rem !important;
            min-width: 0 !important;
            width: 100% !important;
        }

        .stApp [data-testid="stMetricValue"] {
            font-size: 1.35rem !important;
            overflow-wrap: anywhere !important;
        }

        .stApp [data-testid="stPlotlyChart"] {
            width: 100% !important;
            max-width: 100% !important;
            overflow: hidden !important;
        }

        .stApp [data-testid="stPlotlyChart"] iframe {
            max-width: 100% !important;
        }

        .stApp [data-testid="stDataFrame"],
        .stApp [data-testid="stTable"] {
            max-width: 100% !important;
            width: 100% !important;
            overflow-x: auto !important;
        }

        .stApp button,
        .stApp [data-testid="stDownloadButton"] button {
            width: 100% !important;
            min-height: 42px !important;
        }

        .stApp input,
        .stApp textarea,
        .stApp select {
            font-size: 16px !important;
            max-width: 100% !important;
        }

        .stApp [data-testid="stForm"] {
            width: 100% !important;
            padding: 0 !important;
        }

        .stApp section[style*="linear-gradient"] {
            padding: 25px 18px !important;
            border-radius: 16px !important;
        }

        .stApp section[style*="linear-gradient"] h1 {
            font-size: 1.8rem !important;
            line-height: 1.25 !important;
        }

        .stApp section[style*="linear-gradient"] p {
            font-size: 0.92rem !important;
            line-height: 1.6 !important;
        }

        [data-testid="stSidebar"] {
            min-width: 0 !important;
            max-width: 85vw !important;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
            font-size: 1.2rem !important;
        }

        .stApp [data-testid="stVerticalBlock"] {
            gap: 0.8rem;
        }

        html,
        body,
        [data-testid="stAppViewContainer"] {
            max-width: 100% !important;
            overflow-x: hidden !important;
        }
    }

    /* TABLET */
    @media screen and (min-width: 769px) and (max-width: 1024px) {
        .stApp [data-testid="stMainBlockContainer"] {
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


load_css()


# DATABASE

buat_tabel()


# SIDEBAR

with st.sidebar:

    st.markdown(textwrap.dedent("""
    <div style="text-align:center; padding:20px 5px;">
        <div style="font-size:55px;">♻️</div>
        <h2 style="color:#34D399;">ECO MANAGEMENT</h2>
        <p style="color:#94A3B8; font-size:12px;">
            Waste Management System
        </p>
    </div>
    """), unsafe_allow_html=True)

    st.divider()

    menu = st.radio(
        "MENU UTAMA",
        [
            "Dashboard",
            "Tambah Data",
            "Data Sampah",
            "Statistik & Grafik",
            "Laporan",
            "Tentang Aplikasi"
        ]
    )

    st.divider()

    st.markdown(textwrap.dedent("""
    <div style="text-align:center; color:#94A3B8; font-size:12px;">
        ECO MANAGEMENT SYSTEM<br>
        Python & Streamlit
    </div>
    """), unsafe_allow_html=True)


# AMBIL DATA

data = ambil_data()


# HEADER

st.markdown(textwrap.dedent("""
<div style="
    background:linear-gradient(120deg,#064E3B,#102A36);
    padding:22px 25px;
    border-radius:15px;
    border:1px solid #10B981;
    margin-bottom:25px;
">
    <h1 style="color:#34D399; margin:0;">
        ♻️ ECO MANAGEMENT
    </h1>
    <p style="color:#D1FAE5; margin:8px 0 0 0;">
        Sistem Pengelolaan dan Monitoring Sampah
    </p>
</div>
"""), unsafe_allow_html=True)


# DASHBOARD

if menu == "Dashboard":

    total = float(data["berat"].sum()) if not data.empty else 0
    organik = float(data.loc[data["kategori"] == "Organik", "berat"].sum()) if not data.empty else 0
    anorganik = float(data.loc[data["kategori"] == "Anorganik", "berat"].sum()) if not data.empty else 0
    b3 = float(data.loc[data["kategori"] == "B3", "berat"].sum()) if not data.empty else 0

    bulan_ini = pd.DataFrame()

    if not data.empty:
        tanggal_data = pd.to_datetime(data["tanggal"], errors="coerce")
        bulan_ini = data[tanggal_data.dt.to_period("M") == pd.Timestamp.today().to_period("M")]

    total_bulan = float(bulan_ini["berat"].sum()) if not bulan_ini.empty else 0
    rata_rata = total / len(data) if not data.empty else 0
    kategori_terbanyak = data.groupby("kategori")["berat"].sum().idxmax() if not data.empty else "-"

    st.markdown(textwrap.dedent("""
    <section style="background:linear-gradient(120deg,#052e2b 0%,#064e3b 48%,#102a36 100%);padding:42px 38px;border:1px solid #10b981;border-radius:22px;margin:8px 0 28px;position:relative;overflow:hidden;">
        <div style="color:#6ee7b7;font-size:12px;font-weight:700;letter-spacing:3px;margin-bottom:14px;">♻️ SMART WASTE MANAGEMENT</div>
        <h1 style="color:#ecfdf5;font-size:42px;line-height:1.15;margin:0 0 14px;font-weight:800;">Kelola Sampah,<br><span style="color:#34d399;">Ciptakan Lingkungan</span> Lebih Baik.</h1>
        <p style="color:#cbd5e1;font-size:16px;max-width:680px;line-height:1.8;margin-bottom:0;">Pantau pencatatan, kategori, dan perkembangan sampah dalam satu dashboard digital yang praktis dan terorganisir.</p>
        <div style="margin-top:25px;display:flex;gap:10px;flex-wrap:wrap;">
            <span style="background:#10b981;color:#052e2b;padding:10px 17px;border-radius:9px;font-weight:700;font-size:13px;">● SISTEM AKTIF</span>
            <span style="background:#ffffff12;color:#d1fae5;border:1px solid #ffffff25;padding:10px 17px;border-radius:9px;font-size:13px;">DATABASE TERINTEGRASI</span>
        </div>
    </section>
    """), unsafe_allow_html=True)

    st.markdown("<div style='font-size:12px;letter-spacing:2px;color:#34d399;font-weight:700;margin:8px 0 14px;'>OVERVIEW • RINGKASAN DATA</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("♻️ Total Sampah", f"{total:.2f} KG")
    col2.metric("📅 Bulan Ini", f"{total_bulan:.2f} KG")
    col3.metric("🗂️ Total Pencatatan", len(data))
    col4.metric("📊 Kategori Terbanyak", kategori_terbanyak)

    st.markdown("<br><div style='font-size:12px;letter-spacing:2px;color:#34d399;font-weight:700;margin-bottom:14px;'>KATEGORI SAMPAH</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    for col, icon, title, value, desc, accent in [
        (c1, "🌱", "Organik", organik, "Sisa bahan alami dan mudah terurai", "#34d399"),
        (c2, "♻️", "Anorganik", anorganik, "Plastik, botol, kertas, dan kaleng", "#60a5fa"),
        (c3, "⚠️", "B3", b3, "Bahan berbahaya dan beracun", "#fbbf24")
    ]:
        with col:
            st.markdown(textwrap.dedent(f"""
            <div style="background:#142538;border:1px solid #ffffff12;border-top:3px solid {accent};border-radius:14px;padding:20px 22px;min-height:145px;">
                <div style="font-size:25px;">{icon}</div>
                <div style="color:#94a3b8;font-size:13px;margin-top:8px;">Sampah {title}</div>
                <div style="color:{accent};font-size:27px;font-weight:800;margin:4px 0;">{value:.2f} <span style="font-size:13px;">KG</span></div>
                <div style="color:#94a3b8;font-size:12px;">{desc}</div>
            </div>
            """), unsafe_allow_html=True)

    st.markdown("<br><div style='font-size:12px;letter-spacing:2px;color:#34d399;font-weight:700;margin-bottom:14px;'>ANALISIS & MONITORING</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Komposisi Sampah")

        if not data.empty:
            st.plotly_chart(grafik_kategori(data), use_container_width=True)
        else:
            st.info("Belum ada data sampah. Tambahkan pencatatan untuk melihat komposisi.")

    with col2:
        st.markdown("### Perkembangan Sampah")

        if not data.empty:
            st.plotly_chart(grafik_bulanan(data), use_container_width=True)
        else:
            st.info("Grafik perkembangan akan tampil setelah data tersedia.")

    st.markdown("<br><div style='font-size:12px;letter-spacing:2px;color:#34d399;font-weight:700;margin-bottom:14px;'>AKTIVITAS TERBARU</div>", unsafe_allow_html=True)

    if not data.empty:
        st.dataframe(data.head(5), use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada aktivitas pencatatan. Mulai dengan menambahkan data sampah melalui menu Tambah Data.")

    st.markdown(textwrap.dedent("""
    <div style="margin-top:24px;padding:22px 25px;background:linear-gradient(110deg,#102a36,#064e3b);border:1px solid #166b52;border-radius:15px;text-align:center;">
        <div style="font-size:23px;margin-bottom:6px;">🌍</div>
        <div style="color:#6ee7b7;font-size:18px;font-weight:800;">Small Steps, Greener Future.</div>
        <div style="color:#cbd5e1;font-size:13px;margin-top:6px;">Pencatatan yang baik membantu pengelolaan sampah menjadi lebih terarah.</div>
    </div>
    """), unsafe_allow_html=True)


# TAMBAH DATA

elif menu == "Tambah Data":

    st.title("Tambah Data Sampah")
    st.caption("Masukkan informasi sampah yang ingin dicatat.")

    with st.form("form_tambah"):

        nama = st.text_input("Nama Sampah")

        col1, col2 = st.columns(2)

        with col1:
            kategori = st.selectbox(
                "Kategori Sampah",
                ["Organik", "Anorganik", "B3"]
            )

            berat = st.number_input(
                "Berat Sampah (KG)",
                min_value=0.01,
                step=0.5
            )

        with col2:
            tanggal = st.date_input(
                "Tanggal Pencatatan",
                value=date.today()
            )

        keterangan = st.text_area("Keterangan")

        submit = st.form_submit_button(
            "Simpan Data",
            use_container_width=True
        )

        if submit:

            if not nama.strip():
                st.error("Nama sampah harus diisi.")

            else:
                tambah_data(
                    nama,
                    kategori,
                    berat,
                    tanggal.isoformat(),
                    keterangan
                )

                st.success("Data sampah berhasil disimpan!")
                st.rerun()


# DATA SAMPAH

elif menu == "Data Sampah":

    st.title("Data Sampah")
    st.caption("Kelola seluruh data pencatatan sampah.")

    if not data.empty:

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("Edit Data Sampah")

        daftar_id = data["id"].tolist()

        id_edit = st.selectbox(
            "Pilih ID Data",
            daftar_id,
            key="edit_id"
        )

        data_edit = data[data["id"] == id_edit].iloc[0]

        with st.form("form_edit"):

            nama_edit = st.text_input(
                "Nama Sampah",
                value=str(data_edit["nama"])
            )

            col1, col2 = st.columns(2)

            with col1:
                kategori_edit = st.selectbox(
                    "Kategori",
                    ["Organik", "Anorganik", "B3"],
                    index=["Organik", "Anorganik", "B3"].index(
                        data_edit["kategori"]
                    )
                )

                berat_edit = st.number_input(
                    "Berat (KG)",
                    min_value=0.01,
                    value=float(data_edit["berat"]),
                    step=0.5
                )

            with col2:
                tanggal_edit = st.date_input(
                    "Tanggal",
                    value=date.fromisoformat(str(data_edit["tanggal"]))
                )

            keterangan_edit = st.text_area(
                "Keterangan",
                value=str(data_edit["keterangan"] or "")
            )

            update = st.form_submit_button(
                "Update Data",
                use_container_width=True
            )

            if update:

                if not nama_edit.strip():
                    st.error("Nama sampah harus diisi.")

                else:
                    ubah_data(
                        id_edit,
                        nama_edit,
                        kategori_edit,
                        berat_edit,
                        tanggal_edit.isoformat(),
                        keterangan_edit
                    )

                    st.success("Data berhasil diperbarui!")
                    st.rerun()

        st.divider()

        st.subheader("Hapus Data")

        id_hapus = st.selectbox(
            "Pilih ID yang ingin dihapus",
            daftar_id,
            key="hapus_id"
        )

        konfirmasi = st.checkbox(
            "Saya yakin ingin menghapus data ini."
        )

        if st.button("Hapus Data", use_container_width=True):

            if konfirmasi:
                hapus_data(id_hapus)

                st.success("Data berhasil dihapus!")
                st.rerun()

            else:
                st.warning("Centang konfirmasi terlebih dahulu.")

    else:
        st.info("Belum ada data sampah yang tersedia.")


# STATISTIK DAN GRAFIK

elif menu == "Statistik & Grafik":

    st.title("Statistik dan Grafik")
    st.caption("Analisis komposisi dan perkembangan sampah.")

    if not data.empty:

        total, organik, anorganik, b3 = ringkasan(data)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Sampah Berdasarkan Kategori")

            st.plotly_chart(
                grafik_kategori(data),
                use_container_width=True
            )

        with col2:
            st.subheader("Sampah Per Bulan")

            st.plotly_chart(
                grafik_bulanan(data),
                use_container_width=True
            )

        st.divider()

        st.subheader("Ringkasan Kategori")

        ringkas = data.groupby(
            "kategori",
            as_index=False
        )["berat"].sum()

        ringkas.columns = [
            "Kategori",
            "Total Berat (KG)"
        ]

        st.dataframe(
            ringkas,
            use_container_width=True,
            hide_index=True
        )

        st.success(
            f"Total keseluruhan sampah: {total:.2f} KG"
        )

    else:
        st.info("Belum ada data untuk ditampilkan.")


# LAPORAN

elif menu == "Laporan":

    st.title("Laporan Pengelolaan Sampah")
    st.caption("Buat dan unduh laporan pencatatan sampah.")

    if not data.empty:

        total, organik, anorganik, b3 = ringkasan(data)

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Sampah", f"{total:.2f} KG")
        col2.metric("Jumlah Data", len(data))
        col3.metric("Kategori", data["kategori"].nunique())

        st.divider()

        st.subheader("Pratinjau Laporan")

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

        def buat_pdf(data):

            buffer = BytesIO()

            dokumen = SimpleDocTemplate(
                buffer,
                pagesize=landscape(A4),
                rightMargin=30,
                leftMargin=30,
                topMargin=35,
                bottomMargin=35
            )

            elemen = []

            styles = getSampleStyleSheet()

            judul = ParagraphStyle(
                "Judul",
                parent=styles["Title"],
                textColor=colors.HexColor("#047857"),
                fontSize=20,
                alignment=1
            )

            elemen.append(
                Paragraph(
                    "LAPORAN PENGELOLAAN SAMPAH",
                    judul
                )
            )

            elemen.append(Spacer(1, 15))

            elemen.append(
                Paragraph(
                    f"Total Berat Sampah: {total:.2f} KG",
                    styles["Normal"]
                )
            )

            elemen.append(Spacer(1, 15))

            isi = [
                [
                    "ID",
                    "Nama Sampah",
                    "Kategori",
                    "Berat (KG)",
                    "Tanggal",
                    "Keterangan"
                ]
            ]

            for _, baris in data.iterrows():

                isi.append([
                    str(baris["id"]),
                    str(baris["nama"]),
                    str(baris["kategori"]),
                    str(baris["berat"]),
                    str(baris["tanggal"]),
                    str(baris["keterangan"] or "-")
                ])

            tabel = Table(
                isi,
                repeatRows=1,
                colWidths=[35, 130, 90, 75, 100, 200]
            )

            tabel.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0),
                     colors.HexColor("#047857")),

                    ("TEXTCOLOR", (0, 0), (-1, 0),
                     colors.white),

                    ("GRID", (0, 0), (-1, -1), 0.5,
                     colors.HexColor("#D1D5DB")),

                    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                     [colors.white, colors.HexColor("#ECFDF5")]),

                    ("PADDING", (0, 0), (-1, -1), 8),

                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
                ])
            )

            elemen.append(tabel)

            dokumen.build(elemen)

            buffer.seek(0)

            return buffer

        pdf = buat_pdf(data)

        st.download_button(
            label="📄 Download Laporan PDF",
            data=pdf,
            file_name="laporan_pengelolaan_sampah.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.download_button(
            label="📊 Download Data Excel (CSV)",
            data=data.to_csv(index=False).encode("utf-8"),
            file_name="data_pengelolaan_sampah.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:
        st.info("Belum ada data untuk dibuat menjadi laporan.")


# TENTANG APLIKASI

elif menu == "Tentang Aplikasi":

    # DESKRIPSI

    st.header("Tentang Aplikasi")

    st.write("""
    ECO MANAGEMENT merupakan aplikasi pengelolaan sampah
    berbasis Python yang dikembangkan untuk membantu proses
    pencatatan, pengelolaan, dan monitoring data sampah secara
    digital.

    Aplikasi ini dirancang untuk mempermudah pengguna dalam
    mencatat berbagai jenis sampah berdasarkan nama, kategori,
    berat, tanggal pencatatan, dan keterangan.

    Dengan adanya sistem ini, proses pengelolaan data sampah
    menjadi lebih terstruktur, efisien, dan mudah dipantau.
    """)

    st.divider()

    # LATAR BELAKANG

    st.header("Latar Belakang")

    st.write("""
    Sampah merupakan salah satu permasalahan lingkungan yang
    masih sering dijumpai dalam kehidupan sehari-hari.
    Meningkatnya aktivitas manusia menyebabkan jumlah sampah
    yang dihasilkan semakin bertambah.

    Pengelolaan sampah yang kurang terorganisir dapat
    menyebabkan pencemaran lingkungan dan berbagai
    permasalahan lainnya.

    Oleh karena itu, diperlukan sistem yang dapat membantu
    proses pencatatan dan pemantauan sampah secara lebih
    terstruktur.

    ECO MANAGEMENT dibuat sebagai solusi sederhana untuk
    membantu pengelolaan data sampah dengan memanfaatkan
    teknologi informasi.
    """)

    st.divider()

    # TUJUAN

    st.header("Tujuan Aplikasi")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(textwrap.dedent("""
        <div style="
            background:#142538;
            padding:22px;
            border-radius:14px;
            border-left:4px solid #10B981;
            min-height:180px;
        ">
            <h3 style="color:#34D399;">Tujuan Utama</h3>
            <p style="color:#CBD5E1;">
                Membantu proses pencatatan dan pengelolaan
                data sampah secara digital agar lebih
                terorganisir dan mudah dipantau.
            </p>
        </div>
        """), unsafe_allow_html=True)

    with col2:
        st.markdown(textwrap.dedent("""
        <div style="
            background:#142538;
            padding:22px;
            border-radius:14px;
            border-left:4px solid #3B82F6;
            min-height:180px;
        ">
            <h3 style="color:#60A5FA;">Tujuan Khusus</h3>
            <p style="color:#CBD5E1;">
                Menyediakan informasi mengenai jumlah,
                kategori, dan perkembangan sampah melalui
                statistik dan visualisasi grafik.
            </p>
        </div>
        """), unsafe_allow_html=True)

    st.divider()

    # MANFAAT

    st.header("Manfaat Aplikasi")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(textwrap.dedent("""
        <div style="background:#142538;padding:20px;border-radius:12px;text-align:center;min-height:175px;">
            <h2>📋</h2>
            <h4 style="color:#34D399;">Pencatatan</h4>
            <p style="color:#CBD5E1;">Mempermudah pencatatan data sampah.</p>
        </div>
        """), unsafe_allow_html=True)

    with col2:
        st.markdown(textwrap.dedent("""
        <div style="background:#142538;padding:20px;border-radius:12px;text-align:center;min-height:175px;">
            <h2>📊</h2>
            <h4 style="color:#34D399;">Monitoring</h4>
            <p style="color:#CBD5E1;">Memantau jumlah dan kategori sampah.</p>
        </div>
        """), unsafe_allow_html=True)

    with col3:
        st.markdown(textwrap.dedent("""
        <div style="background:#142538;padding:20px;border-radius:12px;text-align:center;min-height:175px;">
            <h2>📄</h2>
            <h4 style="color:#34D399;">Pelaporan</h4>
            <p style="color:#CBD5E1;">Mempermudah pembuatan laporan sampah.</p>
        </div>
        """), unsafe_allow_html=True)

    st.divider()

    # KATEGORI SAMPAH

    st.header("♻️ Kategori Sampah")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(textwrap.dedent("""
        <div style="background:#142538;padding:20px;border-radius:12px;border-top:4px solid #10B981;min-height:180px;">
            <h3 style="color:#34D399;">🌱 Organik</h3>
            <p style="color:#CBD5E1;">
                Sampah yang berasal dari bahan alami
                dan dapat terurai secara biologis.
            </p>
            <small style="color:#94A3B8;">
                Contoh: Daun, sisa makanan, kulit buah.
            </small>
        </div>
        """), unsafe_allow_html=True)

    with col2:
        st.markdown(textwrap.dedent("""
        <div style="background:#142538;padding:20px;border-radius:12px;border-top:4px solid #3B82F6;min-height:180px;">
            <h3 style="color:#60A5FA;">♻️ Anorganik</h3>
            <p style="color:#CBD5E1;">
                Sampah yang umumnya membutuhkan
                waktu lebih lama untuk terurai.
            </p>
            <small style="color:#94A3B8;">
                Contoh: Plastik, botol, kaleng.
            </small>
        </div>
        """), unsafe_allow_html=True)

    with col3:
        st.markdown(textwrap.dedent("""
        <div style="background:#142538;padding:20px;border-radius:12px;border-top:4px solid #F59E0B;min-height:180px;">
            <h3 style="color:#FBBF24;">⚠️ B3</h3>
            <p style="color:#CBD5E1;">
                Sampah yang mengandung bahan
                berbahaya dan beracun.
            </p>
            <small style="color:#94A3B8;">
                Contoh: Baterai bekas, lampu neon.
            </small>
        </div>
        """), unsafe_allow_html=True)

    st.divider()

    # FITUR

    st.header("⚙️ Fitur Utama Aplikasi")

    fitur = [
        ("🏠 Dashboard Monitoring", "Menampilkan ringkasan jumlah sampah dan informasi statistik."),
        ("➕ Tambah Data", "Menambahkan pencatatan sampah baru ke dalam database."),
        ("📦 Data Sampah", "Menampilkan, mengubah, dan menghapus data sampah."),
        ("📊 Statistik & Grafik", "Menyajikan visualisasi komposisi dan perkembangan sampah."),
        ("📄 Laporan", "Menyediakan laporan data sampah dalam format PDF dan CSV."),
        ("🗄️ Database", "Menyimpan data menggunakan SQLite agar dapat digunakan kembali.")
    ]

    for judul, deskripsi in fitur:
        st.markdown(textwrap.dedent(f"""
        <div style="
            background:#142538;
            padding:15px 20px;
            border-radius:10px;
            margin-bottom:10px;
            border-left:3px solid #10B981;
        ">
            <h4 style="color:#34D399;margin:0;">{judul}</h4>
            <p style="color:#CBD5E1;margin:6px 0 0 0;">
                {deskripsi}
            </p>
        </div>
        """), unsafe_allow_html=True)

    st.divider()

    # ALUR SISTEM

    st.header("🔄 Alur Kerja Sistem")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info("**01**\n\nInput Data\n\nPengguna memasukkan data sampah.")

    with col2:
        st.info("**02**\n\nPenyimpanan\n\nData disimpan ke SQLite.")

    with col3:
        st.info("**03**\n\nPengolahan\n\nData diolah menjadi statistik.")

    with col4:
        st.info("**04**\n\nLaporan\n\nInformasi ditampilkan dan dilaporkan.")

    st.divider()

    # TEKNOLOGI

    st.header("💻 Teknologi yang Digunakan")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(textwrap.dedent("""
        <div style="background:#142538;padding:18px;border-radius:12px;text-align:center;">
            <h2></h2>
            <h4 style="color:#34D399;">Python</h4>
            <p style="color:#CBD5E1;">Bahasa pemrograman utama.</p>
        </div>
        """), unsafe_allow_html=True)

    with col2:
        st.markdown(textwrap.dedent("""
        <div style="background:#142538;padding:18px;border-radius:12px;text-align:center;">
            <h2></h2>
            <h4 style="color:#34D399;">Streamlit</h4>
            <p style="color:#CBD5E1;">Framework antarmuka aplikasi.</p>
        </div>
        """), unsafe_allow_html=True)

    with col3:
        st.markdown(textwrap.dedent("""
        <div style="background:#142538;padding:18px;border-radius:12px;text-align:center;">
            <h2></h2>
            <h4 style="color:#34D399;">SQLite</h4>
            <p style="color:#CBD5E1;">Database penyimpanan data.</p>
        </div>
        """), unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(textwrap.dedent("""
        <div style="background:#142538;padding:18px;border-radius:12px;text-align:center;">
            <h3 style="color:#34D399;">Pandas</h3>
            <p style="color:#CBD5E1;">Pengolahan dan analisis data.</p>
        </div>
        """), unsafe_allow_html=True)

    with col2:
        st.markdown(textwrap.dedent("""
        <div style="background:#142538;padding:18px;border-radius:12px;text-align:center;">
            <h3 style="color:#34D399;">Matplotlib / Plotly</h3>
            <p style="color:#CBD5E1;">Visualisasi grafik dan statistik.</p>
        </div>
        """), unsafe_allow_html=True)

    st.divider()

    # PENGEMBANG

    st.header("Informasi Pengembang")

    st.markdown(textwrap.dedent("""
    <div style="
        background:linear-gradient(120deg,#142538,#064E3B);
        padding:25px;
        border-radius:15px;
        border:1px solid #10B981;
    ">
        <h2 style="color:#34D399;">ECO MANAGEMENT</h2>
        <p style="color:#CBD5E1;">
            Aplikasi Sistem Pengelolaan Sampah Berbasis Python.
        </p>
        <hr style="border-color:#31564D;">
        <p style="color:#CBD5E1;">
            <b>Pengembang:</b> [Jihan Ulistiawati G]<br>
            <b>Program:</b> [Teknik Informatika]<br>
            <b>Universitas:</b> [Universitas Khairun]<br>
            <b>Teknologi:</b> Python dan Streamlit
        </p>
    </div>
    """), unsafe_allow_html=True)

    st.markdown(textwrap.dedent("""
    <div style="text-align:center;padding:30px;color:#94A3B8;">
        <h3 style="color:#34D399;">♻️ ECO MANAGEMENT</h3>
        <p>Mulai dari pengelolaan sampah yang lebih baik.</p>
        <small>Waste Management System | Python & Streamlit</small>
    </div>
    """), unsafe_allow_html=True)