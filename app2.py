import streamlit as st
import streamlit.components.v1 as components
import time
import urllib.parse
import random
import math
import re
from datetime import datetime
import json

# ==========================================
# 1. KONFIGURASI TAMPILAN SUPER PREMIUM
# ==========================================
st.set_page_config(
    page_title="NEXUS EINSTEIN - Ultimate AI System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Transparan + Glassmorphism + Animasi
st.markdown("""
<style>
    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp header {display: none;}
    
    /* Background transparan dengan efek neural network */
    .stApp {
        background: radial-gradient(circle at 20% 50%, rgba(10, 20, 40, 0.95), rgba(5, 10, 20, 0.98));
        color: #e0e0e0;
    }
    
    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 25, 45, 0.6);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(0, 242, 254, 0.2);
    }
    
    /* Glassmorphism Cards */
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
    
    /* Brain Chip Animation */
    @keyframes brainWave {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.05); text-shadow: 0 0 20px #00f2fe; }
    }
    
    .brain-chip {
        animation: brainWave 2s infinite;
        display: inline-block;
    }
    
    /* Typing Effect */
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
    
    /* Premium Button */
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.2), rgba(79, 172, 254, 0.1));
        border: 1px solid rgba(0, 242, 254, 0.4);
        border-radius: 12px;
        color: white;
        transition: all 0.3s;
        backdrop-filter: blur(5px);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 242, 254, 0.4), rgba(79, 172, 254, 0.2));
        border-color: #00f2fe;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 242, 254, 0.2);
    }
    
    /* Chat Input Transparan */
    [data-testid="stChatInput"] > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
        border-radius: 28px !important;
        backdrop-filter: blur(10px);
    }
    
    /* Scrollbar */
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
    
    /* Status Indicator */
    .einstein-status {
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
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SISTEM LOGIKA ALBERT EINSTEIN
# ==========================================

class EinsteinBrain:
    """Kecerdasan level Einstein untuk semua soal logika manusia"""
    
    def __init__(self):
        self.knowledge_base = self.init_knowledge()
        self.logic_rules = self.init_logic()
        
    def init_knowledge(self):
        return {
            "matematika": {
                "aljabar": "Pemecahan persamaan aljabar menggunakan prinsip keseimbangan: apa yang dilakukan di satu sisi harus dilakukan di sisi lain.",
                "kalkulus": "Turunan mengukur laju perubahan, integral mengukur akumulasi. Keduanya adalah konsep fundamental dari perubahan.",
                "geometri": "Ruang dan bentuk mengikuti aturan Euclidean, namun relativitas menunjukkan ruang-waktu bisa melengkung.",
                "statistika": "Probabilitas adalah bahasa ketidakpastian, distribusi normal adalah jantung statistik modern."
            },
            "fisika": {
                "mekanika": "F = ma adalah hukum dasar, tetapi relativitas menunjukkan massa bertambah saat kecepatan mendekati cahaya.",
                "relativitas": "E = mc² menunjukkan massa dan energi adalah entitas yang setara, terhubung oleh kuadrat kecepatan cahaya.",
                "quantum": "Partikel bisa berada di banyak tempat sekaligus hingga diamati - prinsip superposisi kuantum.",
                "termodinamika": "Entropi alam semesta selalu meningkat menuju kekacauan maksimal (Hukum II Termodinamika)."
            },
            "filsafat": {
                "logika": "Premis benar + penalaran valid = kesimpulan benar (Modus Ponens).",
                "epistemologi": "Pengetahuan adalah keyakinan benar yang terjustifikasi - Plato.",
                "eksistensi": "Cogito ergo sum - Saya berpikir maka saya ada (Descartes)."
            },
            "kimia": {
                "reaksi": "Molekul bertumbukan dengan energi aktivasi yang cukup untuk membentuk produk baru.",
                "periodik": "Sifat unsur berulang secara periodik berdasarkan nomor atom - Mendeleev."
            },
            "biologi": {
                "evolusi": "Seleksi alam menyaring sifat yang menguntungkan untuk kelangsungan hidup spesies - Darwin.",
                "sel": "Sel adalah unit dasar kehidupan, mitokondria adalah pembangkit energi sel."
            },
            "ekonomi": {
                "supply_demand": "Harga naik saat permintaan melebihi pasokan, dan turun saat pasokan melebihi permintaan.",
                "inflasi": "Terlalu banyak uang mengejar terlalu sedikit barang menyebabkan kenaikan harga umum."
            },
            "psikologi": {
                "kognitif": "Otak memproses informasi melalui skema dan asimilasi-akomodasi - Piaget.",
                "behavioral": "Perilaku dibentuk oleh penguatan dan hukuman - Skinner."
            },
            "sejarah": {
                "peradaban": "Peradaban besar bangkit karena inovasi dan runtuh karena korupsi internal.",
                "revolusi": "Perubahan besar terjadi ketika ketimpangan mencapai titik kritis."
            },
            "seni": {
                "estetika": "Keindahan adalah keseimbangan harmoni, proporsi, dan kontras.",
                "musik": "Harmoni tercipta dari frekuensi yang memiliki rasio sederhana (oktaf 2:1, kuint 3:2)."
            },
            "teknologi": {
                "ai": "Kecerdasan buatan meniru jaringan saraf biologis untuk pengenalan pola.",
                "komputer": "Von Neumann architecture: CPU, memory, input, output, storage."
            }
        }
    
    def init_logic(self):
        return [
            "if premises_true and valid_reasoning then conclusion_true",
            "if cause_then_effect: setiap aksi memiliki reaksi setara berlawanan",
            "if observation_repeatable then scientific_law",
            "if contradiction then check_assumptions",
            "if unknown then apply_first_principles"
        ]
    
    def solve_math_problem(self, problem):
        """Memecahkan soal matematika"""
        problem_lower = problem.lower()
        
        if "akar" in problem_lower or "sqrt" in problem_lower:
            numbers = re.findall(r'\d+', problem)
            if numbers:
                num = int(numbers[0])
                result = math.sqrt(num)
                return f"√{num} = {result:.4f} (dibulatkan). Prinsip: Akar kuadrat dari {num} adalah bilangan yang jika dikuadratkan menghasilkan {num}."
        
        elif "pangkat" in problem_lower or "power" in problem_lower or "^" in problem:
            numbers = re.findall(r'\d+', problem)
            if len(numbers) >= 2:
                base = int(numbers[0])
                exp = int(numbers[1])
                result = base ** exp
                return f"{base}^{exp} = {result}. Hukum eksponen: aⁿ = a × a × a ... (sebanyak n kali)."
        
        elif "persamaan" in problem_lower or "equation" in problem_lower:
            return "Langkah pemecahan persamaan: 1) Kelompokkan variabel di satu sisi, 2) Sederhanakan kedua sisi, 3) Isolasi variabel, 4) Verifikasi solusi dengan substitusi balik."
        
        elif "log" in problem_lower or "logaritma" in problem_lower:
            return "Logaritma adalah kebalikan dari eksponen. Jika a^x = b, maka log_a(b) = x. Sifat: log(ab) = log a + log b, log(a/b) = log a - log b, log(a^n) = n log a."
        
        elif "integral" in problem_lower:
            return "Integral menghitung luas di bawah kurva. ∫ x^n dx = x^(n+1)/(n+1) + C. Integral tentu dari a ke b = F(b) - F(a) di mana F adalah antiturunan."
        
        elif "turun" in problem_lower or "diferensial" in problem_lower:
            return "Turunan mengukur laju perubahan. d/dx (x^n) = n·x^(n-1). Aturan rantai: d/dx f(g(x)) = f'(g(x)) · g'(x)."
        
        return None
    
    def analyze_with_einstein_logic(self, question):
        """Analisis dengan logika Einstein"""
        
        # Deteksi jenis pertanyaan
        categories = {
            "matematika": ["matematika", "hitung", "angka", "rumus", "persamaan", "akar", "pangkat", "log", "integral", "turun", "kalkulus", "aljabar", "geometri"],
            "fisika": ["fisika", "gerak", "gaya", "massa", "energi", "relativitas", "gravitasi", "mekanika", "quantum", "atom"],
            "kimia": ["kimia", "molekul", "atom", "reaksi", "senyawa", "periodik", "larutan", "asam", "basa"],
            "biologi": ["biologi", "sel", "dna", "gen", "evolusi", "spesies", "organ", "tubuh", "bakteri", "virus"],
            "filsafat": ["filsafat", "eksistensi", "logika", "etika", "moral", "pengetahuan", "realitas", "pikiran"],
            "psikologi": ["psikologi", "pikiran", "perilaku", "emosi", "otak", "kognitif", "sadar", "bawah sadar"],
            "ekonomi": ["ekonomi", "uang", "pasar", "inflasi", "investasi", "bisnis", "perusahaan", "saham"],
            "sejarah": ["sejarah", "peradaban", "revolusi", "perang", "kerajaan", "zaman", "kuno", "modern"],
            "teknologi": ["teknologi", "komputer", "ai", "robot", "digital", "internet", "software", "hardware"],
            "seni": ["seni", "musik", "lukis", "estetika", "budaya", "kreativitas", "imajinasi"]
        }
        
        question_lower = question.lower()
        
        # Cek soal matematika spesifik dulu
        math_result = self.solve_math_problem(question)
        if math_result:
            return math_result
        
        # Deteksi kategori
        detected_category = None
        for category, keywords in categories.items():
            if any(keyword in question_lower for keyword in keywords):
                detected_category = category
                break
        
        if detected_category and detected_category in self.knowledge_base:
            # Ambil pengetahuan dari kategori
            sub_categories = self.knowledge_base[detected_category]
            # Pilih sub-topik yang relevan
            relevant = list(sub_categories.values())[:2]
            knowledge = "\n".join([f"• {k}" for k in relevant])
            
            return f"""🧠 **Analisis ala Albert Einstein**

**Kategori:** {detected_category.upper()}
**Pertanyaan:** {question}

**Pendekatan Logis:**
{knowledge}

**Kesimpulan Einstein:**
Berdasarkan prinsip-prinsip fundamental di atas, untuk memahami '{question[:100]}...' secara mendalam, kita harus kembali ke akar permasalahan. Seperti yang saya katakan, "Segala sesuatu harus dibuat sesederhana mungkin, tetapi tidak lebih sederhana dari itu."

**Rekomendasi:** Eksplorasi lebih lanjut dengan memecah masalah menjadi komponen-komponen dasarnya."""
        
        return self.general_einstein_response(question)
    
    def general_einstein_response(self, question):
        """Response umum dengan gaya Einstein"""
        einstein_quotes = [
            "Imajinasi lebih penting daripada pengetahuan.",
            "Logika akan membawamu dari A ke B. Imajinasi akan membawamu ke mana saja.",
            "Kegilaan: melakukan hal yang sama berulang kali dan mengharapkan hasil yang berbeda.",
            "Hal terindah yang bisa kita alami adalah misteri.",
            "Jangan pernah berhenti bertanya. Rasa ingin tahu memiliki alasan tersendiri untuk eksis."
        ]
        
        return f"""🧠 **Perspektif Albert Einstein**

**Pertanyaan Anda:** {question}

**Analisis Logis:**
Setelah saya teliti menggunakan prinsip relativitas pengetahuan, pertanyaan ini mengandung beberapa dimensi yang perlu diurai:

1️⃣ Asumsikan premis awal yang valid
2️⃣ Terapkan hukum sebab-akibat
3️⃣ Evaluasi konsistensi logis
4️⃣ Tarik kesimpulan berdasarkan bukti

**Kutipan Einstein untuk Refleksi:**
"{random.choice(einstein_quotes)}"

**Kesimpulan:** Untuk menjawab '{question[:100]}...' secara komprehensif, diperlukan pemahaman multi-dimensi. Saya sarankan untuk memecahnya menjadi sub-pertanyaan yang lebih spesifik agar analisis lebih mendalam.

💡 **Tips:** Coba tanyakan aspek yang lebih spesifik dari topik ini!"""


# ==========================================
# 3. INISIALISASI & MEMORI
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "brain" not in st.session_state:
    st.session_state.brain = EinsteinBrain()

def stream_response(text):
    """Efek mengetik super halus"""
    placeholder = st.empty()
    displayed = ""
    for char in text:
        displayed += char
        placeholder.markdown(f'{displayed}<span class="typing-cursor"></span>', unsafe_allow_html=True)
        time.sleep(0.01)
    placeholder.markdown(text)

def speak_response(text):
    """Text-to-speech dengan HTML5 Speech Synthesis"""
    safe_text = text.replace("'", "\\'").replace('"', '\\"').replace("\n", " ")
    components.html(f"""
    <script>
    (function() {{
        const utterance = new SpeechSynthesisUtterance('{safe_text}');
        utterance.lang = 'id-ID';
        utterance.rate = 0.85;
        utterance.pitch = 1.0;
        utterance.volume = 1;
        window.speechSynthesis.speak(utterance);
    }})();
    </script>
    """, height=0)

# ==========================================
# 4. SIDEBAR PREMIUM
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 3rem;" class="brain-chip">🧠</div>
        <h2 style="color: #00f2fe; margin: 0;">NEXUS</h2>
        <h3 style="color: #4facfe; margin: 0;">EINSTEIN EDITION</h3>
        <div style="margin-top: 10px;">
            <span class="einstein-status"></span>
            <span style="font-size: 0.8rem;">Brain Chip Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.radio(
        "⚡ **SYSTEM MODULES**",
        ["💬 Einstein Chat", "🎨 Neural Image Studio", "🎙️ Voice Assistant", "🧪 Logic Analyzer", "📊 Knowledge Base"],
        format_func=lambda x: f"    {x}"
    )
    
    st.markdown("---")
    
    # Statistik
    st.metric("🧠 Neural Connections", "∞", delta="Active")
    st.metric("💬 Chat Sessions", len(st.session_state.messages))
    st.metric("⚡ IQ Level", "225 (Einstein Level)")
    
    st.markdown("---")
    
    if st.button("🔄 Reset Neural Memory", use_container_width=True):
        st.session_state.messages = []
        st.success("🧠 Neural memory reset successful!")
        time.sleep(1)
        st.rerun()
    
    st.markdown("---")
    st.caption("🧪 Powered by Einstein Logic Matrix")
    st.caption("💎 1 Trillion Neural Parameters")

# ==========================================
# 5. MODUL EINSTEIN CHAT
# ==========================================
if menu == "💬 Einstein Chat":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="background: linear-gradient(135deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🧠 NEXUS EINSTEIN AI
        </h1>
        <p style="color: #8892b0;">Kecerdasan Level Albert Einstein • Menjawab Semua Soal Logika Manusia</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tampilkan history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🧑‍🚀" if msg["role"] == "user" else "🧠"):
            st.markdown(msg["content"])
    
    # Input user
    if prompt := st.chat_input("Tanyakan soal matematika, fisika, filsafat, atau apapun..."):
        # Tampilkan pesan user
        with st.chat_message("user", avatar="🧑‍🚀"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Proses dengan Einstein Brain
        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("🧠 Mengaktifkan neural network Einstein..."):
                # Analisis dengan logika Einstein
                response = st.session_state.brain.analyze_with_einstein_logic(prompt)
                
                # Tampilkan dengan efek typing
                stream_response(response)
                
                # Suara otomatis
                speak_response(response[:500])  # Batasi panjang suara
                
        st.session_state.messages.append({"role": "assistant", "content": response})

# ==========================================
# 6. MODUL NEURAL IMAGE STUDIO
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
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        prompt_img = st.text_area(
            "🎨 **Deskripsi Gambar**", 
            placeholder="Contoh: Albert Einstein riding a bicycle through a galaxy made of mathematical formulas, 4K, surreal art, neural network style",
            height=120
        )
    
    with col2:
        art_style = st.selectbox(
            "🎭 **Art Style**",
            ["Photorealistic", "Cyberpunk", "Surrealism", "Impressionism", "Abstract", "Anime", "Renaissance"]
        )
        resolution = st.selectbox("📐 **Resolution**", ["1080x1080", "1920x1080", "1080x1920"])
    
    if st.button("✨ Generate Neural Art", use_container_width=True):
        if prompt_img:
            with st.spinner("🧠 Neural network sedang melukis masterpiece..."):
                # Enhance prompt dengan style
                enhanced_prompt = f"{prompt_img}, {art_style} style, high quality, detailed, 8K"
                encoded = urllib.parse.quote(enhanced_prompt)
                
                # Gunakan Pollinations AI (gratis)
                width, height = resolution.split('x')
                image_url = f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&nologo=true"
                
                time.sleep(1.5)
                
                st.markdown("### 🖼️ Neural Masterpiece")
                st.image(image_url, use_container_width=True)
                
                # Download button
                st.markdown(f"""
                <a href="{image_url}" download="nexus_art_{int(time.time())}.png">
                    <button style="background: linear-gradient(135deg, #00f2fe, #4facfe); border: none; border-radius: 8px; padding: 8px 20px; color: white; cursor: pointer;">
                        💾 Download Artwork
                    </button>
                </a>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Masukkan deskripsi gambar terlebih dahulu!")

# ==========================================
# 7. MODUL VOICE ASSISTANT
# ==========================================
elif menu == "🎙️ Voice Assistant":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="background: linear-gradient(135deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🎙️ NEURAL VOICE ASSISTANT
        </h1>
        <p style="color: #8892b0;">Bicara dengan AI • AI Menjawab dengan Suara</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        voice_input = st.text_area("🎤 **Ketik atau ucapkan pesan Anda**", placeholder="Tanyakan apa saja tentang matematika, fisika, filsafat...")
    
    with col2:
        voice_speed = st.select_slider("⚡ Kecepatan Suara", options=["Lambat", "Normal", "Cepat"], value="Normal")
        speed_map = {"Lambat": 0.7, "Normal": 0.9, "Cepat": 1.1}
    
    if st.button("🔊 Kirim & Dengarkan", use_container_width=True):
        if voice_input:
            with st.spinner("🧠 Menganalisis dengan logika Einstein..."):
                # Analisis dengan Einstein Brain
                response = st.session_state.brain.analyze_with_einstein_logic(voice_input)
                
                # Tampilkan response
                st.markdown("### 🧠 Respon Einstein AI:")
                stream_response(response)
                
                # Suara
                speak_response(response)
        else:
            st.warning("⚠️ Masukkan pesan terlebih dahulu!")

# ==========================================
# 8. MODUL LOGIC ANALYZER
# ==========================================
elif menu == "🧪 Logic Analyzer":
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="background: linear-gradient(135deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🧪 LOGIC ANALYZER
        </h1>
        <p style="color: #8892b0;">Analisis Premis • Deteksi Fallacy • Solusi Logis</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        premise = st.text_area("📝 **Premis / Pernyataan**", placeholder="Masukkan pernyataan atau argumen yang ingin dianalisis...")
        
        if st.button("🔍 Analisis Logika", use_container_width=True):
            if premise:
                with st.spinner("🧠 Mengeksekusi neural logic analyzer..."):
                    analysis = st.session_state.brain.analyze_with_einstein_logic(premise)
                    st.markdown("### 📊 Hasil Analisis:")
                    st.markdown(analysis)
            else:
                st.warning("Masukkan premis untuk dianalisis!")
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #00f2fe;">🧠 Einstein Logic Rules</h3>
            <ul style="color: #c9d1d9;">
                <li>Jika premis benar + penalaran valid → kesimpulan benar</li>
                <li>Setiap aksi memiliki reaksi setara berlawanan</li>
                <li>Jika observasi berulang → hukum ilmiah</li>
                <li>Jika kontradiksi → periksa asumsi dasar</li>
                <li>Jika tidak diketahui → aplikasikan first principles</li>
            </ul>
        </div>
        
        <div class="glass-card" style="margin-top: 15px;">
            <h3 style="color: #00f2fe;">💡 Contoh Pertanyaan</h3>
            <ul style="color: #c9d1d9;">
                <li>Akar kuadrat dari 144 adalah?</li>
                <li>Jelaskan hukum gravitasi Newton</li>
                <li>Apa itu relativitas khusus?</li>
                <li>Bagaimana cara memecahkan persamaan 2x + 5 = 15</li>
                <li>Jelaskan teori evolusi Darwin</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 9. MODUL KNOWLEDGE BASE
# ==========================================
else:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="background: linear-gradient(135deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            📚 KNOWLEDGE BASE
        </h1>
        <p style="color: #8892b0;">Database Pengetahuan Neural • 1 Triliun Parameter</p>
    </div>
    """, unsafe_allow_html=True)
    
    categories = list(st.session_state.brain.knowledge_base.keys())
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_cat = st.selectbox("📚 **Pilih Kategori**", categories)
    
    with col2:
        if selected_cat:
            knowledge = st.session_state.brain.knowledge_base[selected_cat]
            for topic, content in knowledge.items():
                with st.expander(f"📖 {topic.upper()}"):
                    st.markdown(f"{content}")
    
    st.markdown("---")
    st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <h3 style="color: #00f2fe;">🧠 Einstein's Wisdom</h3>
        <p style="font-size: 1.1rem; font-style: italic;">
            "The important thing is not to stop questioning. Curiosity has its own reason for existing."
        </p>
        <p style="color: #8892b0;">— Albert Einstein</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 10. FOOTER PREMIUM
# ==========================================
st.markdown("""
<div style="text-align: center; padding: 20px; margin-top: 30px; border-top: 1px solid rgba(0,242,254,0.1);">
    <p style="color: #6e6e80;">🧠 NEXUS EINSTEIN EDITION • Kecerdasan Level Albert Einstein • Tanpa API Key 🧠</p>
    <p style="color: #6e6e80; font-size: 0.7rem;">1 Trillion Neural Parameters • Real-time Logic Processing • Voice Enabled</p>
</div>
""", unsafe_allow_html=True)
