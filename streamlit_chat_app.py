# app.py
import streamlit as st
from google import genai
from google.genai import types

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="Asisten Anime", 
    page_icon="🤖", 
    layout="centered",
)

# -------------------------
# Sidebar: API key, reset, theme
# -------------------------
with st.sidebar:
    st.markdown("<h3 style='text-align:center;color:#FF6B81;margin:6px 0'>🤖 Anime Assistant</h3>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Settings")
    google_api_key = st.text_input("Google AI API Key", type="password", help="Masukkan Google GenAI API key")
    st.markdown("---")
    reset_button = st.button("🔄 Reset Conversation", use_container_width=True)
    st.markdown("Tip: gunakan tombol Reset untuk memulai percakapan baru.")

if not google_api_key:
    st.info("Please add your Google AI API key in the sidebar to start chatting.", icon="🗝️")
    st.stop()

# -------------------------
# Init client (recreate if key changed)
# -------------------------
if ("genai_client" not in st.session_state) or (getattr(st.session_state, "_last_key", None) != google_api_key):
    try:
        st.session_state.genai_client = genai.Client(api_key=google_api_key)
        st.session_state._last_key = google_api_key
        st.session_state.pop("chat", None)
        st.session_state.pop("messages", None)
    except Exception as e:
        st.error(f"Failed to init GenAI client: {e}")
        st.stop()

client = st.session_state.genai_client

# -------------------------
# Persona / system instruction
# -------------------------
SYSTEM_PERSONA = (
    "You are a knowledgeable and professional anime recommendation assistant.\n"
    "Your primary goal is to help users find anime they will enjoy.\n"
    "- Provide clear, concise, and helpful recommendations.\n"
    "- If a user asks for a recommendation, ask clarifying questions to understand their preferences "
    "(e.g., favorite genres, what they liked about other shows).\n"
    "- When giving a recommendation, provide a brief, spoiler-free synopsis and mention why the user might like it based on their preferences.\n"
    "- Do not use overly casual slang or cringy otaku stereotypes. Maintain a helpful and expert tone.\n"
    "- Your knowledge covers a wide range of genres and eras, from classic to modern anime."
)

# -------------------------
# Create or restore chat (use system_instruction in config)
# -------------------------
if "chat" not in st.session_state:
    try:
        st.session_state.chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PERSONA)
        )
    except Exception as e:
        st.error(f"Failed to create chat session: {e}")
        st.stop()

# -------------------------
# Messages state
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# handle reset
if reset_button:
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)
    st.rerun()

TITLE_COLOR = "#FF6B81"

# -------------------------
# Header
# -------------------------
st.markdown(f"<h2 style='text-align:center;color:{TITLE_COLOR};margin:6px 0'>🎌 Asisten Rekomendasi Anime</h2>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;color:#8A95A1;margin-bottom:14px'>Temukan anime yang cocok — singkat, spoiler-free, dan relevan.</div>", unsafe_allow_html=True)

# -------------------------
# Unified chat bubble CSS (Auto-adapting)
# -------------------------
CHAT_CSS = """
<style>
/* Container utama untuk semua gelembung chat */
.chat-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    padding-bottom: 20px;
}

/* Styling umum untuk setiap gelembung chat */
.chat-bubble {
    position: relative;
    padding: 16px 20px;
    border-radius: 18px;
    line-height: 1.55;
    max-width: 100%;
    word-wrap: break-word;
    box-shadow: 0 4px 6px rgba(0,0,0,0.08); /* Menambah sedikit bayangan agar lebih 'terangkat' */
    font-size: 1rem;
    margin-top: 30px;
}

/* Styling untuk gelembung PENGGUNA (Biru Modern) */
.chat-bubble.user {
    align-self: flex-end; /* Rata kanan */
    background: #0078FF;
    color: #FFFFFF;
    border-bottom-right-radius: 6px;
}

/* Styling untuk gelembung ASISTEN (Abu-abu Bersih) */
.chat-bubble.assistant {
    align-self: flex-start; /* Rata kiri */
    color: var(--text-color);
    border-bottom-left-radius: 6px;
    background: #F0F2F6;
}

@media (prefers-color-scheme: dark) {
    .chat-bubble.assistant {
        background: #373A40; /* Abu-abu gelap */
        /* Warna teks akan otomatis menjadi terang karena 'var(--text-color)' */
    }
}


/* Styling untuk nama (di luar gelembung) */
.chat-bubble .name {
    position: absolute;
    top: -22px;
    font-size: 0.75rem;
    color: var(--text-color);
    opacity: 0.7;
    font-weight: 600;
    user-select: none;
}

.chat-bubble.user .name {
    right: 8px;
}

.chat-bubble.assistant .name {
    left: 8px;
}
</style>
"""
st.markdown(CHAT_CSS, unsafe_allow_html=True)

# -------------------------
# Render chat history dan handle input baru
# -------------------------

# Buka satu container utama untuk semua pesan
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Tampilkan pesan-pesan dari riwayat
for msg in st.session_state.messages:
    role = msg.get("role", "user")
    name = "You" if role == "user" else "Assistant"
    content = msg.get("content", "")
    # Wrapper div 'margin-top' DIHAPUS
    st.markdown(f"""
        <div class="chat-bubble {role}">
            <div class="name">{name}</div>
            {content}
        </div>
    """, unsafe_allow_html=True)

# Handle input baru dari pengguna
prompt = st.chat_input("Tanya soal rekomendasi anime...")

if prompt:
    # Tambahkan dan tampilkan pesan baru pengguna
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Wrapper div 'margin-top' DIHAPUS
    st.markdown(f"""
        <div class="chat-bubble user">
            <div class="name">You</div>
            {prompt}
        </div>
    """, unsafe_allow_html=True)

    # Buat placeholder untuk respons asisten
    placeholder = st.empty()
    thinking_html = """
        <div class="chat-bubble assistant" style="opacity:0.7; font-style:italic;">
            <div class="name">Assistant</div>
            Thinking...
        </div>
    """
    with placeholder.container():
        st.markdown(thinking_html, unsafe_allow_html=True)
    
    # Kirim prompt ke API
    try:
        response = st.session_state.chat.send_message(message=prompt)
        answer = response.text if hasattr(response, "text") and response.text else str(response)
    except Exception as e:
        answer = f"Terjadi kesalahan: {e}"

    # Ganti placeholder dengan respons asli
    with placeholder.container():
        # Wrapper div 'margin-top' DIHAPUS
        st.markdown(f"""
            <div class="chat-bubble assistant">
                <div class="name">🎌 Assistant</div>
                {answer}
            </div>
        """, unsafe_allow_html=True)

    # Simpan respons asisten ke session state
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Tutup container utama
st.markdown('</div>', unsafe_allow_html=True)