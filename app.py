
import os
import streamlit as st
from groq import Groq
from datetime import datetime
import sqlite3
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def init_db():
    conn = sqlite3.connect('pharmassist.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  role TEXT, content TEXT,
                  time TEXT, language TEXT)''')
    conn.commit()
    conn.close()

def save_message(role, content, time, language):
    conn = sqlite3.connect('pharmassist.db')
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES (NULL,?,?,?,?)",
              (role, content, time, language))
    conn.commit()
    conn.close()

def load_messages(language):
    conn = sqlite3.connect('pharmassist.db')
    c = conn.cursor()
    c.execute("SELECT role,content,time FROM history WHERE language=? ORDER BY id", (language,))
    rows = c.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1], "time": r[2]} for r in rows]

def clear_history_db(language):
    conn = sqlite3.connect('pharmassist.db')
    c = conn.cursor()
    c.execute("DELETE FROM history WHERE language=?", (language,))
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="PharmAssist AI", page_icon="💊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;600&display=swap');
* { font-family: 'Rajdhani', sans-serif; }
.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
.main-title {
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 2.5em;
    font-weight: bold;
    background: linear-gradient(90deg, #00d2ff, #7b2ff7, #00d2ff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
    padding: 10px;
}
@keyframes shine { to { background-position: 200% center; } }
.welcome-card {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(0,210,255,0.3);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    text-align: center;
    margin-bottom: 20px;
}
.doctor-animation {
    font-size: 80px;
    animation: bounce 2s infinite;
    display: block;
    text-align: center;
}
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-15px); }
}
.greeting-text {
    font-size: 1.8em;
    font-weight: bold;
    background: linear-gradient(90deg, #00d2ff, #7b2ff7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.datetime-card {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 8px 15px;
    border: 1px solid rgba(255,255,255,0.1);
    display: inline-block;
    color: rgba(255,255,255,0.8);
    margin: 5px;
}
.stChatMessage {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 15px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
    margin: 10px 0 !important;
    transition: transform 0.2s ease !important;
}
.stChatMessage:hover { transform: translateX(5px) !important; }
.stButton > button {
    background: linear-gradient(90deg, #00d2ff, #7b2ff7) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 15px rgba(123,47,247,0.4) !important;
    transition: all 0.3s ease !important;
    font-weight: bold !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(123,47,247,0.7) !important;
}
section[data-testid="stSidebar"] {
    background: rgba(15,12,41,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.1) !important;
}
</style>
""", unsafe_allow_html=True)

def get_greeting(language):
    hour = datetime.now().hour
    if 5 <= hour < 12:
        t = "morning"
    elif 12 <= hour < 17:
        t = "afternoon"
    elif 17 <= hour < 21:
        t = "evening"
    else:
        t = "night"
    greetings = {
        "English": {"morning": "☀️ Good Morning!", "afternoon": "🌤️ Good Afternoon!", "evening": "🌆 Good Evening!", "night": "🌙 Good Night!"},
        "Roman Urdu": {"morning": "☀️ Subah Bakhair!", "afternoon": "🌤️ Dopahar Bakhair!", "evening": "🌆 Sham Bakhair!", "night": "🌙 Shab Bakhair!"},
        "اردو": {"morning": "☀️ صبح بخیر!", "afternoon": "🌤️ دوپہر بخیر!", "evening": "🌆 شام بخیر!", "night": "🌙 شب بخیر!"}
    }
    return greetings[language][t]

languages = {
    "English": {
        "title": "💊 PharmAssist AI",
        "subtitle": "Your Personal Pharmacy Assistant",
        "input": "Type your question...",
        "system": "You are PharmAssist AI, a professional pharmacy assistant. When asked about a medicine provide: 1) What it does 2) Dose 3) Side effects 4) Drug interactions 5) Warnings. Be friendly and professional."
    },
    "Roman Urdu": {
        "title": "💊 PharmAssist AI",
        "subtitle": "Aapka Personal Pharmacy Assistant",
        "input": "Apna sawaal likho...",
        "system": "Tum PharmAssist AI ho, ek professional pharmacy assistant. Jab koi medicine ka naam likhe yeh batao: 1) Medicine ka kaam 2) Dose 3) Side effects 4) Drug interactions 5) Warnings. Friendly Roman Urdu mein jawab do."
    },
    "اردو": {
        "title": "💊 فارم اسسٹ اے آئی",
        "subtitle": "آپ کا ذاتی فارمیسی اسسٹنٹ",
        "input": "اپنا سوال لکھیں...",
        "system": "آپ فارم اسسٹ اے آئی ہیں۔ دوائی کے بارے میں پوچھنے پر بتائیں: 1) کام 2) خوراک 3) مضر اثرات 4) تعامل 5) احتیاطیں۔ آسان اردو میں جواب دیں۔"
    }
}

if "language" not in st.session_state:
    st.session_state.language = "Roman Urdu"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = load_messages(st.session_state.language)
if "messages" not in st.session_state:
    L = languages[st.session_state.language]
    st.session_state.messages = [{"role": "system", "content": L['system']}]
    for chat in st.session_state.chat_history:
        st.session_state.messages.append({"role": chat["role"], "content": chat["content"]})
if "prompt_trigger" not in st.session_state:
    st.session_state.prompt_trigger = None

# ═══════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════
with st.sidebar:
    st.markdown("### 🌍 Language")
    selected_lang = st.selectbox("", list(languages.keys()),
                                  index=list(languages.keys()).index(st.session_state.language))
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.session_state.chat_history = load_messages(selected_lang)
        L = languages[selected_lang]
        st.session_state.messages = [{"role": "system", "content": L['system']}]
        for chat in st.session_state.chat_history:
            st.session_state.messages.append({"role": chat["role"], "content": chat["content"]})
        st.rerun()

    L = languages[st.session_state.language]

    st.markdown("---")
    st.markdown("### 📊 Stats")
    total = len([m for m in st.session_state.chat_history if m['role'] == 'user'])
    st.metric("Total Questions", total)

    st.markdown("---")
    st.markdown("### 🔧 Medicine Tools")
    med_search = st.text_input("💊 Medicine Search", placeholder="e.g. Paracetamol")
    if st.button("🔍 Search", use_container_width=True):
        if med_search:
            st.session_state.prompt_trigger = f"Complete info about {med_search}: uses, dose, side effects, interactions, warnings."
            st.rerun()

    st.markdown("---")
    med_dose = st.text_input("⚖️ Dose Calculator", placeholder="e.g. Amoxicillin")
    weight = st.number_input("Weight (kg)", min_value=1, max_value=200, value=70)
    if st.button("💊 Calculate Dose", use_container_width=True):
        if med_dose:
            st.session_state.prompt_trigger = f"Calculate dose of {med_dose} for {weight}kg patient. Adult and child doses."
            st.rerun()

    st.markdown("---")
    drug1 = st.text_input("Drug 1", placeholder="e.g. Aspirin")
    drug2 = st.text_input("Drug 2", placeholder="e.g. Warfarin")
    if st.button("⚠️ Check Interaction", use_container_width=True):
        if drug1 and drug2:
            st.session_state.prompt_trigger = f"Drug interaction between {drug1} and {drug2}. Safe to take together?"
            st.rerun()

    st.markdown("---")
    st.markdown("### 🗑️ Chat Controls")
    if st.button("🗑️ Clear Screen", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.messages = [{"role": "system", "content": L['system']}]
        st.rerun()

    if st.button("❌ Delete All History", use_container_width=True):
        clear_history_db(st.session_state.language)
        st.session_state.chat_history = []
        st.session_state.messages = [{"role": "system", "content": L['system']}]
        st.rerun()

    st.markdown("---")
    st.markdown("### 📜 History")
    history = load_messages(st.session_state.language)
    if not history:
        st.caption("Koi history nahi hai!")
    else:
        user_msgs = [c for c in history if c["role"] == "user"]
        for chat in user_msgs[-10:]:
            st.caption(f"🧑 {chat['content'][:40]}...")

# ═══════════════════════════════════
# MAIN AREA
# ═══════════════════════════════════
L = languages[st.session_state.language]
st.markdown(f'<div class="main-title">{L["title"]}</div>', unsafe_allow_html=True)

now = datetime.now()
greeting = get_greeting(st.session_state.language)
date_str = now.strftime("%A, %d %B %Y")
time_str = now.strftime("%I:%M %p")

st.markdown(f"""
<div class="welcome-card">
    <span class="doctor-animation">👨‍⚕️</span>
    <div class="greeting-text">{greeting}</div>
    <span class="datetime-card">📅 {date_str}</span>
    <span class="datetime-card">🕐 {time_str}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

if len(st.session_state.chat_history) == 0:
    st.info("💊 Koi bhi medicine ka sawaal poochho!")

for chat in st.session_state.chat_history:
    avatar = "🧑" if chat["role"] == "user" else "👨‍⚕️"
    with st.chat_message(chat["role"], avatar=avatar):
        st.write(chat["content"])
        st.caption(chat.get("time", ""))

prompt = st.session_state.prompt_trigger
if prompt:
    st.session_state.prompt_trigger = None

user_input = st.chat_input(L['input'])
if user_input:
    prompt = user_input

if prompt:
    time_now = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.chat_history.append({"role": "user", "content": prompt, "time": time_now})
    save_message("user", prompt, time_now, st.session_state.language)

    with st.chat_message("user", avatar="🧑"):
        st.write(prompt)
        st.caption(time_now)

    with st.chat_message("assistant", avatar="👨‍⚕️"):
        with st.spinner("💭 Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
        st.write(reply)
        st.caption(time_now)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.chat_history.append({"role": "assistant", "content": reply, "time": time_now})
    save_message("assistant", reply, time_now, st.session_state.language)
    st.rerun()