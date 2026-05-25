import streamlit as st
import time
import urllib.parse
from gtts import gTTS
import os

# ==========================================
# 1. KONFIGURASI TAMPILAN MODERN & ESTETIK
# ==========================================
st.set_page_config(
    page_title="Nexus Core System",
    page_icon="🌌",
    layout="wide"
)

# Custom CSS untuk Dark Mode Premium & Glassmorphism
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #090c10;
        color: #c9d1d9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Desain Sidebar yang lebih elegan */
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #30363d;
    }
    
    /* Tombol estetik */
    .stButton>button {
        border-radius: 8px;
        background-color: #238636;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2ea043;
        box-shadow: 0 0 10px #2ea043;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SISTEM MEMORI & ANIMASI TYPING
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

def stream_response(text):
    """Efek mengetik yang sangat halus (0.04 detik per kata)"""
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.04)

def buat_suara_ai(teks):
    """Mengubah teks AI menjadi file suara MP3"""
    tts = gTTS(text=teks, lang='id', slow=False)
    tts.save("respon.mp3")
    return "respon.mp3"

# ==========================================
# 3. NAVIGASI MULTI-FITUR (SIDEBAR)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: white;'>🌌 Nexus Core</h2>", unsafe_allow_html=True)
    st.caption("<p style='text-align: center;'>Sistem Tanpa API Key</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio(
        "Pilih Modul Sistem:",
        ["💬 Chat & Tutor Pelajaran", "🎨 AI Image Studio", "🎙️ Voice Assistant (Suara)"]
    )
    
    st.markdown("---")
    # Logika kalibrasi waktu 5 detik
    if st.button("🔄 Kalibrasi Ulang Memori"):
        with st.spinner("Menghapus cache sistem..."):
            time.sleep(5) # Waktu tunggu disetel 5 detik sesuai konfigurasi optimal
            st.session_state.messages = []
            st.success("Sistem disegarkan!")

# ==========================================
# 4. MODUL 1: CHAT & TUTOR PELAJARAN
# ==========================================
if menu == "💬 Chat & Tutor Pelajaran":
    st.markdown("<h2 style='color: white;'>📚 AI Tutor & Assistant</h2>", unsafe_allow_html=True)
    st.caption("Ajukan pertanyaan pelajaran (Matematika, Sejarah, Sains, dll) atau obrolan santai.")
    
    # Tampilkan memori chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if user_input := st.chat_input("Tanyakan soal pelajaran atau ketik sesuatu..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("assistant"):
            # Analisis pertanyaan tanpa API Key menggunakan Keyword Heuristic
            input_lower = user_input.lower()
            
            if any(x in input_lower for x in ["matematika", "hitung", "+", "-", "*", "/"]):
                jawaban = f"Dari logika matematis yang saya analisis terkait '{user_input}', langkah pertama adalah memecah persamaannya. Pastikan Anda mendahulukan perkalian/pembagian sebelum penjumlahan/pengurangan sesuai aturan dasar algoritma hitung."
            elif any(x in input_lower for x in ["sejarah", "siapa", "tahun", "kapan"]):
                jawaban = f"Pertanyaan sejarah yang bagus tentang '{user_input}'. Peristiwa historis selalu memiliki sebab-akibat. Jika ini untuk tugas sekolah, pastikan Anda mengutip tahun dan nama tokoh utamanya dengan akurat."
            elif any(x in input_lower for x in ["biologi", "sains", "fisika", "kimia"]):
                jawaban = f"Terkait ilmu sains '{user_input}', konsep dasarnya berpusat pada pengamatan empiris. Ingatlah bahwa setiap reaksi atau fenomena alam memiliki variabel sebab yang bisa diukur secara presisi."
            else:
                jawaban = f"Saya menerima instruksi Anda: '{user_input}'. Sistem saya saat ini beroperasi penuh dan siap membantu Anda memecahkan tugas atau masalah logika selanjutnya."
            
            st.write_stream(stream_response(jawaban))
        st.session_state.messages.append({"role": "assistant", "content": jawaban})

# ==========================================
# 5. MODUL 2: AI IMAGE STUDIO (TANPA API KEY)
# ==========================================
elif menu == "🎨 AI Image Studio":
    st.markdown("<h2 style='color: white;'>🎨 AI Image Generator</h2>", unsafe_allow_html=True)
    st.caption("Ketik deskripsi gambar, AI akan melukisnya secara instan (Gunakan Bahasa Inggris untuk hasil terbaik).")
    
    prompt_gambar = st.text_input("Deskripsi Gambar:", placeholder="Contoh: A futuristic cyberpunk city at night with neon lights")
    
    if st.button("🖼️ Buat Gambar"):
        if prompt_gambar:
            with st.spinner("AI sedang melukis gambar Anda..."):
                time.sleep(2)
                # Menggunakan layanan Pollinations AI (100% Gratis, Tanpa API)
                prompt_encoded = urllib.parse.quote(prompt_gambar)
                url_gambar = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=1080&height=720&nologo=true"
                
                st.image(url_gambar, caption=f"✨ Hasil dari: {prompt_gambar}", use_container_width=True)
        else:
            st.warning("Silakan masukkan deskripsi gambar terlebih dahulu!")

# ==========================================
# 6. MODUL 3: VOICE ASSISTANT (SUARA AI)
# ==========================================
elif menu == "🎙️ Voice Assistant (Suara)":
    st.markdown("<h2 style='color: white;'>🎙️ AI Voice Response</h2>", unsafe_allow_html=True)
    st.caption("Ketik pesan Anda, dan AI tidak hanya akan membalas dengan teks, tapi juga berbicara langsung kepada Anda.")
    
    pesan_suara = st.text_area("Apa yang ingin Anda sampaikan ke AI?")
    
    if st.button("🔊 Kirim & Dengarkan Respon"):
        if pesan_suara:
            with st.spinner("Memproses suara AI..."):
                teks_respon = f"Halo, saya mendengar Anda mengatakan: {pesan_suara}. Tampilan dan fitur saya sekarang sudah jauh lebih moderen, lengkap, dan bisa berbicara tanpa perlu verifikasi kode rahasia yang rumit."
                
                # Tampilkan efek ngetik
                st.write_stream(stream_response(teks_respon))
                
                # Buat file audio dan mainkan di website
                file_audio = buat_suara_ai(teks_respon)
                audio_bytes = open(file_audio, "rb").read()
                st.audio(audio_bytes, format="audio/mp3")
        else:
            st.warning("Ketik sesuatu agar AI bisa merespons suara Anda.")
