import streamlit as st
import random
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MindEase - Daily Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MODERN ACCESSIBLE UI DESIGN (CSS) ---
st.markdown("""
    <style>
    /* Gradient Warm Background */
    .stApp {
        background: linear-gradient(135deg, #FFF9F2 0%, #E8F5E9 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Soft Floating Card Container */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 2px solid #E0E0E0;
        margin-bottom: 25px;
        transition: transform 0.2s ease;
    }

    /* Friendly Typography */
    .main-title {
        font-size: 42px !important;
        font-weight: 800;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 5px;
    }
    
    .sub-title {
        font-size: 22px !important;
        color: #558B2F;
        text-align: center;
        margin-bottom: 25px;
    }

    .section-head {
        font-size: 28px !important;
        font-weight: 700;
        color: #1B5E20;
        margin-bottom: 15px;
    }

    /* Custom Pastel Large Action Buttons */
    div.stButton > button {
        width: 100%;
        height: 75px;
        font-size: 24px !important;
        font-weight: 700 !important;
        border-radius: 20px !important;
        border: none !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1) !important;
        transition: all 0.2s ease-in-out !important;
        color: #1A3636 !important;
    }

    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15) !important;
    }

    /* Task Completion Banner */
    .task-done {
        background-color: #E8F5E9;
        border-left: 6px solid #4CAF50;
        padding: 15px;
        border-radius: 12px;
        font-size: 20px;
        font-weight: 600;
        color: #2E7D32;
    }
    </style>
""", unsafe_allow_html=True)

# --- BROWSER SPEECH SYNTHESIS (VOICE ASSISTANT) ---
def speak(text):
    """Voice feedback engine using HTML/JavaScript."""
    js_code = f"""
        <script>
            window.speechSynthesis.cancel();
            var msg = new SpeechSynthesisUtterance('{text}');
            msg.rate = 0.85;
            msg.pitch = 1.0;
            window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(js_code, height=0)

# --- HEADER SECTION ---
st.markdown("<h1 class='main-title'>🌸 MindEase Companion</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Your friendly daily activity & brain exercise space</p>", unsafe_allow_html=True)

# --- TOP NAVIGATION TABS ---
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    if st.button("🧩 Memory Arcade", key="nav_game"):
        st.session_state['active_tab'] = "game"
        speak("Welcome to the Memory Arcade!")

with col_nav2:
    if st.button("💛 How Are You?", key="nav_mood"):
        st.session_state['active_tab'] = "mood"
        speak("Let's check in on how you are feeling today.")

with col_nav3:
    if st.button("📋 Daily Schedule", key="nav_schedule"):
        st.session_state['active_tab'] = "schedule"
        speak("Here is your schedule for today.")

if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = "game"

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# MODULE 1: INTERACTIVE MEMORY ARCADE (GAME)
# ==========================================
if st.session_state['active_tab'] == "game":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-head'>🧩 Emoji & Symbol Match Game</div>", unsafe_allow_html=True)
    st.write("<p style='font-size: 20px; color: #555;'>Look at the active target item and tap the matching card below!</p>", unsafe_allow_html=True)

    # Game State Management
    ITEMS = [
        {"name": "SUN", "icon": "☀️", "speech": "Sun"},
        {"name": "FLOWER", "icon": "🌸", "speech": "Flower"},
        {"name": "TEA", "icon": "🍵", "speech": "Tea Cup"},
        {"name": "BIRD", "icon": "🐦", "speech": "Bird"}
    ]

    if 'target_item' not in st.session_state:
        st.session_state['target_item'] = random.choice(ITEMS)
        st.session_state['score'] = 0
        st.session_state['streak'] = 0

    target = st.session_state['target_item']

    # Display Active Target Card
    st.markdown(f"""
        <div style='text-align: center; background: #FFF3E0; border: 3px dashed #FF9800; border-radius: 20px; padding: 20px; margin-bottom: 25px;'>
            <p style='font-size: 22px; color: #E65100; font-weight:bold; margin:0;'>FIND THIS MATCH:</p>
            <h1 style='font-size: 80px; margin: 10px 0;'>{target['icon']}</h1>
            <h3 style='font-size: 28px; color: #D84315; margin:0;'>{target['name']}</h3>
        </div>
    """, unsafe_allow_html=True)

    # Interactive Game Buttons
    cols = st.columns(4)
    for idx, item in enumerate(ITEMS):
        with cols[idx]:
            if st.button(f"{item['icon']}\n{item['name']}", key=f"btn_game_{idx}"):
                if item['name'] == target['name']:
                    st.session_state['score'] += 10
                    st.session_state['streak'] += 1
                    speak(f"Awesome! You found the {item['speech']}.")
                    st.balloons()
                    # Choose new target
                    st.session_state['target_item'] = random.choice([i for i in ITEMS if i['name'] != target['name']])
                    st.rerun()
                else:
                    speak(f"That is the {item['speech']}. Give it another try!")

    # Live Score Metrics
    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"<h3 style='color: #2E7D32;'>⭐ Total Stars: <b>{st.session_state['score']} Points</b></h3>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<h3 style='color: #E65100;'>🔥 Streak: <b>{st.session_state['streak']} in a row!</b></h3>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MODULE 2: DAILY MOOD & WELLNESS CHECK-IN
# ==========================================
elif st.session_state['active_tab'] == "mood":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-head'>💛 How are you feeling right now?</div>", unsafe_allow_html=True)
    st.write("<p style='font-size: 20px; color: #555;'>Tap an emotion to share how your day is going.</p>", unsafe_allow_html=True)

    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        if st.button("😊 Happy", key="mood_happy"):
            speak("I am so glad to hear that you are feeling happy today!")
            st.success("✨ Wonderful! Keep smiling today.")

    with col_m2:
        if st.button("😌 Peaceful", key="mood_calm"):
            speak("That is lovely. Wishing you a calm and pleasant day.")
            st.info("🌿 Peace and quiet is wonderful for the mind.")

    with col_m3:
        if st.button("🥱 Tired", key="mood_tired"):
            speak("Remember to take rest and drink some water.")
            st.warning("☕ Take it easy and enjoy a gentle rest.")

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MODULE 3: DAILY ROUTINE & INTERACTIVE LIST
# ==========================================
elif st.session_state['active_tab'] == "schedule":
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-head'>📋 Today's Routine Schedule</div>", unsafe_allow_html=True)

    # Initialize task state
    if 'tasks' not in st.session_state:
        st.session_state['tasks'] = {
            "task1": False,
            "task2": False
        }

    # Task 1
    st.markdown("<h3 style='color: #1B5E20;'>1. Morning Medication & Breakfast (8:30 AM)</h3>", unsafe_allow_html=True)
    t1_col1, t1_col2 = st.columns([2, 1])
    
    with t1_col1:
        if st.button("🔊 Read Reminder", key="audio_t1"):
            speak("Time for morning medication with a fresh glass of water.")
            
    with t1_col2:
        if not st.session_state['tasks']['task1']:
            if st.button("✅ Mark Done", key="btn_done1"):
                st.session_state['tasks']['task1'] = True
                speak("Great job completing your morning routine!")
                st.rerun()
        else:
            st.markdown("<div class='task-done'>✓ Completed</div>", unsafe_allow_html=True)

    st.divider()

    # Task 2
    st.markdown("<h3 style='color: #1B5E20;'>2. Afternoon Walk or Rest (2:00 PM)</h3>", unsafe_allow_html=True)
    t2_col1, t2_col2 = st.columns([2, 1])
    
    with t2_col1:
        if st.button("🔊 Read Reminder", key="audio_t2"):
            speak("Time for a gentle short walk or relaxation.")
            
    with t2_col2:
        if not st.session_state['tasks']['task2']:
            if st.button("✅ Mark Done", key="btn_done2"):
                st.session_state['tasks']['task2'] = True
                speak("Walk completed! Stay hydrated.")
                st.rerun()
        else:
            st.markdown("<div class='task-done'>✓ Completed</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
