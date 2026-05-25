import streamlit as st
import streamlit.components.v1 as components
import time
import urllib.parse
import random
import math
import re
from datetime import datetime
import json
import base64

# ==========================================
# 1. KONFIGURASI TAMPILAN PREMIUM
# ==========================================
st.set_page_config(
    page_title="NEXUS EINSTEIN - Realistic Voice AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Premium
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp header {display: none;}
    
    .stApp {
        background: radial-gradient(circle at 20% 50%, #0a0a2a, #000000);
        color: #e0e0e0;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(10, 20, 40, 0.7);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0, 242, 254, 0.2);
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        border: 1px solid rgba(0, 242, 254, 0.2);
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(0, 242, 254, 0.5);
        box-shadow: 0 0 30px rgba(0, 242, 254, 0.1);
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.05); text-shadow: 0 0 20px #00f2fe; }
    }
    
    .voice-active {
        animation: pulse 1.5s infinite;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.2), rgba(79, 172, 254, 0.1));
        border: 1px solid rgba(0, 242, 254, 0.4);
        border-radius: 12px;
        color: white;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.4), rgba(79, 172, 254, 0.2));
        border-color: #00f2fe;
        transform: translateY(-2px);
    }
    
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00f2fe, #4facfe);
        border-radius: 3px;
    }
    
    .status-online {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #00ff00;
        border-radius: 50%;
        box-shadow: 0 0 10px #00ff00;
        animation: statusPulse 2s infinite;
        margin-right: 8px;
    }
    
    @keyframes statusPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .typing-cursor {
        display: inline-block;
        width: 2px;
        height: 18px;
        background: #00f2fe;
        margin-left: 4px;
        animation: blink 1s infinite;
        vertical-align: middle;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SISTEM LOGIKA EINSTEIN
# ==========================================

class EinsteinBrain:
    def __init__(self):
        self.knowledge_base = self.init_knowledge()
        
    def init_knowledge(self):
        return {
            "matematika": {
                "aljabar": "Pemecahan persamaan aljabar menggunakan prinsip keseimbangan.",
                "kalkulus": "Turunan mengukur laju perubahan, integral mengukur akumulasi.",
                "geometri": "Ruang dan bentuk mengikuti aturan Euclidean.",
                "statistika": "Probabilitas adalah bahasa ketidakpastian."
            },
            "fisika": {
                "mekanika": "F = ma adalah hukum dasar gerak Newton.",
                "relativitas": "E = mc², massa dan energi adalah entitas yang setara.",
                "quantum": "Partikel bisa berada di banyak tempat sekaligus hingga diamati."
            },
            "filsafat": {
                "logika": "Premis benar + penalaran valid = kesimpulan benar.",
                "eksistensi": "Cogito ergo sum - Saya berpikir maka saya ada."
            },
            "biologi": {
                "evolusi": "Seleksi alam menyaring sifat yang menguntungkan.",
                "sel": "Sel adalah unit dasar kehidupan."
            }
        }
    
    def analyze(self, question):
        """Analisis dengan logika Einstein"""
        question_lower = question.lower()
        
        # Deteksi matematika
        if any(x in question_lower for x in ["akar", "sqrt", "pangkat", "log", "integral"]):
            return self.solve_math(question)
        
        # Deteksi kategori
        categories = {
            "matematika": ["matematika", "hitung", "angka", "rumus"],
            "fisika": ["fisika", "gerak", "gaya", "energi", "relativitas"],
            "filsafat": ["filsafat", "eksistensi", "logika", "etika"],
            "biologi": ["biologi", "sel", "dna", "evolusi"]
        }
        
        for category, keywords in categories.items():
            if any(k in question_lower for k in keywords):
                return self.get_category_response(category, question)
        
        return self.general_response(question)
    
    def solve_math(self, question):
        """Pemecahan soal matematika"""
        numbers = re.findall(r'\d+', question)
        
        if "akar" in question or "sqrt" in question:
            if numbers:
                num = int(numbers[0])
                result = math.sqrt(num)
                return f"Nilai akar kuadrat dari {num} adalah {result:.4f}. Ini berarti {result} × {result} = {num}."
        
        elif "pangkat" in question or "^" in question:
            if len(numbers) >= 2:
                base = int(numbers[0])
                exp = int(numbers[1])
                result = base ** exp
                return f"{base} pangkat {exp} = {result}. Ini artinya {base} dikalikan dengan dirinya sendiri sebanyak {exp} kali."
        
        return "Untuk menyelesaikan soal matematika ini, kita perlu menggunakan prinsip-prinsip dasar aljabar. Coba tanyakan dengan lebih spesifik!"
    
    def get_category_response(self, category, question):
        knowledge = self.knowledge_base.get(category, {})
        relevant = list(knowledge.values())[:2]
        knowledge_text = "\n".join([f"• {k}" for k in relevant])
        
        return f"""Berdasarkan analisis saya menggunakan prinsip logika Einstein:

**Kategori:** {category.upper()}

**Penjelasan:**
{knowledge_text}

Mengenai pertanyaan Anda tentang "{question[:100]}{'...' if len(question) > 100 else ''}", hal ini dapat dipahami dengan melihat akar permasalahannya. Seperti kata Einstein, "Segala sesuatu harus dibuat sesederhana mungkin, tetapi tidak lebih sederhana dari itu."

Apakah ada aspek spesifik yang ingin Anda tanyakan lebih lanjut?"""
    
    def general_response(self, question):
        quotes = [
            "Imajinasi lebih penting daripada pengetahuan.",
            "Logika akan membawamu dari A ke B. Imajinasi akan membawamu ke mana saja.",
            "Jangan pernah berhenti bertanya. Rasa ingin tahu memiliki alasan tersendiri untuk eksis."
        ]
        
        return f"""Menarik sekali pertanyaan Anda!

Setelah saya analisis menggunakan kerangka berpikir logis, pertanyaan "{question[:100]}{'...' if len(question) > 100 else ''}" memiliki beberapa dimensi yang menarik untuk dieksplorasi.

**Refleksi:**
"{random.choice(quotes)}"

**Saran:**
Coba uraikan pertanyaan Anda menjadi bagian-bagian yang lebih kecil agar lebih mudah dipahami. Saya siap membantu lebih lanjut!"""

# ==========================================
# 3. VOICE AI SUPER REALISTIS
# ==========================================

def create_realistic_voice_html(text, voice_type="natural", speed=0.9, pitch=1.0):
    """Membuat voice AI super realistis dengan Web Speech API premium"""
    
    safe_text = text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ").replace("`", "\\`")
    
    # Pilihan suara premium (perempuan dan laki-laki)
    voice_selector = """
    let voices = window.speechSynthesis.getVoices();
    let selectedVoice = null;
    
    // Prioritas suara natural
    const preferredVoices = [
        'Google UK English Female',
        'Google US English Female', 
        'Microsoft Zira Desktop',
        'Samantha',
        'Google UK English Male',
        'Google US English Male'
    ];
    
    for (let pref of preferredVoices) {
        selectedVoice = voices.find(v => v.name.includes(pref));
        if (selectedVoice) break;
    }
    
    // Fallback ke suara Indonesia jika ada
    if (!selectedVoice) {
        selectedVoice = voices.find(v => v.lang.includes('id'));
    }
    """
    
    html_code = f"""
    <script>
    (function() {{
        const speakText = function() {{
            if (!window.speechSynthesis) {{
                console.log('Speech synthesis not supported');
                return;
            }}
            
            window.speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance('{safe_text}');
            
            // Pengaturan suara natural
            utterance.lang = 'id-ID';
            utterance.rate = {speed};
            utterance.pitch = {pitch};
            utterance.volume = 1;
            
            // Pilih suara terbaik
            const voices = window.speechSynthesis.getVoices();
            const naturalVoices = voices.filter(v => 
                v.lang.includes('id') || 
                v.name.includes('Google') || 
                v.name.includes('Natural') ||
                v.name.includes('Female') ||
                v.name.includes('Male')
            );
            
            if (naturalVoices.length > 0) {{
                // Pilih suara yang paling natural
                const bestVoice = naturalVoices.find(v => v.name.includes('Google')) || naturalVoices[0];
                utterance.voice = bestVoice;
            }}
            
            // Event untuk debugging
            utterance.onstart = () => console.log('🎙️ Voice started');
            utterance.onend = () => console.log('✅ Voice finished');
            utterance.onerror = (e) => console.log('Error:', e);
            
            // Play voice
            setTimeout(() => {{
                window.speechSynthesis.speak(utterance);
            }}, 100);
        }};
        
        // Tunggu voices loaded
        if (window.speechSynthesis.getVoices().length > 0) {{
            speakText();
        }} else {{
            window.speechSynthesis.onvoiceschanged = speakText;
        }}
    }})();
    </script>
    """
    
    return components.html(html_code, height=0)

def create_mic_button():
    """Membuat tombol mic untuk voice input"""
    mic_html = """
    <div id="mic-container" style="position: fixed; bottom: 100px; right: 30px; z-index: 1000;">
        <button id="premium-mic-btn" style="
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            border: none;
            cursor: pointer;
            font-size: 2rem;
            box-shadow: 0 0 30px rgba(0,242,254,0.5);
            transition: all 0.3s;
            animation: micPulse 2s infinite;
        ">
            🎤
        </button>
        <div id="mic-status" style="text-align: center; margin-top: 10px; font-size: 0.7rem; color: #00f2fe;">Tap to speak</div>
    </div>
    
    <style>
        @keyframes micPulse {
            0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(0,242,254,0.5); }
            50% { transform: scale(1.05); box-shadow: 0 0 40px rgba(0,242,254,0.8); }
        }
        .mic-recording {
            animation: recordingPulse 0.5s infinite !important;
            background: linear-gradient(135deg, #ff4444, #cc0000) !important;
        }
        @keyframes recordingPulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
    </style>
    
    <script>
    let isRecording = false;
    let recognition = null;
    
    function initPremiumVoice() {
        if ('webkitSpeechRecognition' in window) {
            recognition = new webkitSpeechRecognition();
            recognition.lang = 'id-ID';
            recognition.continuous = false;
            recognition.interimResults = true;
            
            recognition.onstart = function() {
                isRecording = true;
                const btn = document.getElementById('premium-mic-btn');
                const status = document.getElementById('mic-status');
                btn.classList.add('mic-recording');
                btn.innerHTML = '🔴';
                status.innerHTML = '🔴 Listening... Speak now';
                status.style.color = '#ff4444';
            };
            
            recognition.onresult = function(event) {
                let finalTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript;
                    }
                }
                if (finalTranscript) {
                    const url = new URL(window.location.href);
                    url.searchParams.set('voice_msg', encodeURIComponent(finalTranscript));
                    window.location.href = url.toString();
                }
            };
            
            recognition.onerror = function(event) {
                console.error('Error:', event.error);
                stopRecording();
                const status = document.getElementById('mic-status');
                status.innerHTML = '❌ Error, try again';
                status.style.color = '#ff4444';
                setTimeout(() => {
                    status.innerHTML = 'Tap to speak';
                    status.style.color = '#00f2fe';
                }, 2000);
            };
            
            recognition.onend = function() {
                stopRecording();
            };
            
            return true;
        }
        return false;
    }
    
    function stopRecording() {
        isRecording = false;
        const btn = document.getElementById('premium-mic-btn');
        const status = document.getElementById('mic-status');
        btn.classList.remove('mic-recording');
        btn.innerHTML = '🎤';
        status.innerHTML = 'Tap to speak';
        status.style.color = '#00f2fe';
    }
    
    document.getElementById('premium-mic-btn').onclick = function() {
        if (!recognition) {
            if (!initPremiumVoice()) {
                alert('Voice recognition not supported. Please use Chrome!');
                return;
            }
        }
        if (!isRecording) {
            recognition.start();
        } else {
            recognition.stop();
        }
    };
    
    initPremiumVoice();
    </script>
    """
    return components.html(mic_html, height=100)

# ==========================================
# 4. INISIALISASI
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "brain" not in st.session_state:
    st.session_state.brain = EinsteinBrain()

def stream_response(text):
    """Efek mengetik halus"""
    placeholder = st.empty()
    displayed = ""
    for char in text:
        displayed += char
        placeholder.markdown(f'{displayed}<span class="typing-cursor"></span>', unsafe_allow_html=True)
        time.sleep(0.008)
    placeholder.markdown(displayed)

# ==========================================
# 5. SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 3rem;">🎙️</div>
        <h2 style="color: #00f2fe;">NEXUS</h2>
        <h3 style="color: #4facfe;">REALISTIC VOICE</h3>
        <div style="margin-top: 10px;">
            <span class="status-online"></span>
            <span style="font-size: 0.8rem;">Human-like Voice</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.radio(
        "⚡ **MODULES**",
        ["💬 Einstein Chat", "🎙️ Realistic Voice AI", "🎨 Neural Image Studio", "🧪 Logic Analyzer"]
    )
    
    st.markdown("---")
    
    st.markdown("### 🎵 Voice Settings")
    voice_speed = st.slider("Speaking Speed", 0.6, 1.2, 0.85, 0.05)
    voice_pitch = st.slider("Voice Pitch", 0.7, 1.3, 1.0, 0.05)
    
    st.markdown("---")
    st.metric("🧠 IQ Level", "225 (Einstein)")
    st.metric("💬 Chat Count", len(st.session_state.messages))
    
    st.markdown("---")
    if st.button("🔄 Reset Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ==========================================
# 6. MODUL EINSTEIN CHAT
# ==========================================
if menu == "💬 Einstein Chat":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="background: linear-gradient(135deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🧠 EINSTEIN AI CHAT
        </h1>
        <p style="color: #8892b0;">Kecerdasan Level Einstein • Suara Manusia Natural</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tombol mic floating
    create_mic_button()
    
    # Tampilkan history
    for msg in st.session_state.messages[-20:]:
        with st.chat_message(msg["role"], avatar="🧑‍🚀" if msg["role"] == "user" else "🧠"):
            st.markdown(msg["content"])
    
    # Input user
    if prompt := st.chat_input("Tanyakan soal matematika, fisika, atau apapun..."):
        with st.chat_message("user", avatar="🧑‍🚀"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("🧠 Menganalisis..."):
                response = st.session_state.brain.analyze(prompt)
                stream_response(response)
                
                # Voice dengan suara realistis
                create_realistic_voice_html(response, speed=voice_speed, pitch=voice_pitch)
                
        st.session_state.messages.append({"role": "assistant", "content": response})

# ==========================================
# 7. MODUL REALISTIC VOICE AI
# ==========================================
elif menu == "🎙️ Realistic Voice AI":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="background: linear-gradient(135deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🎙️ REALISTIC VOICE AI
        </h1>
        <p style="color: #8892b0;">Bukan Suara Robot • Suara Manusia Natural</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        voice_text = st.text_area(
            "✍️ **Ketik pesan Anda**", 
            placeholder="Contoh: Jelaskan hukum relativitas Einstein dengan bahasa sederhana...",
            height=120
        )
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 3rem;">🎙️</div>
            <p style="color: #00f2fe;">Premium Voice</p>
            <p style="font-size: 0.7rem;">Natural • Clear • Human-like</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Voice preview
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔊 Dengarkan Contoh", use_container_width=True):
            example_text = "Halo! Saya Nexus AI dengan suara manusia natural, bukan suara robot. Saya siap membantu Anda!"
            create_realistic_voice_html(example_text, speed=voice_speed, pitch=voice_pitch)
            st.success("✅ Memutar contoh suara...")
    
    with col2:
        if st.button("🧠 Analisis & Bicara", use_container_width=True):
            if voice_text:
                with st.spinner("🧠 Menganalisis..."):
                    response = st.session_state.brain.analyze(voice_text)
                    
                    st.markdown("### 📝 Respon AI:")
                    stream_response(response)
                    
                    # Voice dengan suara realistis
                    create_realistic_voice_html(response, speed=voice_speed, pitch=voice_pitch)
                    
                    st.success("🔊 Suara sedang diputar...")
            else:
                st.warning("Masukkan pesan terlebih dahulu!")
    
    with col3:
        voice_preview = st.checkbox("🎤 Auto-play response")
    
    # Voice tips
    st.markdown("""
    <div class="glass-card" style="margin-top: 20px;">
        <h3 style="color: #00f2fe;">💡 Tips Voice AI Realistis</h3>
        <ul>
            <li>Suara menggunakan Web Speech API premium</li>
            <li>Otomatis memilih suara Google/Microsoft terbaik</li>
            <li>Bisa diatur kecepatan dan pitch di sidebar</li>
            <li>Support bahasa Indonesia natural</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 8. MODUL NEURAL IMAGE STUDIO
# ==========================================
elif menu == "🎨 Neural Image Studio":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="background: linear-gradient(135deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🎨 NEURAL IMAGE STUDIO
        </h1>
        <p style="color: #8892b0;">AI Melukis dengan Imajinasi Neural</p>
    </div>
    """, unsafe_allow_html=True)
    
    prompt_img = st.text_area(
        "🎨 **Deskripsi Gambar**", 
        placeholder="Contoh: Albert Einstein riding a bicycle through space, surreal art, 4K",
        height=100
    )
    
    style = st.selectbox("🎭 Style", ["Photorealistic", "Surrealism", "Cyberpunk", "Impressionism", "Abstract"])
    
    if st.button("✨ Generate Art", use_container_width=True):
        if prompt_img:
            with st.spinner("🎨 Neural network painting..."):
                enhanced = f"{prompt_img}, {style} style, high quality, 8K"
                encoded = urllib.parse.quote(enhanced)
                image_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1080&nologo=true"
                
                time.sleep(1.5)
                st.image(image_url, use_container_width=True)
                
                # Voice feedback
                create_realistic_voice_html("Gambar telah selesai dibuat. Selamat menikmati!", speed=0.85, pitch=1.0)
        else:
            st.warning("Masukkan deskripsi gambar!")

# ==========================================
# 9. MODUL LOGIC ANALYZER
# ==========================================
else:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="background: linear-gradient(135deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🧪 LOGIC ANALYZER
        </h1>
        <p style="color: #8892b0;">Analisis Premis • Deteksi Fallacy • Solusi Logis</p>
    </div>
    """, unsafe_allow_html=True)
    
    premise = st.text_area("📝 **Premis / Pernyataan**", placeholder="Masukkan argumen atau pernyataan yang ingin dianalisis...", height=150)
    
    if st.button("🔍 Analisis Logika", use_container_width=True):
        if premise:
            with st.spinner("🧠 Menganalisis dengan logika Einstein..."):
                analysis = st.session_state.brain.analyze(premise)
                st.markdown("### 📊 Hasil Analisis:")
                stream_response(analysis)
                create_realistic_voice_html(analysis[:300], speed=0.85, pitch=1.0)
        else:
            st.warning("Masukkan premis untuk dianalisis!")

# ==========================================
# 10. HANDLE VOICE INPUT
# ==========================================
query_params = st.query_params
if "voice_msg" in query_params and query_params["voice_msg"]:
    voice_message = query_params["voice_msg"]
    
    if voice_message and voice_message.strip():
        with st.chat_message("user", avatar="🧑‍🚀"):
            st.markdown(f"🎤 {voice_message}")
        st.session_state.messages.append({"role": "user", "content": voice_message})
        
        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("🧠 Menganalisis..."):
                response = st.session_state.brain.analyze(voice_message)
                stream_response(response)
                create_realistic_voice_html(response, speed=voice_speed, pitch=voice_pitch)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.query_params.clear()
        st.rerun()

# ==========================================
# 11. FOOTER
# ==========================================
st.markdown("""
<div style="text-align: center; padding: 20px; margin-top: 30px; border-top: 1px solid rgba(0,242,254,0.1);">
    <p style="color: #6e6e80;">🎙️ NEXUS REALISTIC VOICE AI • Suara Manusia Natural • Bukan Robot 🎙️</p>
    <p style="color: #6e6e80; font-size: 0.7rem;">Powered by Web Speech API Premium • Einstein Level Intelligence • Real-time Voice</p>
</div>
""", unsafe_allow_html=True)
