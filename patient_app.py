import streamlit as st
import random
from datetime import datetime

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="MindEase - Daily Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# DEFAULT SETTINGS / SESSION STATE INIT
# =====================================================
DEFAULTS = {
    "active_tab": "game",
    "theme": "Warm Sunrise",
    "font_scale": "Large",
    "high_contrast": False,
    "sound_on": True,
    "reduce_motion": False,
    "last_speech": "",
    "game_intro_spoken": False,
}
for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

if "tasks" not in st.session_state:
    st.session_state["tasks"] = {"task1": False, "task2": False, "task3": False}

if "mood_log" not in st.session_state:
    st.session_state["mood_log"] = []

# =====================================================
# THEME DEFINITIONS
# =====================================================
THEMES = {
    "Warm Sunrise": {"bg1": "#FFF9F2", "bg2": "#E8F5E9", "primary": "#2E7D32",
                      "secondary": "#558B2F", "accent": "#FF9800", "accent_dark": "#E65100",
                      "card": "rgba(255,255,255,0.96)", "border": "#E0E0E0"},
    "Ocean Calm": {"bg1": "#F0F8FF", "bg2": "#E1F0FA", "primary": "#0D47A1",
                   "secondary": "#1565C0", "accent": "#00ACC1", "accent_dark": "#006064",
                   "card": "rgba(255,255,255,0.96)", "border": "#D6E9F5"},
    "Lavender Peace": {"bg1": "#FBF7FF", "bg2": "#F1E6FA", "primary": "#6A1B9A",
                        "secondary": "#8E24AA", "accent": "#AB47BC", "accent_dark": "#4A148C",
                        "card": "rgba(255,255,255,0.96)", "border": "#E6D6F2"},
    "Soft Blush": {"bg1": "#FFF5F7", "bg2": "#FDECEF", "primary": "#AD1457",
                   "secondary": "#C2185B", "accent": "#F06292", "accent_dark": "#880E4F",
                   "card": "rgba(255,255,255,0.96)", "border": "#F5D9E0"},
}

FONT_SCALES = {
    "Normal": {"title": 32, "sub": 18, "section": 22, "body": 16, "button": 18},
    "Large": {"title": 40, "sub": 21, "section": 26, "body": 19, "button": 22},
    "Extra Large": {"title": 48, "sub": 24, "section": 30, "body": 22, "button": 26},
}

theme = THEMES[st.session_state["theme"]]
fonts = FONT_SCALES[st.session_state["font_scale"]]

if st.session_state["high_contrast"]:
    bg1, bg2 = "#000000", "#111111"
    card_bg, text_main, border_col = "#1A1A1A", "#FFFFFF", "#FFD54F"
    primary = secondary = accent = "#FFD54F"
    accent_dark = "#FFA000"
else:
    bg1, bg2 = theme["bg1"], theme["bg2"]
    card_bg, text_main, border_col = theme["card"], "#263238", theme["border"]
    primary, secondary, accent, accent_dark = theme["primary"], theme["secondary"], theme["accent"], theme["accent_dark"]

motion_css = "" if not st.session_state["reduce_motion"] else "*{transition:none !important; animation:none !important;}"

# =====================================================
# DYNAMIC CSS — smooth easing, mobile-first layout
# =====================================================
st.markdown(f"""
    <style>
    html {{ scroll-behavior: smooth; }}

    .stApp {{
        background: linear-gradient(135deg, {bg1} 0%, {bg2} 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: {text_main};
    }}

    .block-container {{
        padding-top: 1.4rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 900px;
    }}

    section[data-testid="stSidebar"] {{
        background: {card_bg};
        border-right: 2px solid {border_col};
    }}

    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(16px) scale(0.98); }}
        to   {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    @keyframes popIn {{
        0%   {{ opacity: 0; transform: scale(0.7); }}
        60%  {{ opacity: 1; transform: scale(1.08); }}
        100% {{ transform: scale(1); }}
    }}
    @keyframes pulseGlow {{
        0%   {{ box-shadow: 0 0 0 0 {accent}55; }}
        70%  {{ box-shadow: 0 0 0 18px {accent}00; }}
        100% {{ box-shadow: 0 0 0 0 {accent}00; }}
    }}

    .glass-card {{
        background: {card_bg};
        border-radius: 24px;
        padding: 26px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 2px solid {border_col};
        margin-bottom: 22px;
        animation: fadeInUp 0.45s cubic-bezier(0.22, 1, 0.36, 1);
    }}

    .main-title {{
        font-size: clamp(28px, 6vw, {fonts['title']}px) !important;
        font-weight: 800;
        color: {primary};
        text-align: center;
        margin-bottom: 4px;
        letter-spacing: 0.3px;
    }}
    .sub-title {{
        font-size: clamp(15px, 3.2vw, {fonts['sub']}px) !important;
        color: {secondary};
        text-align: center;
        margin-bottom: 16px;
        font-weight: 500;
    }}
    .section-head {{
        font-size: clamp(19px, 4.4vw, {fonts['section']}px) !important;
        font-weight: 800;
        color: {primary};
        margin-bottom: 12px;
        border-bottom: 3px dashed {border_col};
        padding-bottom: 8px;
    }}
    .body-text {{
        font-size: clamp(14px, 3vw, {fonts['body']}px) !important;
        color: {text_main};
        line-height: 1.5;
    }}

    div.stButton > button {{
        width: 100%;
        min-height: 64px;
        font-size: clamp(15px, 3.6vw, {fonts['button']}px) !important;
        font-weight: 800 !important;
        border-radius: 18px !important;
        border: 2px solid {border_col} !important;
        box-shadow: 0 5px 14px rgba(0,0,0,0.09) !important;
        transition: transform 0.18s cubic-bezier(0.34, 1.56, 0.64, 1),
                    box-shadow 0.25s ease, border-color 0.25s ease, background 0.25s ease !important;
        color: {text_main} !important;
        background: linear-gradient(180deg, #FFFFFF 0%, {bg2} 100%) !important;
        will-change: transform;
    }}
    div.stButton > button:hover {{
        transform: translateY(-3px) scale(1.025);
        box-shadow: 0 10px 20px rgba(0,0,0,0.16) !important;
        border-color: {accent} !important;
    }}
    div.stButton > button:active {{
        transform: translateY(0) scale(0.96);
        box-shadow: 0 3px 8px rgba(0,0,0,0.14) !important;
        transition-duration: 0.06s !important;
    }}

    .nav-active button {{
        background: linear-gradient(180deg, {accent} 0%, {accent_dark} 100%) !important;
        color: white !important;
        border-color: {accent_dark} !important;
        animation: popIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}

    .target-card {{
        text-align: center;
        background: linear-gradient(180deg, #FFF3E0 0%, #FFE0B2 100%);
        border: 3px dashed {accent};
        border-radius: 22px;
        padding: 20px;
        margin-bottom: 20px;
        animation: pulseGlow 2.4s infinite, popIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}
    .target-card h1 {{ font-size: clamp(56px, 14vw, 84px); margin: 8px 0; }}

    .task-done {{
        background-color: {bg2};
        border-left: 8px solid {accent};
        padding: 14px;
        border-radius: 12px;
        font-size: clamp(14px, 3vw, {fonts['body']}px);
        font-weight: 700;
        color: {primary};
        animation: popIn 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}

    .badge {{
        display: inline-block;
        padding: 6px 14px;
        border-radius: 999px;
        background: {accent}22;
        color: {accent_dark};
        font-weight: 700;
        font-size: clamp(12px, 2.6vw, {fonts['body']-2}px);
        margin: 3px 6px 3px 0;
        animation: fadeInUp 0.3s ease;
    }}

    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, {accent} 0%, {primary} 100%) !important;
        transition: width 0.6s cubic-bezier(0.22, 1, 0.36, 1) !important;
    }}

    div[data-testid="stHorizontalBlock"] {{
        gap: 14px !important;
        row-gap: 14px !important;
    }}
    div[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton {{ animation-delay: 0.02s; }}
    div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton {{ animation-delay: 0.08s; }}
    div[data-testid="stHorizontalBlock"] > div:nth-child(3) .stButton {{ animation-delay: 0.14s; }}
    div[data-testid="stHorizontalBlock"] > div:nth-child(4) .stButton {{ animation-delay: 0.20s; }}
    div[data-testid="stHorizontalBlock"] > div:nth-child(5) .stButton {{ animation-delay: 0.26s; }}
    div[data-testid="stHorizontalBlock"] > div:nth-child(6) .stButton {{ animation-delay: 0.32s; }}
    .stButton {{ animation: fadeInUp 0.4s cubic-bezier(0.22, 1, 0.36, 1) backwards; }}

    /* ---------- MOBILE OPTIMIZATION ---------- */
    @media (max-width: 640px) {{
        .block-container {{ padding-left: 0.6rem !important; padding-right: 0.6rem !important; }}

        div[data-testid="stHorizontalBlock"] {{
            flex-wrap: wrap !important;
        }}
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
            flex: 1 1 46% !important;
            min-width: 46% !important;
        }}
        div.stButton > button {{
            min-height: 84px !important;
        }}
        .glass-card {{ padding: 18px 14px; border-radius: 18px; }}
        .target-card h1 {{ font-size: 64px; }}
    }}

    {motion_css}
    </style>
""", unsafe_allow_html=True)

# =====================================================
# VOICE ASSISTANT (SPEECH SYNTHESIS)
# =====================================================
def speak(text):
    """Voice feedback engine using HTML/JavaScript. Cancels cleanly, then speaks."""
    st.session_state["last_speech"] = text
    if not st.session_state["sound_on"]:
        return
    safe_text = text.replace("'", "\\'")
    js_code = f"""
        <script>
            window.speechSynthesis.cancel();
            setTimeout(function() {{
                var msg = new SpeechSynthesisUtterance('{safe_text}');
                msg.rate = 0.88;
                msg.pitch = 1.0;
                window.speechSynthesis.speak(msg);
            }}, 120);
        </script>
    """
    st.components.v1.html(js_code, height=0)

def replay_last():
    if st.session_state["last_speech"]:
        speak(st.session_state["last_speech"])

CORRECT_PHRASES = [
    "Wonderful! You found the {item}.",
    "That's it! The {item}, well done.",
    "Perfect match — the {item} is correct.",
    "Great eyes! You spotted the {item}.",
]
WRONG_PHRASES = [
    "That is the {item}. Look for the picture at the top and try again.",
    "Not quite — that one is the {item}. Take your time and try once more.",
    "Close, but that's the {item}. Look carefully and give it another go.",
]
STREAK_PHRASES = [
    "You are on a {n} in a row streak, amazing focus!",
    "{n} correct in a row! You're doing great.",
    "Nice work, that's {n} in a row now.",
]

# =====================================================
# SIDEBAR: CUSTOMIZATION PANEL
# =====================================================
with st.sidebar:
    st.markdown(f"<h2 style='color:{primary};'>⚙️ Customize MindEase</h2>", unsafe_allow_html=True)

    st.markdown("**🎨 Colour Theme**")
    new_theme = st.selectbox("Choose a theme", list(THEMES.keys()),
                              index=list(THEMES.keys()).index(st.session_state["theme"]),
                              label_visibility="collapsed")
    if new_theme != st.session_state["theme"]:
        st.session_state["theme"] = new_theme
        st.rerun()

    st.markdown("**🔠 Text Size**")
    new_font = st.select_slider("Choose text size", options=list(FONT_SCALES.keys()),
                                 value=st.session_state["font_scale"], label_visibility="collapsed")
    if new_font != st.session_state["font_scale"]:
        st.session_state["font_scale"] = new_font
        st.rerun()

    st.markdown("**🌓 Display**")
    new_contrast = st.toggle("High Contrast Mode", value=st.session_state["high_contrast"])
    if new_contrast != st.session_state["high_contrast"]:
        st.session_state["high_contrast"] = new_contrast
        st.rerun()

    new_motion = st.toggle("Reduce Animations", value=st.session_state["reduce_motion"])
    if new_motion != st.session_state["reduce_motion"]:
        st.session_state["reduce_motion"] = new_motion
        st.rerun()

    st.markdown("**🔊 Voice Reminders**")
    new_sound = st.toggle("Enable Spoken Feedback", value=st.session_state["sound_on"])
    if new_sound != st.session_state["sound_on"]:
        st.session_state["sound_on"] = new_sound
        st.rerun()

    if st.button("🔁 Repeat Last Message"):
        replay_last()

    st.markdown("---")
    st.caption("💡 Tip: On a phone, buttons now arrange into an easy two-per-row grid so they're simple to tap.")

# =====================================================
# HEADER SECTION
# =====================================================
st.markdown("<h1 class='main-title'>🌸 MindEase Companion</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Your friendly daily activity & brain exercise space</p>", unsafe_allow_html=True)

now = datetime.now()
st.markdown(
    f"<p class='body-text' style='text-align:center; opacity:0.75;'>🗓️ {now.strftime('%A, %d %B %Y')} &nbsp;•&nbsp; 🕒 {now.strftime('%I:%M %p')}</p>",
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# TOP NAVIGATION TABS (active-state highlight)
# =====================================================
nav_items = [
    ("game", "🧩 Memory Arcade", "Welcome to the Memory Arcade! Tap the picture that matches the glowing card."),
    ("mood", "💛 How Are You?", "Let's check in on how you are feeling today."),
    ("schedule", "📋 Daily Schedule", "Here is your schedule for today."),
]
nav_cols = st.columns(3)
for col, (key, label, phrase) in zip(nav_cols, nav_items):
    with col:
        is_active = st.session_state["active_tab"] == key
        st.markdown(f"<div class='{'nav-active' if is_active else ''}'>", unsafe_allow_html=True)
        if st.button(label, key=f"nav_{key}"):
            st.session_state["active_tab"] = key
            speak(phrase)
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# MODULE 1: INTERACTIVE MEMORY ARCADE (GAME)
# =====================================================
if st.session_state["active_tab"] == "game":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-head'>🧩 Emoji & Symbol Match Game</div>", unsafe_allow_html=True)
    st.markdown(
        "<p class='body-text'>Look at the glowing target card, then tap the matching picture below. "
        "The game gently gets a little bigger as your streak grows.</p>",
        unsafe_allow_html=True
    )

    ALL_ITEMS = [
        {"name": "SUN", "icon": "☀️", "speech": "Sun"},
        {"name": "FLOWER", "icon": "🌸", "speech": "Flower"},
        {"name": "TEA", "icon": "🍵", "speech": "Tea Cup"},
        {"name": "BIRD", "icon": "🐦", "speech": "Bird"},
        {"name": "STAR", "icon": "⭐", "speech": "Star"},
        {"name": "APPLE", "icon": "🍎", "speech": "Apple"},
    ]

    if "target_item" not in st.session_state:
        st.session_state["target_item"] = random.choice(ALL_ITEMS)
        st.session_state["score"] = 0
        st.session_state["streak"] = 0
        st.session_state["best_streak"] = 0

    if not st.session_state["game_intro_spoken"]:
        speak("Look at the picture in the orange dashed card, then tap the same picture in the grid below it.")
        st.session_state["game_intro_spoken"] = True

    n_cards = min(4 + st.session_state["streak"] // 3, 6)
    target = st.session_state["target_item"]

    pool = ALL_ITEMS[:n_cards]
    if target["name"] not in [p["name"] for p in pool]:
        pool = pool[:-1] + [target]
    random.Random(target["name"]).shuffle(pool)

    st.markdown(f"""
        <div class='target-card'>
            <p style='font-size: clamp(14px,3.2vw,{fonts['body']}px); color: {accent_dark}; font-weight:bold; margin:0;'>FIND THIS MATCH:</p>
            <h1 style='margin: 8px 0;'>{target['icon']}</h1>
            <h3 style='font-size: clamp(18px,4.4vw,{fonts['section']}px); color: {accent_dark}; margin:0;'>{target['name']}</h3>
        </div>
    """, unsafe_allow_html=True)

    per_row = 3 if len(pool) > 4 else min(len(pool), 4)
    for row_start in range(0, len(pool), per_row):
        row_items = pool[row_start:row_start + per_row]
        cols = st.columns(len(row_items))
        for col, item in zip(cols, row_items):
            with col:
                if st.button(f"{item['icon']}\n{item['name']}", key=f"btn_game_{item['name']}"):
                    if item["name"] == target["name"]:
                        st.session_state["score"] += 10
                        st.session_state["streak"] += 1
                        st.session_state["best_streak"] = max(st.session_state["best_streak"], st.session_state["streak"])
                        phrase = random.choice(CORRECT_PHRASES).format(item=item["speech"])
                        if st.session_state["streak"] > 0 and st.session_state["streak"] % 3 == 0:
                            phrase += " " + random.choice(STREAK_PHRASES).format(n=st.session_state["streak"])
                        speak(phrase)
                        if not st.session_state["reduce_motion"]:
                            st.balloons()
                        remaining = [i for i in ALL_ITEMS if i["name"] != target["name"]]
                        st.session_state["target_item"] = random.choice(remaining)
                        st.rerun()
                    else:
                        st.session_state["streak"] = 0
                        speak(random.choice(WRONG_PHRASES).format(item=item["speech"]))
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<span class='badge'>⭐ {st.session_state['score']} Points</span>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<span class='badge'>🔥 Streak: {st.session_state['streak']}</span>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<span class='badge'>🏆 Best: {st.session_state['best_streak']}</span>", unsafe_allow_html=True)

    st.progress(min(st.session_state["streak"] / 9, 1.0), text="Progress toward the next difficulty level")
    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# MODULE 2: DAILY MOOD & WELLNESS CHECK-IN
# =====================================================
elif st.session_state["active_tab"] == "mood":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-head'>💛 How are you feeling right now?</div>", unsafe_allow_html=True)
    st.markdown("<p class='body-text'>Tap an emotion to share how your day is going.</p>", unsafe_allow_html=True)

    moods = [
        ("😊", "Happy", "col_happy", "I am so glad to hear that you are feeling happy today! Keep that lovely energy going.", "success", "✨ Wonderful! Keep smiling today."),
        ("😌", "Peaceful", "col_calm", "That is lovely to hear. Wishing you a calm and pleasant rest of your day.", "info", "🌿 Peace and quiet is wonderful for the mind."),
        ("🥱", "Tired", "col_tired", "Thank you for telling me. Remember to take rest and drink some water.", "warning", "☕ Take it easy and enjoy a gentle rest."),
        ("😟", "Worried", "col_worried", "It is okay to feel worried sometimes. Let's take a slow, deep breath together, in and out.", "warning", "🤍 You are not alone. A short walk or a chat with someone you trust can help."),
    ]

    cols_m = st.columns(len(moods))
    for col, (icon, label, key, phrase, style, msg) in zip(cols_m, moods):
        with col:
            if st.button(f"{icon} {label}", key=key):
                speak(phrase)
                st.session_state["mood_log"].append((now.strftime("%I:%M %p"), label))
                getattr(st, style)(msg)

    if st.session_state["mood_log"]:
        st.markdown("<br><div class='body-text'><b>📝 Today's Check-ins:</b></div>", unsafe_allow_html=True)
        for t, label in reversed(st.session_state["mood_log"][-5:]):
            st.markdown(f"<span class='badge'>{t} — {label}</span>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# MODULE 3: DAILY ROUTINE & INTERACTIVE LIST
# =====================================================
elif st.session_state["active_tab"] == "schedule":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-head'>📋 Today's Routine Schedule</div>", unsafe_allow_html=True)

    tasks_config = [
        ("task1", "1. Morning Medication & Breakfast (8:30 AM)",
         "Time for morning medication with a fresh glass of water.",
         "Great job completing your morning routine!"),
        ("task2", "2. Afternoon Walk or Rest (2:00 PM)",
         "Time for a gentle short walk or relaxation.",
         "Walk completed! Stay hydrated."),
        ("task3", "3. Evening Wind-down & Reading (7:00 PM)",
         "Time to relax with a book or some quiet music before bed.",
         "Lovely! A calm evening helps you sleep well."),
    ]

    completed = sum(st.session_state["tasks"].values())
    st.progress(completed / len(tasks_config), text=f"{completed} of {len(tasks_config)} tasks completed today")
    st.markdown("<br>", unsafe_allow_html=True)

    for i, (tkey, title, read_phrase, done_phrase) in enumerate(tasks_config):
        st.markdown(f"<h3 class='body-text' style='color:{primary}; font-size:clamp(16px,4vw,{fonts['body']+4}px);'>{title}</h3>", unsafe_allow_html=True)
        t_col1, t_col2 = st.columns([2, 1])

        with t_col1:
            if st.button("🔊 Read Reminder", key=f"audio_{tkey}"):
                speak(read_phrase)

        with t_col2:
            if not st.session_state["tasks"][tkey]:
                if st.button("✅ Mark Done", key=f"btn_done_{tkey}"):
                    st.session_state["tasks"][tkey] = True
                    speak(done_phrase)
                    st.rerun()
            else:
                st.markdown("<div class='task-done'>✓ Completed</div>", unsafe_allow_html=True)

        if i < len(tasks_config) - 1:
            st.divider()

    if completed == len(tasks_config):
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("🎉 All tasks completed for today — wonderful work!")
        if not st.session_state["reduce_motion"]:
            st.balloons()

    if st.button("🔄 Reset Today's Tasks", key="reset_tasks"):
        st.session_state["tasks"] = {k: False for k in st.session_state["tasks"]}
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
