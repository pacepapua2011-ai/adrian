import streamlit as st
import streamlit.components.v1 as components
import requests
import urllib.parse
import time
import json
import os
from datetime import datetime
import hashlib

# =========================================================
# 1. KONFIGURASI SISTEM NEXUS 2026 ULTIMATE
# =========================================================
st.set_page_config(
    page_title="Nexus OS 2026 Ultimate",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. CSS CUSTOM SUPER MODERN (HOLOGRAFIK + NEON + GLASS)
# =========================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600;700&display=swap');
    
    /* Background Futuristik */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a0b2e 50%, #0a0a0f 100%);
        color: #e0e0e0;
    }
    
    /* Animasi Background Particle */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: radial-gradient(circle at 20% 50%, rgba(0, 242, 254, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Typography Keren */
    .nexus-title {
        font-family: 'Orbitron', monospace;
        font-size: 3.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 30%, #00f2fe 70%, #4facfe 100%);
        background-size: 300% auto;
        animation: gradient-shift 3s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        letter-spacing: 5px;
        margin-bottom: 0;
        text-shadow: 0 0 30px rgba(0,242,254,0.3);
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glass Morphism Card */
    .glass-card {
        background: rgba(10, 20, 40, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 24px;
        border: 1px solid rgba(0, 242, 254, 0.3);
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(0, 242, 254, 0.8);
        box-shadow: 0 8px 32px rgba(0, 242, 254, 0.2);
        transform: translateY(-2px);
    }
    
    /* Chat Message Modern */
    [data-testid="stChatMessage"] {
        background: rgba(15, 25, 45, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(0, 242, 254, 0.2);
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Typing Animation Cursor */
    .typing-cursor {
        display: inline-block;
        width: 3px;
        height: 20px;
        background: #00f2fe;
        margin-left: 5px;
        animation: blink 1s infinite;
        vertical-align: middle;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    
    /* Button Futuristik */
    .stButton > button {
        background: linear-gradient(135deg, #00f2fe, #4facfe);
        color: #0a0a0f;
        font-family: 'Orbitron', monospace;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 12px 28px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0, 242, 254, 0.4);
        background: linear-gradient(135deg, #4facfe, #00f2fe);
    }
    
    /* Input Modern */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background: rgba(10, 20, 40, 0.8) !important;
        border: 1px solid #00f2fe !important;
        border-radius: 12px !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Scrollbar Keren */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00f2fe, #4facfe);
        border-radius: 10px;
    }
    
    /* Sidebar Modern */
    [data-testid="stSidebar"] {
        background: rgba(5, 10, 25, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0, 242, 254, 0.2);
    }
    
    /* Status Indicator */
    .status-online {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #00ff00;
        border-radius: 50%;
        box-shadow: 0 0 10px #00ff00;
        animation: pulse 2s infinite;
        margin-right: 8px;
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
        100% { opacity: 1; transform: scale(1); }
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 3. FUNGSI TYPING ANIMATION (MACAM CHATGPT)
# =========================================================
def typing_animation_effect(text, container, speed=0.02):
    """Efek typing seperti ChatGPT"""
    import time
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(f'{displayed_text}<span class="typing-cursor"></span>', unsafe_allow_html=True)
        time.sleep(speed)
    container.markdown(text, unsafe_allow_html=True)

def stream_response_streamlit(response_text, placeholder):
    """Streaming response dengan efek mengetik"""
    full_response = ""
    for chunk in response_text.split():
        full_response += chunk + " "
        placeholder.markdown(full_response + "▌")
        time.sleep(0.05)
    placeholder.markdown(full_response)

# =========================================================
# 4. FITUR SUARA FUTURISTIK
# =========================================================
def play_futuristic_sound():
    """Efek suara futuristik untuk notifikasi"""
    components.html("""
    <script>
        // Sound efek menggunakan Web Audio API
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        const audioCtx = new AudioContext();
        
        function playBeep() {
            const oscillator = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            
            oscillator.frequency.value = 880;
            gainNode.gain.value = 0.1;
            
            oscillator.start();
            gainNode.gain.exponentialRampToValueAtTime(0.00001, audioCtx.currentTime + 0.5);
            oscillator.stop(audioCtx.currentTime + 0.5);
        }
        
        playBeep();
    </script>
    """, height=0)

def speak_with_voice(text):
    """Text to speech dengan kontrol suara"""
    safe_text = text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    components.html(f"""
    <script>
        const utterance = new SpeechSynthesisUtterance('{safe_text}');
        utterance.lang = 'id-ID';
        utterance.rate = 0.9;
        utterance.pitch = 1.1;
        utterance.volume = 1;
        
        // Pilih suara yang natural
        window.speechSynthesis.onvoiceschanged = () => {{
            const voices = window.speechSynthesis.getVoices();
            const indonesianVoice = voices.find(voice => voice.lang.includes('id'));
            if (indonesianVoice) utterance.voice = indonesianVoice;
            window.speechSynthesis.speak(utterance);
        }};
        
        window.speechSynthesis.speak(utterance);
    </script>
    """, height=0)

# =========================================================
# 5. API CALL DENGAN RETRY MECHANISM
# =========================================================
def call_ai_api(prompt, system_prompt=None, max_retries=2):
    """Panggil API Pollinations dengan retry"""
    for attempt in range(max_retries):
        try:
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            if system_prompt:
                url += f"?system={urllib.parse.quote(system_prompt)}"
            
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.text
            else:
                if attempt == max_retries - 1:
                    return "⚠️ Gangguan koneksi ke server AI. Coba lagi ya!"
                time.sleep(1)
        except Exception as e:
            if attempt == max_retries - 1:
                return f"⚠️ Error: {str(e)}"
            time.sleep(1)
    return "⚠️ Gagal terhubung ke AI"

# =========================================================
# 6. SIDEBAR MODERN DENGAN STATISTIK
# =========================================================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <div style="font-size: 3rem;">🌌</div>
            <h2 style="color: #00f2fe; font-family: 'Orbitron'; margin: 0;">NEXUS OS</h2>
            <p style="color: #8892b0; font-size: 0.8rem;">v2026.2 ULTIMATE</p>
            <div style="margin-top: 10px;">
                <span class="status-online"></span>
                <span style="color: #00ff00; font-size: 0.8rem;">AI ACTIVE</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Menu dengan icon modern
    menu_options = {
        "💬 Neural Chat": "🧠",
        "🌐 Universal Translator": "🌍",
        "🎨 Quantum Studio": "✨",
        "⚡ Code Nexus": "💻",
        "🛸 Nexus Store": "🎮",
        "📊 Analytics Hub": "📈"
    }
    
    pilihan = st.radio(
        "**SYSTEM MODULES**",
        list(menu_options.keys()),
        format_func=lambda x: f"{menu_options[x]} {x}"
    )
    
    st.markdown("---")
    
    # Statistik real-time
    if "messages" in st.session_state:
        chat_count = len(st.session_state.get("messages", []))
        st.metric("💬 Total Interactions", chat_count, delta="+1" if chat_count > 0 else "0")
    
    # Tombol dengan efek
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Reset", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🔊 Mute/Unmute", use_container_width=True):
            st.session_state.sound_enabled = not st.session_state.get("sound_enabled", True)
            st.success("✅ Suara diubah!")

# Inisialisasi session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "sound_enabled" not in st.session_state:
    st.session_state.sound_enabled = True

# =========================================================
# 7. MODUL 1: NEURAL CHAT (DENGAN TYPING ANIMATION)
# =========================================================
if pilihan == "💬 Neural Chat":
    st.markdown('<h1 class="nexus-title">NEURAL CHAT</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #4facfe; margin-bottom: 30px;">⚡ AI dengan efek mengetik real-time ⚡</p>', unsafe_allow_html=True)
    
    # Tampilkan history chat dengan animasi
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🧑‍🚀" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])
    
    # Input user
    if prompt := st.chat_input("💭 Ketik pesanmu disini... (bisa pakai voice di HP dengan tap 🎤)"):
        # Tambah pesan user
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍🚀"):
            st.markdown(prompt)
        
        # Proses AI dengan efek mengetik
        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            
            system_prompt = "Kamu adalah Nexus AI, asisten futuristik tahun 2026. Jawab dengan bahasa Indonesia yang natural, kreatif, dan antusias. Gunakan emoji yang relevan. Jawaban dibuat ringkas tapi informatif karena akan dibacakan suara."
            
            # Panggil API
            jawaban = call_ai_api(prompt, system_prompt)
            
            # Efek typing seperti ChatGPT
            stream_response_streamlit(jawaban, message_placeholder)
            
            # Simpan ke history
            st.session_state.messages.append({"role": "assistant", "content": jawaban})
            
            # Fitur suara jika diaktifkan
            col1, col2, col3 = st.columns([1,1,3])
            with col1:
                if st.button("🔊 Play Voice"):
                    speak_with_voice(jawaban)
                    if st.session_state.sound_enabled:
                        play_futuristic_sound()
            with col2:
                if st.button("📋 Copy"):
                    st.write("✅ Tersalin!")

# =========================================================
# 8. MODUL 2: UNIVERSAL TRANSLATOR (DENGAN DETEKSI OTOMATIS)
# =========================================================
elif pilihan == "🌐 Universal Translator":
    st.markdown('<h1 class="nexus-title">UNIVERSAL TRANSLATOR</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #4facfe;">🌍 Terjemahkan ke 15+ bahasa dengan AI 🌍</p>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            source_text = st.text_area("📝 Teks sumber:", height=150, 
                                       placeholder="Tulis teks yang ingin diterjemahkan...")
        
        with col2:
            target_lang = st.selectbox("🎯 Target bahasa:", [
                "English (US)", "English (UK)", "Japanese", "Korean", 
                "Chinese (Mandarin)", "Arabic", "Russian", "German", 
                "French", "Spanish", "Italian", "Dutch", 
                "Indonesian Formal", "Javanese (Krama)", "Sundanese"
            ])
        
        # Fitur tambahan
        use_formal = st.checkbox("✨ Mode Formal (untuk dokumen resmi)")
        auto_detect = st.checkbox("🔍 Auto-detect bahasa sumber", value=True)
        
        if st.button("🚀 TERJEMAHKAN", use_container_width=True):
            if source_text:
                with st.spinner("🧠 Memproses terjemahan..."):
                    if auto_detect:
                        prompt = f"Detect the language of this text, then translate it to {target_lang}. {'Use formal language' if use_formal else 'Use natural casual language'}. Only output the translation, no explanations. Text: {source_text}"
                    else:
                        prompt = f"Translate this text to {target_lang}. {'Use formal language' if use_formal else 'Use natural casual language'}. Only output translation. Text: {source_text}"
                    
                    result = call_ai_api(prompt)
                    
                    st.markdown("---")
                    st.markdown("### ✅ Hasil Terjemahan:")
                    st.markdown(f'<div class="glass-card">{result}</div>', unsafe_allow_html=True)
                    
                    # Tombol suara untuk hasil
                    if st.button("🔊 Dengarkan hasil"):
                        speak_with_voice(result)
            else:
                st.warning("⚠️ Masukkan teks yang akan diterjemahkan!")

# =========================================================
# 9. MODUL 3: QUANTUM STUDIO (AI IMAGE GENERATOR PREMIUM)
# =========================================================
elif pilihan == "🎨 Quantum Studio":
    st.markdown('<h1 class="nexus-title">QUANTUM STUDIO</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #4facfe;">🎨 Generate gambar 4K dengan AI canggih 🎨</p>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            prompt_img = st.text_area("🎨 Deskripsi gambar:", 
                                      placeholder="Contoh: Cyberpunk samurai with neon katana in futuristic Tokyo, rain, reflections, 8K, cinematic lighting, masterpiece",
                                      height=100)
        
        with col2:
            style = st.selectbox("🎭 Style:", ["Photorealistic", "Anime", "Cyberpunk", "Fantasy", "Abstract", "Minimalist"])
            resolution = st.selectbox("📐 Resolusi:", ["1080x1080 (Square)", "1920x1080 (Landscape)", "1080x1920 (Portrait)"])
        
        # Gallery history
        if "gallery" not in st.session_state:
            st.session_state.gallery = []
        
        if st.button("✨ GENERATE SEKARANG", use_container_width=True):
            if prompt_img:
                with st.spinner("🎨 AI sedang melukis masterpiece anda..."):
                    # Enhance prompt dengan style
                    enhanced_prompt = f"{prompt_img}, {style} style, high quality, detailed"
                    seed = int(time.time())
                    res_map = {
                        "1080x1080 (Square)": "1080x1080",
                        "1920x1080 (Landscape)": "1920x1080",
                        "1080x1920 (Portrait)": "1080x1920"
                    }
                    
                    image_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(enhanced_prompt)}?width={res_map[resolution].split('x')[0]}&height={res_map[resolution].split('x')[1]}&seed={seed}&nologo=true"
                    
                    time.sleep(1.5)  # Efek loading
                    
                    st.markdown("### 🖼️ Hasil Generate:")
                    st.image(image_url, use_container_width=True)
                    
                    # Tombol download
                    st.markdown(f'<a href="{image_url}" download="nexus_art_{seed}.png"><button style="background: linear-gradient(135deg, #00f2fe, #4facfe); border: none; border-radius: 10px; padding: 10px 20px; color: white; cursor: pointer;">💾 Download Gambar</button></a>', unsafe_allow_html=True)
                    
                    # Simpan ke galeri
                    st.session_state.gallery.append({"prompt": prompt_img, "url": image_url, "time": datetime.now()})
                    
                    if st.session_state.sound_enabled:
                        play_futuristic_sound()
            else:
                st.warning("⚠️ Masukkan deskripsi gambar terlebih dahulu!")
        
        # Tampilkan galeri
        if st.session_state.gallery:
            with st.expander("📸 Gallery History", expanded=False):
                for idx, img in enumerate(reversed(st.session_state.gallery[-6:])):
                    st.image(img["url"], caption=f"{img['prompt'][:50]}...", use_container_width=True)

# =========================================================
# 10. MODUL 4: CODE NEXUS (AI PROGRAMMING ASSISTANT)
# =========================================================
elif pilihan == "⚡ Code Nexus":
    st.markdown('<h1 class="nexus-title">CODE NEXUS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #4facfe;">⚡ AI Programming Assistant dengan syntax highlighting ⚡</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        language = st.selectbox("💻 Bahasa:", ["Python", "JavaScript", "TypeScript", "Java", "C++", "Go", "Rust", "HTML/CSS", "SQL"])
        code_type = st.radio("Tipe:", ["Generate New", "Explain Code", "Debug", "Optimize"])
    
    with col1:
        user_input = st.text_area("📝 Instruksi atau code:", 
                                  placeholder="Contoh: Buatkan function untuk detect faces menggunakan Python dengan OpenCV",
                                  height=150)
    
    if st.button("🚀 EXECUTE", use_container_width=True):
        if user_input:
            with st.spinner("🧠 AI sedang menganalisa code..."):
                if code_type == "Generate New":
                    prompt = f"Generate {language} code for: {user_input}. Provide only the code with proper syntax highlighting and a brief explanation."
                elif code_type == "Explain Code":
                    prompt = f"Explain this {language} code line by line in Indonesian: {user_input}"
                elif code_type == "Debug":
                    prompt = f"Debug this {language} code and provide fixed version: {user_input}"
                else:  # Optimize
                    prompt = f"Optimize this {language} code for better performance: {user_input}"
                
                result = call_ai_api(prompt)
                
                st.markdown("### ✅ Output:")
                st.code(result, language=language.lower())
                
                # Copy button
                if st.button("📋 Copy Code"):
                    st.write("✅ Code tersalin ke clipboard!")
                
                if st.session_state.sound_enabled:
                    play_futuristic_sound()
        else:
            st.warning("⚠️ Masukkan instruksi atau code!")

# =========================================================
# 11. MODUL 5: NEXUS STORE (DENGAN QR CODE SIMULASI)
# =========================================================
elif pilihan == "🛸 Nexus Store":
    st.markdown('<h1 class="nexus-title">NEXUS STORE</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #4facfe;">💎 Top-up game termurah se-alam semesta 💎</p>', unsafe_allow_html=True)
    
    # Banner promo
    st.markdown("""
        <div class="glass-card" style="text-align: center; background: linear-gradient(135deg, rgba(0,242,254,0.1), rgba(79,172,254,0.1));">
            <h3 style="color: #00f2fe;">🎉 PROMO SPESIAL</h3>
            <p style="font-size: 1.2rem;">Diskon 20% untuk semua item! Gunakan kode: <strong style="color: #00f2fe;">NEXUS2026</strong></p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        game = st.selectbox("🎮 Game:", ["Mobile Legends", "Free Fire", "PUBG Mobile", "Valorant", "Genshin Impact", "Call of Duty Mobile"])
        id_player = st.text_input("🆔 Player ID / User ID")
        zone_id = st.text_input("🌍 Zone ID (Optional)")
    
    with col2:
        item = st.selectbox("💎 Item / Diamond:", [
            "50 Diamond - Rp 12.000",
            "100 Diamond - Rp 22.000", 
            "250 Diamond - Rp 52.000",
            "500 Diamond - Rp 99.000",
            "1000 Diamond - Rp 189.000",
            "Weekly Pass - Rp 49.000",
            "Monthly Pass - Rp 149.000"
        ])
        
        payment = st.selectbox("💳 Metode Payment:", ["QRIS (All Bank)", "OVO", "GoPay", "DANA", "Bank Transfer", "ShopeePay"])
    
    promo_code = st.text_input("🎁 Kode Promo (optional)")
    
    # Hitung total
    prices = {
        "50 Diamond - Rp 12.000": 12000,
        "100 Diamond - Rp 22.000": 22000,
        "250 Diamond - Rp 52.000": 52000,
        "500 Diamond - Rp 99.000": 99000,
        "1000 Diamond - Rp 189.000": 189000,
        "Weekly Pass - Rp 49.000": 49000,
        "Monthly Pass - Rp 149.000": 149000
    }
    
    total = prices[item]
    if promo_code == "NEXUS2026":
        total = int(total * 0.8)
        st.success("✨ Kode promo valid! Diskon 20% applied ✨")
    
    st.markdown(f"""
        <div style="background: rgba(0,242,254,0.1); padding: 15px; border-radius: 12px; margin: 15px 0;">
            <h4 style="margin: 0;">💰 Total Pembayaran:</h4>
            <p style="font-size: 2rem; color: #00f2fe; margin: 0;">Rp {total:,}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("💳 PROCEED TO PAYMENT", use_container_width=True):
        if not id_player:
            st.error("⚠️ Player ID wajib diisi!")
        else:
            with st.spinner("🔐 Memproses transaksi..."):
                time.sleep(2)
                
                # QR Code simulasi
                st.markdown("""
                    <div class="glass-card" style="text-align: center;">
                        <h3>📱 Scan QR Code untuk membayar</h3>
                        <div style="width: 200px; height: 200px; background: black; margin: 20px auto; display: flex; align-items: center; justify-content: center; border-radius: 20px;">
                            <p style="color: white;">[ SIMULASI QR ]</p>
                        </div>
                        <p style="color: #00f2fe;">Kode Transaksi: <strong>NEX{int(time.time())}</strong></p>
                        <p>Silakan scan QR Code di atas menggunakan {payment}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("✅ Saya sudah membayar"):
                    st.balloons()
                    st.success(f"✅ Top-up {game} untuk ID {id_player} berhasil! Item akan masuk dalam 5 menit.")
                    
                    # Kirim notifikasi suara
                    if st.session_state.sound_enabled:
                        play_futuristic_sound()
                        speak_with_voice(f"Top up untuk game {game} berhasil, terima kasih sudah berbelanja di Nexus Store")

# =========================================================
# 12. MODUL 6: ANALYTICS HUB (FITUR BARU!)
# =========================================================
elif pilihan == "📊 Analytics Hub":
    st.markdown('<h1 class="nexus-title">ANALYTICS HUB</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #4facfe;">📊 Statistik penggunaan AI dan performa sistem 📊</p>', unsafe_allow_html=True)
    
    # Statistik chat
    total_chats = len(st.session_state.messages)
    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    ai_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💬 Total Chat", total_chats)
    with col2:
        st.metric("👤 User Messages", user_msgs)
    with col3:
        st.metric("🤖 AI Responses", ai_msgs)
    with col4:
        st.metric("⚡ AI Status", "Active", delta="Online")
    
    # Waktu penggunaan
    if "session_start" not in st.session_state:
        st.session_state.session_start = time.time()
    
    session_duration = time.time() - st.session_state.session_start
    st.info(f"⏱️ Session duration: {int(session_duration // 60)} menit {int(session_duration % 60)} detik")
    
    # Tips penggunaan
    with st.expander("💡 Tips & Trik Nexus OS", expanded=True):
        st.markdown("""
        - 🎤 **Voice Input:** Gunakan microphone di keyboard HP untuk bicara ke AI
        - 🔊 **Voice Output:** Klik tombol "Play Voice" di setiap response AI
        - 🎨 **Image Generation:** Semakin detail deskripsi, semakin bagus hasilnya
        - ⚡ **Code Nexus:** Bisa generate, explain, debug, dan optimize code
        - 💎 **Nexus Store:** Kode promo **NEXUS2026** untuk diskon 20%
        """)
    
    # Progress bar penggunaan
    st.markdown("### 🚀 System Performance")
    st.progress(0.75)
    st.caption("75% System Capacity - Optimal")
    
    # Galeri images count
    if "gallery" in st.session_state:
        st.metric("🎨 Images Generated", len(st.session_state.gallery))

# =========================================================
# 13. FOOTER
# =========================================================
st.markdown("""
    <div style="text-align: center; padding: 30px; margin-top: 50px; border-top: 1px solid rgba(0,242,254,0.2);">
        <p style="color: #8892b0;">⚡ Nexus OS 2026 Ultimate Edition ⚡</p>
        <p style="color: #8892b0; font-size: 0.8rem;">Powered by Pollinations AI | Real-time Typing Animation | Voice Enabled</p>
    </div>
""", unsafe_allow_html=True)
