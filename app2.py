import streamlit as st
import streamlit.components.v1 as components
import time
import urllib.parse
import random
import re
from datetime import datetime

# ==========================================
# 1. KONFIGURASI TAMPILAN PREMIUM
# ==========================================
st.set_page_config(
    page_title="Nexus AI - Next Gen Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Style Gemini/Claude/DeepSeek
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp header {display: none;}
    .stDeployButton {display: none;}
    
    /* Main background */
    .stApp {
        background: #0f0f13 !important;
    }
    
    /* Main container */
    .main .block-container {
        max-width: 900px;
        padding-top: 0;
        padding-bottom: 0;
    }
    
    /* Chat messages like Claude/Gemini */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        padding: 1.5rem 0 !important;
        border: none !important;
    }
    
    /* Typing animation */
    .typing-indicator {
        display: flex;
        gap: 6px;
        padding: 0.5rem 0;
    }
    
    .typing-indicator span {
        width: 8px;
        height: 8px;
        background: #6e6e80;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
        30% { transform: translateY(-10px); opacity: 1; }
    }
    
    /* Code blocks like DeepSeek */
    .message-content pre {
        background: #1a1a1e;
        border-radius: 12px;
        padding: 1rem;
        overflow-x: auto;
        margin: 0.75rem 0;
        font-size: 0.85rem;
    }
    
    .message-content code {
        background: #1a1a1e;
        padding: 0.2rem 0.4rem;
        border-radius: 6px;
        font-size: 0.85rem;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 5px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: #3a3a40;
        border-radius: 3px;
    }
    
    /* Sidebar like Claude */
    [data-testid="stSidebar"] {
        background: #0a0a0e;
        border-right: 1px solid #1a1a1e;
    }
    
    /* Input container fixed bottom like ChatGPT */
    .input-fixed {
        position: fixed;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 900px;
        background: linear-gradient(to top, #0f0f13 70%, transparent);
        padding: 1rem 1rem 1.5rem 1rem;
        z-index: 100;
    }
    
    /* Model selector like Gemini */
    .model-selector {
        background: #1a1a1e;
        border-radius: 30px;
        padding: 0.25rem;
        display: inline-flex;
        margin-bottom: 0.75rem;
    }
    
    .model-option {
        padding: 0.4rem 1rem;
        border-radius: 28px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .model-option.active {
        background: #2a2a2e;
        color: #00f2fe;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SYSTEM PROMPT & BRAIN
# ==========================================

class NexusBrain:
    def __init__(self):
        self.knowledge = {
            "math": "Untuk soal matematika, gunakan pendekatan sistematis: identifikasi masalah, terapkan rumus yang tepat, hitung dengan teliti, dan verifikasi hasil.",
            "physics": "Fisika adalah studi tentang alam semesta. Hukum-hukum fundamental seperti gravitasi, elektromagnetisme, dan mekanika kuantum mengatur fenomena alam.",
            "philosophy": "Filsafat mengajarkan kita untuk mempertanyakan asumsi dasar, mencari kebenaran, dan memahami makna eksistensi.",
            "code": "Pemrograman adalah seni memecahkan masalah dengan logika. Tulis kode yang bersih, terstruktur, dan mudah dipahami orang lain."
        }
    
    def respond(self, prompt):
        prompt_lower = prompt.lower()
        
        if any(x in prompt_lower for x in ["halo", "hai", "hello", "hi"]):
            return "Halo! Ada yang bisa saya bantu hari ini? Saya Nexus AI, siap membantu Anda dengan pertanyaan apa pun. ✨"
        
        if any(x in prompt_lower for x in ["apa kabar", "how are you"]):
            return "Saya baik-baik saja, terima kasih! Selalu siap membantu. Ada yang ingin Anda diskusikan? 😊"
        
        if any(x in prompt_lower for x in ["siapa kamu", "who are you"]):
            return "Saya Nexus AI, asisten cerdas yang siap membantu Anda dengan berbagai pertanyaan - dari matematika, fisika, pemrograman, hingga filsafat. Ada yang bisa saya bantu?"
        
        if any(x in prompt_lower for x in ["terima kasih", "thanks", "thank you"]):
            return "Sama-sama! Senang bisa membantu. Jika ada pertanyaan lain, jangan ragu untuk bertanya ya! ✨"
        
        if any(x in prompt_lower for x in ["matematika", "math", "hitung", "rumus"]):
            return f"**Tentang Matematika:**\n\n{self.knowledge['math']}\n\nApakah Anda ingin saya membantu memecahkan soal matematika tertentu?"
        
        if any(x in prompt_lower for x in ["fisika", "physics", "gravitasi", "relativitas"]):
            return f"**Tentang Fisika:**\n\n{self.knowledge['physics']}\n\nAda konsep fisika yang ingin Anda pahami lebih dalam?"
        
        if any(x in prompt_lower for x in ["kode", "code", "program", "python", "javascript"]):
            return f"**Tentang Pemrograman:**\n\n{self.knowledge['code']}\n\nButuh bantuan coding? Saya siap membantu!"
        
        if any(x in prompt_lower for x in ["filsafat", "philosophy", "eksistensi", "makna"]):
            return f"**Tentang Filsafat:**\n\n{self.knowledge['philosophy']}\n\nPertanyaan filosofis yang menarik! Mari kita diskusikan lebih lanjut."
        
        return f"""Menarik sekali pertanyaan Anda!

Saya akan coba analisis: "{prompt[:100]}{'...' if len(prompt) > 100 else ''}"

Untuk memberikan jawaban yang lebih tepat, bisakah Anda memberikan konteks atau detail tambahan? Atau jika ini tentang topik tertentu (matematika, fisika, coding, dll), beri tahu saya ya!

Saya siap membantu! 💫"""

# ==========================================
# 3. INISIALISASI
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "brain" not in st.session_state:
    st.session_state.brain = NexusBrain()
    
if "model" not in st.session_state:
    st.session_state.model = "Nexus Pro"

def stream_text(text, placeholder):
    """Efek mengetik seperti ChatGPT"""
    displayed = ""
    for char in text:
        displayed += char
        placeholder.markdown(displayed)
        time.sleep(0.008)

# ==========================================
# 4. SIDEBAR - Seperti Claude/Gemini
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0;">
        <div style="font-size: 2.5rem;">✨</div>
        <h2 style="color: #e1e1e1; margin: 0.5rem 0;">Nexus AI</h2>
        <p style="color: #6e6e80; font-size: 0.8rem;">Next Generation Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Model selector seperti Gemini
    st.markdown("#### 🤖 Model")
    model_options = ["Nexus Pro", "Nexus Fast", "Nexus Creative"]
    selected_model = st.selectbox("Pilih model", model_options, label_visibility="collapsed")
    if selected_model != st.session_state.model:
        st.session_state.model = selected_model
        st.rerun()
    
    st.markdown("---")
    
    # Stats
    st.markdown("#### 📊 Stats")
    st.caption(f"💬 {len(st.session_state.messages)} messages")
    
    st.markdown("---")
    
    # New chat button
    if st.button("✏️ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    # Info
    st.markdown("""
    <div style="background: #1a1a1e; border-radius: 12px; padding: 1rem;">
        <p style="color: #6e6e80; font-size: 0.7rem; margin: 0;">
            ✨ Nexus AI mampu menjawab pertanyaan tentang:
            <br>• Matematika & Fisika
            <br>• Pemrograman & Coding
            <br>• Filsafat & Logika
            <br>• Dan berbagai topik lainnya
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. HEADER - Seperti Claude
# ==========================================
st.markdown("""
<div style="padding: 1rem 0 0.5rem 0;">
    <h1 style="font-size: 1.8rem; font-weight: 600; margin: 0; background: linear-gradient(135deg, #e1e1e1, #8b8b8b); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        Nexus AI
    </h1>
    <p style="color: #6e6e80; margin-top: 0.25rem;">Ask me anything — math, code, philosophy, or just chat</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. CHAT HISTORY
# ==========================================
chat_container = st.container()

with chat_container:
    if len(st.session_state.messages) == 0:
        # Welcome screen seperti ChatGPT/Gemini
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">✨</div>
            <h3 style="font-weight: 500;">How can I help you today?</h3>
            <p style="color: #6e6e80; margin-top: 0.5rem;">Try asking me about math, coding, physics, or philosophy</p>
            
            <div style="display: flex; flex-wrap: wrap; gap: 0.75rem; justify-content: center; margin-top: 2rem;">
                <button class="example-btn" onclick="setExample('Jelaskan hukum gravitasi Newton')" style="background: #1a1a1e; border: 1px solid #2a2a2e; border-radius: 24px; padding: 0.5rem 1rem; color: #e1e1e1; cursor: pointer;">🌌 Hukum Gravitasi</button>
                <button class="example-btn" onclick="setExample('Buatkan kode Python untuk menghitung faktorial')" style="background: #1a1a1e; border: 1px solid #2a2a2e; border-radius: 24px; padding: 0.5rem 1rem; color: #e1e1e1; cursor: pointer;">💻 Kode Python</button>
                <button class="example-btn" onclick="setExample('Apa itu relativitas?')" style="background: #1a1a1e; border: 1px solid #2a2a2e; border-radius: 24px; padding: 0.5rem 1rem; color: #e1e1e1; cursor: pointer;">⚡ Relativitas</button>
                <button class="example-btn" onclick="setExample('Jelaskan logika filsafat')" style="background: #1a1a1e; border: 1px solid #2a2a2e; border-radius: 24px; padding: 0.5rem 1rem; color: #e1e1e1; cursor: pointer;">📚 Filsafat</button>
            </div>
        </div>
        
        <script>
        function setExample(text) {
            const input = document.querySelector('textarea');
            if (input) {
                input.value = text;
                input.focus();
                input.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
        </script>
        """, unsafe_allow_html=True)
    
    # Tampilkan chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ==========================================
# 7. INPUT AREA - FIXED BOTTOM
# ==========================================
# Spacer untuk memberi ruang input
st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

# Input fixed di bottom
input_container = st.container()
with input_container:
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        if prompt := st.chat_input("Message Nexus AI...", key="main_input"):
            # Tambah pesan user
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Tampilkan pesan user
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Proses AI
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown('<div class="typing-indicator"><span></span><span></span><span></span></div>', unsafe_allow_html=True)
                
                # Dapatkan response
                response = st.session_state.brain.respond(prompt)
                
                # Hapus typing indicator
                message_placeholder.empty()
                
                # Stream response
                stream_text(response, message_placeholder)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

# ==========================================
# 8. HANDLE VOICE INPUT (Optional - tidak otomatis)
# ==========================================
# Tombol mic untuk voice input (manual, tidak otomatis baca)
voice_html = """
<div style="position: fixed; bottom: 110px; right: 30px; z-index: 1000;">
    <button id="voiceInputBtn" style="
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #1a1a1e;
        border: 1px solid #2a2a2e;
        cursor: pointer;
        font-size: 1.3rem;
        transition: all 0.2s;
    ">
        🎤
    </button>
</div>

<script>
let recognition = null;
let isListening = false;

function initVoice() {
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.lang = 'id-ID';
        recognition.continuous = false;
        
        recognition.onstart = () => {
            isListening = true;
            const btn = document.getElementById('voiceInputBtn');
            btn.style.background = '#ff4444';
            btn.style.color = 'white';
        };
        
        recognition.onresult = (event) => {
            const text = event.results[0][0].transcript;
            const textarea = document.querySelector('textarea');
            if (textarea) {
                textarea.value = text;
                textarea.focus();
                textarea.dispatchEvent(new Event('input', { bubbles: true }));
            }
        };
        
        recognition.onend = () => {
            isListening = false;
            const btn = document.getElementById('voiceInputBtn');
            btn.style.background = '#1a1a1e';
            btn.style.color = '#e1e1e1';
        };
        
        return true;
    }
    return false;
}

document.getElementById('voiceInputBtn').onclick = function() {
    if (!recognition) {
        if (!initVoice()) {
            alert('Voice input not supported. Please use Chrome!');
            return;
        }
    }
    if (!isListening) {
        recognition.start();
    } else {
        recognition.stop();
    }
};
</script>
"""

components.html(voice_html, height=0)

# ==========================================
# 9. FOOTER
# ==========================================
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #6e6e80; font-size: 0.7rem;">
    ✨ Nexus AI • Powered by Advanced Intelligence • No Voice Auto-read ✨
</div>
""", unsafe_allow_html=True)
