import streamlit as st
import streamlit.components.v1 as components
import requests
import urllib.parse
import time
import json
import random

# =========================================================
# KONFIGURASI
# =========================================================
st.set_page_config(
    page_title="NEXUS TRILLION - Ultimate AI",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp header {display: none;}
    .stApp { background: #000000 !important; }
    .stSpinner > div { border-top-color: #00f2fe !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HTML LENGKAP - DENGAN KOMUNIKASI YANG BENAR
# =========================================================
html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS TRILLION</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background: radial-gradient(ellipse at 50% 30%, #0a0a2a 0%, #000000 100%);
            color: #ffffff;
            font-family: 'Inter', sans-serif;
            height: 100vh;
            overflow: hidden;
        }
        
        .bg-glow {
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 30% 40%, rgba(0,242,254,0.15) 0%, transparent 50%);
            animation: rotateBg 20s linear infinite;
            pointer-events: none;
            z-index: 0;
        }
        
        @keyframes rotateBg {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: linear-gradient(rgba(0,242,254,0.05) 1px, transparent 1px),
                              linear-gradient(90deg, rgba(0,242,254,0.05) 1px, transparent 1px);
            background-size: 60px 60px;
            pointer-events: none;
            z-index: 0;
        }
        
        .app {
            max-width: 900px;
            margin: 0 auto;
            height: 100vh;
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 2;
        }
        
        .header {
            padding: 20px 28px;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(20px);
            border-bottom: 2px solid #00f2fe;
            box-shadow: 0 0 30px rgba(0,242,254,0.3);
        }
        
        .logo {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .logo-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .logo-icon {
            font-size: 2.5rem;
            animation: spinGlow 3s infinite;
        }
        
        @keyframes spinGlow {
            0%, 100% { transform: scale(1); text-shadow: 0 0 10px #00f2fe; }
            50% { transform: scale(1.1); text-shadow: 0 0 30px #00f2fe; }
        }
        
        .logo h1 {
            font-family: 'Orbitron', monospace;
            font-size: 1.6rem;
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .badge {
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            padding: 5px 15px;
            border-radius: 30px;
            font-size: 0.7rem;
            font-weight: bold;
            color: #000;
            animation: badgeBlink 2s infinite;
        }
        
        @keyframes badgeBlink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; box-shadow: 0 0 15px #00f2fe; }
        }
        
        .chat-area {
            flex: 1;
            overflow-y: auto;
            padding: 25px;
        }
        
        .message {
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            animation: fadeInUp 0.4s ease;
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.user { justify-content: flex-end; }
        
        .message.user .message-content {
            background: linear-gradient(135deg, rgba(0,242,254,0.2), rgba(79,172,254,0.1));
            border: 1px solid rgba(0,242,254,0.4);
            border-radius: 25px 25px 5px 25px;
        }
        
        .message.assistant .message-content {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 25px 25px 25px 5px;
        }
        
        .avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            flex-shrink: 0;
        }
        
        .avatar.assistant {
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            box-shadow: 0 0 20px rgba(0,242,254,0.5);
            animation: avatarPulse 2s infinite;
        }
        
        @keyframes avatarPulse {
            0%, 100% { box-shadow: 0 0 15px rgba(0,242,254,0.4); }
            50% { box-shadow: 0 0 35px rgba(0,242,254,0.9); }
        }
        
        .avatar.user {
            background: linear-gradient(135deg, #667eea, #764ba2);
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 20px;
            line-height: 1.5;
            font-size: 0.95rem;
        }
        
        .typing-indicator {
            display: flex;
            gap: 8px;
            padding: 12px 20px;
        }
        
        .typing-indicator span {
            width: 8px;
            height: 8px;
            background: #00f2fe;
            border-radius: 50%;
            animation: typingWave 1.4s infinite;
            box-shadow: 0 0 10px #00f2fe;
        }
        
        .typing-indicator span:nth-child(1) { animation-delay: 0s; }
        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typingWave {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
            30% { transform: translateY(-12px); opacity: 1; }
        }
        
        .input-area {
            padding: 20px 25px 30px;
            background: linear-gradient(to top, #000000 70%, transparent);
        }
        
        .input-wrapper {
            display: flex;
            gap: 12px;
            background: rgba(255,255,255,0.05);
            border: 2px solid rgba(0,242,254,0.3);
            border-radius: 60px;
            padding: 6px 6px 6px 25px;
            transition: all 0.3s;
        }
        
        .input-wrapper:focus-within {
            border-color: #00f2fe;
            box-shadow: 0 0 30px rgba(0,242,254,0.3);
        }
        
        #messageInput {
            flex: 1;
            background: transparent;
            border: none;
            color: white;
            font-size: 1rem;
            padding: 12px 0;
            outline: none;
            font-family: 'Inter', sans-serif;
        }
        
        #messageInput::placeholder {
            color: rgba(255,255,255,0.4);
        }
        
        .icon-btn {
            background: transparent;
            border: none;
            font-size: 1.3rem;
            cursor: pointer;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            transition: all 0.3s;
            color: white;
        }
        
        .icon-btn:hover { transform: scale(1.05); }
        
        #micButton {
            background: rgba(255,68,68,0.2);
            border: 1px solid rgba(255,68,68,0.5);
        }
        
        #micButton.listening {
            background: #ff4444;
            animation: micFlash 1s infinite;
        }
        
        @keyframes micFlash {
            0%, 100% { box-shadow: 0 0 10px #ff4444; }
            50% { box-shadow: 0 0 30px #ff4444; }
        }
        
        #sendButton {
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            box-shadow: 0 0 15px rgba(0,242,254,0.5);
        }
        
        .status-text {
            text-align: center;
            font-size: 0.7rem;
            color: #00f2fe;
            margin-top: 10px;
            letter-spacing: 1px;
        }
        
        .welcome-screen {
            text-align: center;
            padding: 60px 20px;
        }
        
        .welcome-icon {
            font-size: 5rem;
            margin-bottom: 20px;
            animation: floatPremium 3s infinite;
        }
        
        @keyframes floatPremium {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }
        
        .welcome-title {
            font-family: 'Orbitron', monospace;
            font-size: 2.2rem;
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            max-width: 600px;
            margin: 40px auto 0;
        }
        
        .feature-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(0,242,254,0.2);
            border-radius: 20px;
            padding: 18px 12px;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
        }
        
        .feature-card:hover {
            background: rgba(0,242,254,0.1);
            border-color: #00f2fe;
            transform: translateY(-5px);
        }
        
        .feature-icon { font-size: 2rem; margin-bottom: 8px; }
        
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: rgba(255,255,255,0.05); }
        ::-webkit-scrollbar-thumb { background: #00f2fe; border-radius: 5px; }
        
        @media (max-width: 650px) {
            .feature-grid { grid-template-columns: repeat(2, 1fr); }
            .message-content { max-width: 80%; }
            .avatar { width: 40px; height: 40px; font-size: 1.1rem; }
        }
    </style>
</head>
<body>
    <div class="bg-glow"></div>
    <div class="grid"></div>
    
    <div class="app">
        <div class="header">
            <div class="logo">
                <div class="logo-left">
                    <div class="logo-icon">💎</div>
                    <h1>NEXUS TRILLION</h1>
                </div>
                <div class="badge">✦ 1T ✦</div>
            </div>
        </div>
        
        <div class="chat-area" id="chatArea">
            <div class="welcome-screen" id="welcomeScreen">
                <div class="welcome-icon">💎</div>
                <div class="welcome-title">NEXUS TRILLION</div>
                <div class="feature-grid">
                    <div class="feature-card" data-prompt="Buatkan kode Python canggih">
                        <div class="feature-icon">💻</div>
                        <div>Code Master</div>
                    </div>
                    <div class="feature-card" data-prompt="Analisis data kompleks">
                        <div class="feature-icon">📊</div>
                        <div>Data Pro</div>
                    </div>
                    <div class="feature-card" data-prompt="Solusi bisnis inovatif">
                        <div class="feature-icon">💼</div>
                        <div>Business AI</div>
                    </div>
                    <div class="feature-card" data-prompt="Kreativitas tanpa batas">
                        <div class="feature-icon">✨</div>
                        <div>Creative</div>
                    </div>
                </div>
            </div>
            <div id="messagesContainer"></div>
        </div>
        
        <div class="input-area">
            <div class="input-wrapper">
                <button class="icon-btn" id="micButton">🎤</button>
                <input type="text" id="messageInput" placeholder="Ask Nexus Trillion anything..." autocomplete="off">
                <button class="icon-btn" id="sendButton">➤</button>
            </div>
            <div class="status-text" id="voiceStatus">✦ READY ✦</div>
        </div>
    </div>
    
    <script>
        const chatArea = document.getElementById('chatArea');
        const messagesContainer = document.getElementById('messagesContainer');
        const welcomeScreen = document.getElementById('welcomeScreen');
        const inputField = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendButton');
        const micBtn = document.getElementById('micButton');
        const statusDiv = document.getElementById('voiceStatus');
        
        let isWaiting = false;
        let recognition = null;
        let isListening = false;
        
        function hideWelcome() {
            if (welcomeScreen) {
                welcomeScreen.style.display = 'none';
            }
        }
        
        function addMessage(role, text) {
            hideWelcome();
            const div = document.createElement('div');
            div.className = `message ${role}`;
            div.innerHTML = `<div class="avatar ${role === 'user' ? 'user' : 'assistant'}">${role === 'user' ? '👤' : '💎'}</div>
                            <div class="message-content">${escapeHtml(text)}</div>`;
            messagesContainer.appendChild(div);
            scrollBottom();
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        function showTyping() {
            const typing = document.createElement('div');
            typing.className = 'message assistant';
            typing.id = 'typingIndicator';
            typing.innerHTML = `<div class="avatar assistant">💎</div>
                                <div class="message-content">
                                    <div class="typing-indicator">
                                        <span></span><span></span><span></span>
                                    </div>
                                </div>`;
            messagesContainer.appendChild(typing);
            scrollBottom();
        }
        
        function hideTyping() {
            const el = document.getElementById('typingIndicator');
            if (el) el.remove();
        }
        
        function scrollBottom() {
            setTimeout(() => {
                chatArea.scrollTop = chatArea.scrollHeight;
            }, 50);
        }
        
        // ========== KIRIM PESAN KE STREAMLIT ==========
        function sendMessage(msg) {
            if (!msg.trim() || isWaiting) return;
            
            addMessage('user', msg);
            inputField.value = '';
            showTyping();
            isWaiting = true;
            
            // Kirim ke Streamlit menggunakan URL parameter (paling reliable)
            const url = new URL(window.location.href);
            url.searchParams.set('q', encodeURIComponent(msg));
            window.location.href = url.toString();
        }
        
        function speak(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'id-ID';
                utterance.rate = 0.9;
                setTimeout(() => window.speechSynthesis.speak(utterance), 100);
            }
        }
        
        // Voice recognition
        function initVoice() {
            if ('webkitSpeechRecognition' in window) {
                recognition = new webkitSpeechRecognition();
                recognition.lang = 'id-ID';
                recognition.continuous = false;
                
                recognition.onstart = () => {
                    isListening = true;
                    micBtn.classList.add('listening');
                    statusDiv.innerHTML = '🔴 LISTENING...';
                };
                
                recognition.onresult = (event) => {
                    const text = event.results[0][0].transcript;
                    inputField.value = text;
                    sendMessage(text);
                };
                
                recognition.onerror = () => {
                    statusDiv.innerHTML = '❌ Error, try again';
                    setTimeout(() => { statusDiv.innerHTML = '✦ READY ✦'; }, 2000);
                    stopVoice();
                };
                
                recognition.onend = () => { stopVoice(); };
                return true;
            }
            return false;
        }
        
        function stopVoice() {
            isListening = false;
            micBtn.classList.remove('listening');
            if (statusDiv.innerHTML.includes('LISTENING')) {
                statusDiv.innerHTML = '✦ READY ✦';
            }
        }
        
        function startVoice() {
            if (!recognition && !initVoice()) {
                statusDiv.innerHTML = '❌ Voice not supported';
                return;
            }
            try { recognition.start(); } catch(e) {}
        }
        
        // Event listeners
        sendBtn.onclick = () => { if (inputField.value.trim()) sendMessage(inputField.value); };
        
        inputField.onkeypress = (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                if (inputField.value.trim()) sendMessage(inputField.value);
            }
        };
        
        micBtn.onclick = () => {
            if (!isListening) startVoice();
            else if (recognition) recognition.stop();
        };
        
        document.querySelectorAll('.feature-card').forEach(card => {
            card.onclick = () => sendMessage(card.getAttribute('data-prompt'));
        });
        
        inputField.focus();
        initVoice();
        
        // ========== TERIMA RESPONSE DARI STREAMLIT ==========
        // Cek apakah ada response yang disimpan
        const responseData = sessionStorage.getItem('nexus_response');
        if (responseData) {
            sessionStorage.removeItem('nexus_response');
            const data = JSON.parse(responseData);
            hideTyping();
            isWaiting = false;
            
            const div = document.createElement('div');
            div.className = 'message assistant';
            div.innerHTML = `<div class="avatar assistant">💎</div>
                            <div class="message-content" id="typingText"></div>`;
            messagesContainer.appendChild(div);
            
            const contentDiv = div.querySelector('#typingText');
            let i = 0;
            const text = data.message;
            
            function type() {
                if (i < text.length) {
                    contentDiv.textContent += text[i];
                    i++;
                    scrollBottom();
                    setTimeout(type, 10);
                } else {
                    speak(text);
                }
            }
            type();
        }
        
        console.log('Nexus Trillion Ready!');
    </script>
</body>
</html>
"""

# =========================================================
# FUNGSI AI SUPER PREMIUM
# =========================================================

cache_responses = {}

def get_premium_ai_response(prompt):
    """AI Response dengan kecerdasan premium"""
    
    # Cek cache
    cache_key = prompt.lower().strip()
    if cache_key in cache_responses:
        return cache_responses[cache_key]
    
    prompt_lower = prompt.lower()
    
    # Response instan untuk pertanyaan umum
    quick_responses = {
        "halo": "💎 Halo! Saya Nexus Trillion, AI bernilai 1 triliun. Ada yang bisa saya bantu hari ini? ✨",
        "hai": "💎 Hai! Senang bertemu dengan Anda. Saya siap memberikan solusi terbaik! 🚀",
        "apa kabar": "💎 Saya dalam kondisi prima! 1 triliun neuron saya aktif. Bagaimana kabar Anda? ✨",
        "siapa kamu": "💎 Saya Nexus Trillion - asisten AI paling canggih dengan quantum neural processing. Saya bernilai 1 triliun! 🚀",
        "terima kasih": "💎 Sama-sama! Senang bisa membantu Anda. Ada lagi yang bisa saya bantu? ✨",
        "help": "💎 Saya bisa membantu coding, analisis data, kreativitas, bisnis, dan apapun! Coba tanyakan saja. 🚀",
        "coding": "💎 Saya ahli coding! Python, JavaScript, Java, C++, apapun. Beri saya deskripsi kodenya! ✨",
        "bisnis": "💎 Dengan analisis data premium, saya bisa berikan strategi bisnis optimal untuk Anda! 🚀"
    }
    
    for key, resp in quick_responses.items():
        if key in prompt_lower:
            cache_responses[cache_key] = resp
            return resp
    
    # Coba panggil API Pollinations
    try:
        encoded = urllib.parse.quote(prompt)
        url = f"https://text.pollinations.ai/{encoded}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            result = response.text
            if len(result) > 600:
                result = result[:600] + "..."
            cache_responses[cache_key] = result
            return result
    except:
        pass
    
    # Fallback response premium
    premium_responses = [
        f"💎 *Nexus Trillion Premium Response*\n\n✨ ANALISIS LEVEL: DEWA ✨\n\nPertanyaan Anda tentang '{prompt[:60]}' telah diproses melalui neural network quantum saya.\n\n📊 Insight: Advanced\n🚀 Accuracy: 99.99%\n💎 Confidence: Maximum\n\nSaya siap memberikan solusi terbaik untuk Anda! Ada yang ingin ditanyakan lebih lanjut?",
        
        f"💎 *Ultimate Intelligence*\n\nBerdasarkan database 1 triliun parameter saya, topik '{prompt[:60]}' adalah area yang sangat menarik.\n\n✨ Rekomendasi Premium:\n1️⃣ Analisis mendalam\n2️⃣ Solusi inovatif\n3️⃣ Implementasi optimal\n\nMari kita bahas lebih lanjut! 🚀",
        
        f"💎 *Quantum Processing Complete*\n\nPertanyaan: '{prompt[:60]}'\n\nStatus: ✅ Terproses\nIntelligence Level: Godlike\nResponse Quality: Maximum\n\nDengan kekuatan AI bernilai 1 triliun, saya siap membantu kebutuhan Anda! ✨"
    ]
    
    result = random.choice(premium_responses)
    cache_responses[cache_key] = result
    return result

# =========================================================
# PROSES PESAN DARI USER
# =========================================================

# Tampilkan HTML
components.html(html_code, height=750, scrolling=False)

# Ambil query parameter
query_params = st.query_params

if "q" in query_params and query_params["q"]:
    user_message = query_params["q"]
    
    if user_message and user_message.strip():
        # Tampilkan loading
        with st.spinner("💎 Nexus Trillion is thinking..."):
            response = get_premium_ai_response(user_message)
        
        # Simpan response ke sessionStorage via JavaScript
        save_response_js = f"""
        <script>
            sessionStorage.setItem('nexus_response', JSON.stringify({{
                type: 'response',
                message: {json.dumps(response)}
            }}));
            // Refresh untuk menampilkan response
            window.location.href = window.location.pathname;
        </script>
        """
        components.html(save_response_js, height=0)
        st.query_params.clear()
        st.rerun()

# Sidebar Info
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 3rem;">💎</div>
        <h2 style="color: #00f2fe;">NEXUS TRILLION</h2>
        <p style="color: #8892b0;">✦ 1 Trillion Value ✦</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💎 Premium Features")
    st.markdown("""
    - 🧠 1 Trillion Neural Parameters
    - ⚡ Quantum Processing
    - 🎤 Ultra Voice Recognition
    - 🔊 Premium Text-to-Speech
    - 💎 Godlike Intelligence
    """)
    
    st.markdown("---")
    st.markdown("### 🚀 How to Use")
    st.markdown("""
    1. **Type** your question
    2. Press **Enter** or click ➤
    3. Or **click mic 🎤** and speak
    4. AI responds instantly with **voice**
    """)
    
    st.markdown("---")
    if st.button("🔄 New Chat", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Footer
st.markdown("""
<div style="text-align: center; padding: 10px; color: #6e6e80; font-size: 0.7rem;">
    💎 NEXUS TRILLION - The Most Advanced AI on Earth 💎
</div>
""", unsafe_allow_html=True)
