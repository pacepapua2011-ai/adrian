import streamlit as st
import time
import datetime
import random

# ==========================================
# 1. KONFIGURASI HALAMAN UTAMA
# ==========================================
st.set_page_config(
    page_title="Premium AI Control System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS modern yang kompatibel dengan Streamlit terbaru
st.markdown("""
    <style>
    /* Target yang benar untuk Streamlit terbaru */
    .stApp { background-color: #0e1117; }
    .stButton > button {
        width: 100%;
        border-radius: 6px;
        font-weight: bold;
        transition: 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255,255,255,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. INISIALISASI SESSION STATE GLOBAL
# ==========================================
# Inisialisasi di awal agar tidak error di menu manapun
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Sistem siap. Ada instruksi atau data yang ingin Anda analisis?"}
    ]

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "server_url" not in st.session_state:
    st.session_state.server_url = "https://api.cloud-system.com/v2"

if "refresh_rate" not in st.session_state:
    st.session_state.refresh_rate = 5

if "exec_count" not in st.session_state:
    st.session_state.exec_count = 1842

# ==========================================
# 3. SIDEBAR NAVIGASI
# ==========================================
st.sidebar.title("🤖 AI Command Center")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Pilih Menu Sistem:",
    ["💬 AI Intelligent Assistant", "📊 Monitoring & Analisis Data", "⚙️ Konfigurasi API & Sistem"]
)

st.sidebar.markdown("---")

# Indikator status API
if st.session_state.api_key:
    st.sidebar.success("🟢 API: Terhubung")
else:
    st.sidebar.warning("🔴 API: Belum dikonfigurasi")

st.sidebar.caption(f"🗓️ {datetime.date.today().strftime('%d %B %Y')}")
st.sidebar.caption("🟢 Status Server: Optimal")

# ==========================================
# 4. MENU 1 — AI INTELLIGENT ASSISTANT
# ==========================================
if menu == "💬 AI Intelligent Assistant":
    st.title("💬 AI Intelligent Assistant")
    st.subheader("Asisten cerdas dengan sistem memori aktif.")
    st.markdown("---")

    # Tampilkan riwayat chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Input dari pengguna
    if user_input := st.chat_input("Ketik pesan, perintah, atau masukkan log data di sini..."):
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.exec_count += 1  # Update counter eksekusi

        with st.chat_message("assistant"):
            with st.spinner("Sedang memproses instruksi..."):

                # Cek apakah API key sudah diisi
                if not st.session_state.api_key:
                    response = (
                        "⚠️ API Key belum dikonfigurasi. "
                        "Silakan masuk ke menu **Konfigurasi API & Sistem** "
                        "dan isi API Key terlebih dahulu."
                    )
                else:
                    # === TITIK INTEGRASI API ===
                    # Ganti blok ini dengan pemanggilan API nyata Anda, contoh:
                    #
                    # import anthropic
                    # client = anthropic.Anthropic(api_key=st.session_state.api_key)
                    # result = client.messages.create(
                    #     model="claude-opus-4-5",
                    #     max_tokens=1024,
                    #     messages=[{"role": "user", "content": user_input}]
                    # )
                    # response = result.content[0].text
                    #
                    time.sleep(1.2)
                    response = (
                        f"✅ Instruksi diterima dan diproses.\n\n"
                        f"**Input:** {user_input}\n\n"
                        f"Hubungkan ke API nyata di bagian kode yang ditandai "
                        f"`TITIK INTEGRASI API` untuk mendapatkan respons dinamis."
                    )

                st.write(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

    # Tombol reset chat
    if st.button("🗑️ Reset Riwayat Chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Sistem siap. Ada instruksi atau data yang ingin Anda analisis?"}
        ]
        st.rerun()

# ==========================================
# 5. MENU 2 — MONITORING & ANALISIS DATA
# ==========================================
elif menu == "📊 Monitoring & Analisis Data":
    st.title("📊 System Monitoring & Analytics")
    st.subheader("Pantau performa script, automation bot, dan metrik sistem Anda.")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("Status Operasional", "ACTIVE", "24 Jam Nonstop")
    col2.metric(
        "Total Eksekusi Logika",
        f"{st.session_state.exec_count:,} Request",
        f"+{st.session_state.exec_count - 1842} Sesi Ini"
    )
    col3.metric("Kecepatan Respon Rata-rata", "0.38 Detik", "-0.04s")

    st.markdown("---")

    # Grafik dengan data yang sedikit lebih dinamis
    st.subheader("📈 Grafik Tren Performa")
    
    tab1, tab2 = st.tabs(["📊 Tren Request", "⏱️ Tren Kecepatan"])
    
    with tab1:
        # Simulasi data request per jam (bisa diganti data nyata)
        data_request = [random.randint(10, 60) for _ in range(24)]
        st.line_chart(data_request, use_container_width=True)
        st.caption("Jumlah request per jam dalam 24 jam terakhir")

    with tab2:
        data_speed = [round(random.uniform(0.2, 0.8), 2) for _ in range(24)]
        st.line_chart(data_speed, use_container_width=True)
        st.caption("Kecepatan respon (detik) per jam — semakin rendah semakin baik")

    # Live Logs
    st.markdown("---")
    st.subheader("📋 Catatan Aktivitas Sistem")
    
    waktu = datetime.datetime.now().strftime("%H:%M:%S")
    total_chat = len(st.session_state.messages)
    api_status = "Terhubung ✅" if st.session_state.api_key else "Belum dikonfigurasi ⚠️"

    with st.container(height=220):
        st.caption(f"[{waktu}] 🟢 SUCCESS: Server utama aktif dan merespons.")
        st.caption(f"[{waktu}] ℹ️ INFO: Total pesan dalam sesi ini — {total_chat} pesan.")
        st.caption(f"[{waktu}] ℹ️ INFO: Status API Key — {api_status}")
        st.caption(f"[{waktu}] ⚠️ WARNING: Aktivitas tinggi terdeteksi, performa dioptimalkan.")
        st.caption(f"[{waktu}] 🟢 READY: Menunggu perintah baru dari AI Assistant.")

# ==========================================
# 6. MENU 3 — KONFIGURASI API & SISTEM
# ==========================================
elif menu == "⚙️ Konfigurasi API & Sistem":
    st.title("⚙️ System Settings & Credentials")
    st.subheader("Atur kunci akses API dan endpoint server Anda dengan aman.")
    st.markdown("---")

    st.info("💡 Token yang diinput hanya berjalan di memori sesi ini dan tidak disebarkan ke publik.")

    # Gunakan value dari session_state agar tidak hilang saat berpindah menu
    api_key_input = st.text_input(
        "Kunci API Utama (Secret API Key):",
        type="password",
        value=st.session_state.api_key,
        help="Masukkan API Key dari platform penyedia layanan Anda"
    )
    server_url_input = st.text_input(
        "Server URL Endpoint:",
        value=st.session_state.server_url
    )
    refresh_rate_input = st.slider(
        "Interval Refresh Data Otomatis (Detik):",
        min_value=1, max_value=60,
        value=st.session_state.refresh_rate
    )

    st.markdown("---")

    col_save, col_reset = st.columns(2)

    with col_save:
        if st.button("💾 Simpan Pengaturan"):
            if api_key_input:
                # Simpan ke session_state agar persisten selama sesi
                st.session_state.api_key = api_key_input
                st.session_state.server_url = server_url_input
                st.session_state.refresh_rate = refresh_rate_input
                st.success("✅ Pengaturan berhasil disimpan untuk sesi ini!")
            else:
                st.warning("⚠️ Mohon isi Kunci API sebelum menyimpan.")

    with col_reset:
        if st.button("🔄 Reset ke Default"):
            st.session_state.api_key = ""
            st.session_state.server_url = "https://api.cloud-system.com/v2"
            st.session_state.refresh_rate = 5
            st.info("🔄 Pengaturan dikembalikan ke nilai default.")
            st.rerun()
